import { useState, useCallback, useRef, useEffect } from 'react';
import type { UtteranceResponse } from '../api/types';
import { api } from '../api/client';
import { AudioPlayer } from '../lib/audioPlayer';
import { AudioRecorder } from '../lib/audioRecorder';
import { toast } from 'sonner';

export type SessionPhase = 'narrator' | 'transition' | 'interactive' | 'ended';

// A single rendered message bubble (child or AI)
export interface ChatMessage {
  id: string;
  speakerType: 'child' | 'ai';
  text: string;
  feedback?: UtteranceResponse['feedback'];
}

interface UseSessionFlowProps {
  sessionId: string | null;
  onPhaseChange?: (phase: SessionPhase) => void;
}

export function useSessionFlow({ sessionId, onPhaseChange }: UseSessionFlowProps) {
  const [phase, setPhaseState] = useState<SessionPhase>('narrator');
  const [isAiSpeaking, setIsAiSpeaking] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const audioPlayer = useRef<AudioPlayer>(new AudioPlayer());
  const recorder = useRef<AudioRecorder | null>(null);

  const setPhase = useCallback((newPhase: SessionPhase) => {
    setPhaseState(newPhase);
    onPhaseChange?.(newPhase);
  }, [onPhaseChange]);

  // Initialize Recorder
  useEffect(() => {
    recorder.current = new AudioRecorder({
      onDataAvailable: () => { },
      onStop: handleRecordingStop,
    });
    return () => {
      audioPlayer.current.stop();
    };
  }, [sessionId]); // eslint-disable-line react-hooks/exhaustive-deps

  const addChatMessages = useCallback((response: UtteranceResponse) => {
    const childText = response.childText?.trim();
    const aiText = response.aiResponseText?.trim();

    setMessages(prev => {
      const newMessages: ChatMessage[] = [];
      // Child bubble (only if there's actual text)
      if (childText) {
        newMessages.push({
          id: `child-${response.utteranceId ?? Date.now()}`,
          speakerType: 'child',
          text: childText,
        });
      }
      // AI bubble
      if (aiText) {
        newMessages.push({
          id: `ai-${response.utteranceId ?? Date.now()}`,
          speakerType: 'ai',
          text: aiText,
          feedback: response.feedback,
        });
      }
      return [...prev, ...newMessages];
    });

    // Play TTS audio
    if (response.aiResponseAudioBase64) {
      setIsAiSpeaking(true);
      audioPlayer.current.playBase64(response.aiResponseAudioBase64, () => {
        setIsAiSpeaking(false);
      });
    }
  }, []);

  const handleRecordingStop = async (blob: Blob) => {
    if (!sessionId) return;
    setIsRecording(false);
    setIsProcessing(true);

    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = async () => {
      const base64Audio = (reader.result as string).split(',')[1];

      try {
        const response = await api.post<UtteranceResponse>(
          `/v1/kid/sessions/${sessionId}/utterances`,
          { audio_data: base64Audio },
          { headers: { 'X-Idempotency-Key': crypto.randomUUID() }, skipCamelConversion: false }
        );

        if (response.nextPhase === 'interactive') {
          // Trigger word detected → add chat bubbles and advance to interactive
          addChatMessages({
            ...response,
            childText: response.childText || '',
          });
          setPhaseState(prev => prev === 'transition' ? 'interactive' : prev);
        } else if (response.nextPhase === 'transition') {
          // Guide response (trigger not detected) → play audio only, stay in transition
          if (response.aiResponseAudioBase64) {
            setIsAiSpeaking(true);
            audioPlayer.current.playBase64(response.aiResponseAudioBase64, () => {
              setIsAiSpeaking(false);
            });
          }
        } else {
          // Fallback: treat as interactive (e.g. old backend without next_phase)
          addChatMessages({
            ...response,
            childText: response.childText || '',
          });
          setPhaseState(prev => prev === 'transition' ? 'interactive' : prev);
        }

      } catch (err) {
        console.error("Failed to upload utterance", err);
        toast.error("오류가 발생했어요. 다시 시도해주세요.");
      } finally {
        setIsProcessing(false);
      }
    };
  };

  const startRecording = useCallback(async () => {
    if (isAiSpeaking || isProcessing) return;
    try {
      if (recorder.current) {
        await recorder.current.start();
        setIsRecording(true);
      }
    } catch {
      toast.error("마이크를 켜주세요!");
    }
  }, [isAiSpeaking, isProcessing]);

  const stopRecording = useCallback(() => {
    if (recorder.current && recorder.current.isRecording()) {
      recorder.current.stop(); // Triggers onStop -> handleRecordingStop
    }
  }, []);

  const toggleRecording = useCallback(() => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }, [isRecording, startRecording, stopRecording]);

  const advancePhase = useCallback((newPhase: SessionPhase) => {
    setPhase(newPhase);
  }, [setPhase]);

  return {
    phase,
    messages,
    isAiSpeaking,
    isRecording,
    isProcessing,
    startRecording,
    stopRecording,
    toggleRecording,
    advancePhase,
    setPhase,
  };
}
