/**
 * PCM16 Recorder - Captures 24kHz 16-bit mono PCM audio via AudioWorklet.
 * Outputs base64-encoded PCM16 chunks for WebSocket streaming.
 */

const TARGET_SAMPLE_RATE = 24000;
const BUFFER_SIZE = 4096;

// Inline AudioWorklet processor code (loaded as blob URL)
const WORKLET_CODE = `
class PcmProcessor extends AudioWorkletProcessor {
  process(inputs) {
    const input = inputs[0];
    if (input.length > 0) {
      const float32 = input[0];
      this.port.postMessage(float32.buffer, [float32.buffer]);
    }
    return true;
  }
}
registerProcessor('pcm-processor', PcmProcessor);
`;

export interface PcmRecorderCallbacks {
  onChunk: (base64Pcm16: string) => void;
  onError?: (error: Error) => void;
}

export class PcmRecorder {
  private stream: MediaStream | null = null;
  private audioContext: AudioContext | null = null;
  private workletNode: AudioWorkletNode | null = null;
  private _isRecording = false;

  isRecording(): boolean {
    return this._isRecording;
  }

  async start(callbacks: PcmRecorderCallbacks): Promise<void> {
    if (this._isRecording) return;

    try {
      this.stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: { ideal: TARGET_SAMPLE_RATE },
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      this.audioContext = new AudioContext({ sampleRate: TARGET_SAMPLE_RATE });
      const source = this.audioContext.createMediaStreamSource(this.stream);

      // Try AudioWorklet first, fall back to ScriptProcessor
      if (this.audioContext.audioWorklet) {
        await this._startWorklet(source, callbacks);
      } else {
        this._startScriptProcessor(source, callbacks);
      }

      this._isRecording = true;
    } catch (err) {
      this.cleanup();
      const error = err instanceof Error ? err : new Error(String(err));
      callbacks.onError?.(error);
      throw error;
    }
  }

  stop(): void {
    this._isRecording = false;
    this.cleanup();
  }

  private async _startWorklet(
    source: MediaStreamAudioSourceNode,
    callbacks: PcmRecorderCallbacks,
  ): Promise<void> {
    const blob = new Blob([WORKLET_CODE], { type: 'application/javascript' });
    const url = URL.createObjectURL(blob);

    try {
      await this.audioContext!.audioWorklet.addModule(url);
    } finally {
      URL.revokeObjectURL(url);
    }

    this.workletNode = new AudioWorkletNode(this.audioContext!, 'pcm-processor');
    this.workletNode.port.onmessage = (e: MessageEvent<ArrayBuffer>) => {
      if (!this._isRecording) return;
      const float32 = new Float32Array(e.data);
      const pcm16 = float32ToPcm16(float32);
      callbacks.onChunk(arrayBufferToBase64(pcm16.buffer as ArrayBuffer));
    };

    source.connect(this.workletNode);
    this.workletNode.connect(this.audioContext!.destination);
  }

  private _startScriptProcessor(
    source: MediaStreamAudioSourceNode,
    callbacks: PcmRecorderCallbacks,
  ): void {
    // ScriptProcessor fallback for browsers without AudioWorklet
    const processor = this.audioContext!.createScriptProcessor(BUFFER_SIZE, 1, 1);
    processor.onaudioprocess = (e: AudioProcessingEvent) => {
      if (!this._isRecording) return;
      const float32 = e.inputBuffer.getChannelData(0);
      const resampled = resample(float32, this.audioContext!.sampleRate, TARGET_SAMPLE_RATE);
      const pcm16 = float32ToPcm16(resampled);
      callbacks.onChunk(arrayBufferToBase64(pcm16.buffer as ArrayBuffer));
    };

    source.connect(processor);
    processor.connect(this.audioContext!.destination);
  }

  private cleanup(): void {
    this.workletNode?.disconnect();
    this.workletNode = null;

    if (this.audioContext && this.audioContext.state !== 'closed') {
      this.audioContext.close().catch(() => {});
    }
    this.audioContext = null;

    this.stream?.getTracks().forEach((t) => t.stop());
    this.stream = null;
  }
}

function float32ToPcm16(float32: Float32Array): Int16Array {
  const pcm16 = new Int16Array(float32.length);
  for (let i = 0; i < float32.length; i++) {
    const s = Math.max(-1, Math.min(1, float32[i]));
    pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
  }
  return pcm16;
}

function resample(input: Float32Array, fromRate: number, toRate: number): Float32Array {
  if (fromRate === toRate) return input;
  const ratio = fromRate / toRate;
  const outputLen = Math.round(input.length / ratio);
  const output = new Float32Array(outputLen);
  for (let i = 0; i < outputLen; i++) {
    output[i] = input[Math.round(i * ratio)] ?? 0;
  }
  return output;
}

function arrayBufferToBase64(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}
