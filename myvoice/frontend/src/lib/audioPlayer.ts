export class AudioPlayer {
    private audio: HTMLAudioElement;
    private queue: string[] = [];
    private isPlaying: boolean = false;
    private onPlaybackEnd: (() => void) | null = null;
    private _muted: boolean = false;

    constructor() {
        this.audio = new Audio();
        this.audio.onended = () => {
            this.playNext();
        };
    }

    get muted(): boolean {
        return this._muted;
    }

    set muted(value: boolean) {
        this._muted = value;
        this.audio.muted = value;
    }

    playBase64(base64Audio: string, onEnd?: () => void): void {
        this.queue.push(base64Audio);
        if (onEnd) this.onPlaybackEnd = onEnd;

        if (!this.isPlaying) {
            this.playNext();
        }
    }

    private playNext(): void {
        if (this.queue.length === 0) {
            this.isPlaying = false;
            if (this.onPlaybackEnd) {
                this.onPlaybackEnd();
                this.onPlaybackEnd = null;
            }
            return;
        }

        const nextAudio = this.queue.shift();
        if (nextAudio) {
            this.isPlaying = true;
            const mime = detectMimeType(nextAudio);
            this.audio.src = `data:${mime};base64,${nextAudio}`;
            this.audio.muted = this._muted;
            this.audio.play().catch(console.error);
        }
    }

    stop(): void {
        this.audio.pause();
        this.queue = [];
        this.isPlaying = false;
    }
}

/** Detect audio MIME type from base64-encoded data by checking magic bytes. */
function detectMimeType(base64: string): string {
    // Decode first few bytes to check file signatures
    const raw = atob(base64.slice(0, 16));
    if (raw.length >= 4 && raw.slice(0, 4) === 'RIFF') return 'audio/wav';
    if (raw.length >= 4 && raw.slice(0, 4) === 'OggS') return 'audio/ogg';
    if (raw.length >= 3 && raw.slice(0, 3) === 'ID3') return 'audio/mp3';
    if (raw.length >= 2 && raw.charCodeAt(0) === 0xff && (raw.charCodeAt(1) & 0xe0) === 0xe0) return 'audio/mp3';
    // Default fallback
    return 'audio/mp3';
}
