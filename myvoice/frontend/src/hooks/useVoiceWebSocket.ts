/**
 * useVoiceWebSocket - Dual-mode voice hook (WebSocket / HTTP fallback)
 *
 * WebSocket mode: PCM16 streaming via /v1/kid/voice/{sessionId}
 * HTTP mode: Falls back to existing useSessionFlow (AudioRecorder → POST /utterances)
 */
import { useState, useCallback, useRef, useEffect } from 'react';
import { PcmRecorder } from '@/lib/pcmRecorder';
import { AudioPlayer } from '@/lib/audioPlayer';
import { toast } from 'sonner';

const API_BASE = import.meta.env.VITE_API_BASE || '';

export interface VoiceMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  text: string;
  /** Special message types for UI rendering */
  uiType?: 'mood_checkin' | 'safety_pass' | 'closing_ritual' | 'mission_call' | 'goal_achieved';
}

interface ServerMessage {
  type: 'status' | 'transcript' | 'audio' | 'audio_chunk' | 'error' | 'mood_checkin' | 'safety_pass' | 'closing_ritual' | 'mission_call' | 'goal_achieved';
  message?: string;
  role?: 'user' | 'assistant';
  text?: string;
  audio?: string;
  chunk?: number;
  final?: boolean;
  /** Mission theme data for R0 */
  missionCode?: string;
  ritualPhrase?: string;
  closingPhrase?: string;
  /** Goal achievement data */
  keyExpression?: string;
}

type ConnectionState = 'disconnected' | 'connecting' | 'connected' | 'error';

interface UseVoiceWebSocketProps {
  sessionId: string | null;
  childToken: string | null;
  muted?: boolean;
  onStatusMessage?: (message: string) => void;
}

export function useVoiceWebSocket({
  sessionId,
  childToken,
  muted = false,
  onStatusMessage,
}: UseVoiceWebSocketProps) {
  const [messages, setMessages] = useState<VoiceMessage[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [isAiSpeaking, setIsAiSpeaking] = useState(false);
  const [connectionState, setConnectionState] = useState<ConnectionState>('disconnected');
  const [goalAchieved, setGoalAchieved] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const recorderRef = useRef<PcmRecorder>(new PcmRecorder());
  const playerRef = useRef<AudioPlayer>(new AudioPlayer());
  const audioChunksRef = useRef<string[]>([]);
  const audioStreamBufRef = useRef<string[]>([]);
  const mutedRef = useRef(muted);
  mutedRef.current = muted;

  // Stop playback immediately when muted
  useEffect(() => {
    if (muted) {
      playerRef.current.stop();
      setIsAiSpeaking(false);
    }
  }, [muted]);
  const msgIdRef = useRef(0);

  // Connect WebSocket
  const connect = useCallback(() => {
    if (!sessionId || !childToken) return;
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setConnectionState('connecting');

    // Build WS URL from API_BASE or window.location
    const base = API_BASE || window.location.origin;
    const wsBase = base.replace(/^http/, 'ws');
    const url = `${wsBase}/v1/kid/voice/${sessionId}`;

    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setConnectionState('connected');
      // Send auth token as first message instead of URL query parameter
      ws.send(JSON.stringify({ type: 'auth', token: childToken }));
      ws.send(JSON.stringify({ type: 'start' }));
    };

    ws.onmessage = (event) => {
      try {
        const data: ServerMessage = JSON.parse(event.data);
        handleServerMessage(data);
      } catch {
        console.error('Failed to parse WS message');
      }
    };

    ws.onerror = () => {
      setConnectionState('error');
    };

    ws.onclose = () => {
      setConnectionState('disconnected');
      wsRef.current = null;
    };
  }, [sessionId, childToken]); // eslint-disable-line react-hooks/exhaustive-deps

  // Handle incoming server messages
  const handleServerMessage = useCallback((data: ServerMessage) => {
    switch (data.type) {
      case 'status':
        onStatusMessage?.(data.message || '');
        break;

      case 'transcript':
        if (data.role && data.text) {
          // Hide internal system triggers from display
          if (data.role === 'user' && data.text.startsWith('[SYSTEM_OPENING]')) break;

          setMessages((prev) => [
            ...prev,
            {
              id: `msg-${++msgIdRef.current}`,
              role: data.role!,
              text: data.text!,
            },
          ]);
        }
        break;

      case 'audio':
        if (data.audio) {
          if (mutedRef.current) {
            // Muted — skip playback but still mark speaking cycle
            setIsAiSpeaking(true);
            setTimeout(() => setIsAiSpeaking(false), 300);
          } else {
            setIsAiSpeaking(true);
            playerRef.current.playBase64(data.audio, () => {
              setIsAiSpeaking(false);
            });
          }
        }
        break;

      case 'audio_chunk':
        if (data.audio) {
          audioStreamBufRef.current.push(data.audio);
          if (data.final) {
            const fullAudio = audioStreamBufRef.current.join('');
            audioStreamBufRef.current = [];
            if (mutedRef.current) {
              setIsAiSpeaking(true);
              setTimeout(() => setIsAiSpeaking(false), 300);
            } else {
              setIsAiSpeaking(true);
              playerRef.current.playBase64(fullAudio, () => {
                setIsAiSpeaking(false);
              });
            }
          }
        }
        break;

      case 'mood_checkin':
        // R3: Server asks for mood check-in → add system message for UI
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${++msgIdRef.current}`,
            role: 'system',
            text: data.message || '오늘 기분은 어때? 1, 2, 3 중에 골라줘!',
            uiType: 'mood_checkin',
          },
        ]);
        break;

      case 'safety_pass':
        // Safety Pass detected — show Popo intervention feedback
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${++msgIdRef.current}`,
            role: 'assistant',
            text: data.text || '알겠어, 캡틴! 포포가 도와줄게~',
            uiType: 'safety_pass',
          },
        ]);
        break;

      case 'closing_ritual':
        // R4: Closing ritual message
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${++msgIdRef.current}`,
            role: 'system',
            text: data.text || '',
            uiType: 'closing_ritual',
          },
        ]);
        break;

      case 'mission_call':
        // R0: Mission call + theme info
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${++msgIdRef.current}`,
            role: 'system',
            text: data.text || '',
            uiType: 'mission_call',
          },
        ]);
        break;

      case 'goal_achieved':
        // Mid-mission goal achievement — child said the key_expression
        setMessages((prev) => [
          ...prev,
          {
            id: `msg-${++msgIdRef.current}`,
            role: 'system',
            text: data.text || '미션 성공!',
            uiType: 'goal_achieved',
          },
        ]);
        setGoalAchieved(true);
        break;

      case 'error':
        toast.error(data.message || '오류가 발생했어요.');
        break;
    }
  }, [onStatusMessage]);

  // Send text message
  const sendText = useCallback((text: string) => {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ws.send(JSON.stringify({ type: 'text', text }));
  }, []);

  // Send mood score (R3 Emotion Check-in)
  const sendMood = useCallback((score: 1 | 2 | 3) => {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ws.send(JSON.stringify({ type: 'mood', score }));
    // Add user response to chat
    const labels = { 1: '😔 1 (조금 다운)', 2: '😊 2 (보통)', 3: '🤩 3 (신나요!)' };
    setMessages((prev) => [
      ...prev,
      {
        id: `msg-${++msgIdRef.current}`,
        role: 'user',
        text: labels[score],
      },
    ]);
  }, []);

  // Send end session (triggers R4 Closing Ritual)
  const sendEnd = useCallback(() => {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ws.send(JSON.stringify({ type: 'end' }));
  }, []);

  // Start recording
  const startRecording = useCallback(async () => {
    if (isAiSpeaking || isRecording) return;
    if (connectionState !== 'connected') {
      toast.error('연결 중입니다. 잠시 후 다시 시도해주세요.');
      return;
    }

    try {
      audioChunksRef.current = [];
      await recorderRef.current.start({
        onChunk: (base64Pcm16) => {
          // Accumulate chunks — send all at once when recording stops
          audioChunksRef.current.push(base64Pcm16);
        },
        onError: (err) => {
          console.error('Recording error:', err);
          setIsRecording(false);
          toast.error('마이크를 켜주세요!');
        },
      });
      setIsRecording(true);
    } catch {
      toast.error('마이크를 켜주세요!');
    }
  }, [isAiSpeaking, isRecording, connectionState]);

  // Stop recording — combine accumulated chunks and send as one message
  const stopRecording = useCallback(() => {
    if (!recorderRef.current.isRecording()) return;
    recorderRef.current.stop();
    setIsRecording(false);

    // Combine all PCM16 chunks and send as single audio message
    const chunks = audioChunksRef.current;
    if (chunks.length > 0) {
      const combined = combineBase64Chunks(chunks);
      audioChunksRef.current = [];
      const ws = wsRef.current;
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'audio', audio: combined }));
      }
    }
  }, []);

  // Toggle recording
  const toggleRecording = useCallback(() => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }, [isRecording, startRecording, stopRecording]);

  // End session
  const disconnect = useCallback(() => {
    const ws = wsRef.current;
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'end' }));
      ws.close();
    }
    recorderRef.current.stop();
    playerRef.current.stop();
    wsRef.current = null;
    setConnectionState('disconnected');
  }, []);

  // Auto-connect when sessionId + token are available
  useEffect(() => {
    if (sessionId && childToken) {
      connect();
    }
    return () => {
      disconnect();
    };
  }, [sessionId, childToken]); // eslint-disable-line react-hooks/exhaustive-deps

  // Clear messages
  const clearMessages = useCallback(() => setMessages([]), []);

  return {
    messages,
    isRecording,
    isAiSpeaking,
    connectionState,
    goalAchieved,
    connect,
    disconnect,
    startRecording,
    stopRecording,
    toggleRecording,
    sendText,
    sendMood,
    sendEnd,
    clearMessages,
  };
}

/** Combine multiple base64-encoded PCM16 chunks into a single base64 string. */
function combineBase64Chunks(chunks: string[]): string {
  // Decode all chunks to binary, concatenate, re-encode
  const decoded = chunks.map((c) => atob(c));
  let totalLen = 0;
  for (const d of decoded) totalLen += d.length;

  const combined = new Uint8Array(totalLen);
  let offset = 0;
  for (const d of decoded) {
    for (let i = 0; i < d.length; i++) {
      combined[offset++] = d.charCodeAt(i);
    }
  }

  let binary = '';
  for (let i = 0; i < combined.length; i++) {
    binary += String.fromCharCode(combined[i]);
  }
  return btoa(binary);
}
