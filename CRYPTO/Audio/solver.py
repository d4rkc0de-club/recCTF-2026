import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, filtfilt

# Standard DTMF Configuration
DTMF_MAP = {
    (697, 1209): '1', (697, 1336): '2', (697, 1477): '3',
    (770, 1209): '4', (770, 1336): '5', (770, 1477): '6',
    (852, 1209): '7', (852, 1336): '8', (852, 1477): '9',
    (941, 1336): '0'
}

LOW_FREQS = np.array([697, 770, 852, 941])
HIGH_FREQS = np.array([1209, 1336, 1477])

# Audio Processing & Filtering
def lowpass_filter(audio, sample_rate, cutoff=2000, order=5):
    """Removes all high-frequency spectrogram text noise above 2kHz."""
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, audio)

def decode_dtmf_channel(audio, sample_rate):
    """Extracts DTMF sequence using FFT with dynamic thresholding."""
    # Step A: Filter out high frequencies
    clean_audio = lowpass_filter(audio, sample_rate, cutoff=2000)
    
    # Step B: Frame sliding parameters (30ms frame, 10ms step)
    frame_len = int(sample_rate * 0.03)
    hop_len = int(sample_rate * 0.01)
    
    max_amp = np.max(np.abs(clean_audio))
    if max_amp == 0:
        return ""
        
    detected_sequence = []
    
    # Step C: Analyze frames
    for start in range(0, len(clean_audio) - frame_len, hop_len):
        frame = clean_audio[start:start + frame_len]
        
        # Ignore silent intervals between tones
        if np.max(np.abs(frame)) < 0.15 * max_amp:
            detected_sequence.append(None)
            continue
            
        # Compute Hanning-windowed FFT
        windowed = frame * np.hanning(len(frame))
        fft_vals = np.abs(np.fft.rfft(windowed))
        fft_freqs = np.fft.rfftfreq(len(frame), 1.0 / sample_rate)
        
        # Find peak energies in DTMF frequency bands
        low_energies = [fft_vals[np.argmin(np.abs(fft_freqs - f))] for f in LOW_FREQS]
        high_energies = [fft_vals[np.argmin(np.abs(fft_freqs - f))] for f in HIGH_FREQS]
        
        best_low_idx = np.argmax(low_energies)
        best_high_idx = np.argmax(high_energies)
        
        # Check if detected peaks are prominent enough
        if low_energies[best_low_idx] > 1.5 * np.mean(low_energies) and \
           high_energies[best_high_idx] > 1.5 * np.mean(high_energies):
            
            key = DTMF_MAP.get((LOW_FREQS[best_low_idx], HIGH_FREQS[best_high_idx]), None)
            detected_sequence.append(key)
        else:
            detected_sequence.append(None)
            
    # Step D: Debounce sequence (merge consecutive frames of the same digit)
    digits = []
    current_key = None
    for key in detected_sequence:
        if key != current_key:
            if key is not None:
                digits.append(key)
            current_key = key
            
    return "".join(digits)

def main(wav_file="stereo_crypto_challenge.wav"):
    print(f"Loading '{wav_file}'...")
    sample_rate, data = wav.read(wav_file)
    
    # Normalize input to float range [-1.0, 1.0]
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
        
    left_channel = data[:, 0]
    right_channel = data[:, 1]
    
    print("Decoding Left Channel (p)...")
    str_p = decode_dtmf_channel(left_channel, sample_rate)
    print(f"    └─ p = {str_p}")
    
    print("Decoding Right Channel (q)...")
    str_q = decode_dtmf_channel(right_channel, sample_rate)
    print(f"    └─ q = {str_q}")
    
    if not str_p or not str_q:
        print("\n[!] Error: Failed to extract p or q. Ensure audio contains valid DTMF tones.")
        return
        
    p = int(str_p)
    q = int(str_q)
    
    print("Performing crypto math (N = p * q)...")
    N = p * q
    
    num_bytes = (N.bit_length() + 7) // 8
    flag_bytes = N.to_bytes(num_bytes, byteorder='big')
    
    try:
        flag = flag_bytes.decode('utf-8')
        print(f"\nSUCCESS! Flag: {flag}")
    except UnicodeDecodeError:
        print("ok")

if __name__ == "__main__":
    main()