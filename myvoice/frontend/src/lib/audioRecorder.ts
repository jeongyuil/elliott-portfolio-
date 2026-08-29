export interface AudioRecorderOptions {
    onDataAvailable: (blob: Blob) => void;
    onStop: (blob: Blob) => void;
}

// Pick the best supported mimeType
function getSupportedMimeType(): string {
    const types = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/ogg',
        'audio/mp4',
    ];
    for (const type of types) {
        if (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported(type)) {
            return type;
        }
    }
    return ''; // fallback: let browser choose
}

export class AudioRecorder {
    private mediaRecorder: MediaRecorder | null = null;
    private chunks: Blob[] = [];
    private options: AudioRecorderOptions;
    // Track pending stop request (if stop() called before MediaRecorder is ready)
    private pendingStop = false;
    private startPromise: Promise<void> | null = null;

    constructor(options: AudioRecorderOptions) {
        this.options = options;
    }

    async start(): Promise<void> {
        if (this.startPromise) return; // Already starting

        this.pendingStop = false;
        this.startPromise = this._doStart();
        await this.startPromise;
        this.startPromise = null;

        // If stop() was called while we were starting, stop now
        if (this.pendingStop) {
            this.stop();
        }
    }

    private async _doStart(): Promise<void> {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.chunks = [];

            const mimeType = getSupportedMimeType();
            this.mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});

            this.mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    this.chunks.push(e.data);
                    this.options.onDataAvailable(e.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                const type = this.mediaRecorder?.mimeType || 'audio/webm';
                const blob = new Blob(this.chunks, { type });
                this.options.onStop(blob);
                stream.getTracks().forEach(track => track.stop());
                this.mediaRecorder = null;
            };

            this.mediaRecorder.start();
        } catch (err) {
            this.startPromise = null;
            console.error('Error accessing microphone:', err);
            throw err;
        }
    }

    stop(): void {
        if (!this.mediaRecorder) {
            // start() not yet complete — mark pending
            this.pendingStop = true;
            return;
        }
        if (this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
        }
    }

    isRecording(): boolean {
        return this.mediaRecorder?.state === 'recording';
    }
}
