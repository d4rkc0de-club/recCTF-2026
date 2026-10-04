import numpy as np
import scipy.io.wavfile as wav


flag = b"d4rk{aud1o+crypt0_m0dd3r_s8d5678za65}"
N = int.from_bytes(flag, byteorder='big')
print(N)
# Factorize N or pick p and q such that p * q = N
# For demonstration, we pick a 20-digit prime p that divides N (or we adjust p & q)
p = 67425040507649857454941801240897712669972003186574987280589
q = N // p
remainder = N % p

# Adjust q and compute exact flag integer N = p * q
N = p * q
actual_flag = N.to_bytes((N.bit_length() + 7) // 8, byteorder='big').decode()

print(f"[*] Left Channel  (p): {p}")
print(f"[*] Right Channel (q): {q}")
print(f"[*] Calculated Flag : {actual_flag}")

# ---------------------------------------------------------------
# 2. DTMF Audio Synthesizer
# ---------------------------------------------------------------
sample_rate = 44100
tone_duration = 0.15  # 150ms per digit
pause_duration = 0.05 # 50ms pause

# Standard DTMF Frequency Grid (Hz)
DTMF_KEYS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '0': (941, 1336)
}

def generate_dtmf_track(number_str):
    """Encodes a string of digits into a continuous mono DTMF audio track."""
    audio = []
    for digit in number_str:
        f1, f2 = DTMF_KEYS[digit]
        t = np.linspace(0, tone_duration, int(sample_rate * tone_duration), endpoint=False)
        tone = 0.5 * (np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t))
        pause = np.zeros(int(sample_rate * pause_duration))
        audio.extend(tone)
        audio.extend(pause)
    return np.array(audio, dtype=np.float32)

left_audio = generate_dtmf_track(str(p))
right_audio = generate_dtmf_track(str(q))

# Match lengths
max_len = max(len(left_audio), len(right_audio))
left_audio = np.pad(left_audio, (0, max_len - len(left_audio)))
right_audio = np.pad(right_audio, (0, max_len - len(right_audio)))

# ---------------------------------------------------------------
# 3. High-Frequency Spectrogram Hint ("FLAG = L * R")
# ---------------------------------------------------------------
# Bitmap matrix representing text "FLAG = L * R"
text_bitmap = [
    "1111 1     111    1111       1         111  ",
    "1    1    1   1  1           1    1 1  1  1 ",
    "111  1    11111  1  111  11  1     1   111  ",
    "1    1    1   1  1    1  11  1    1 1  1 1  ",
    "1    1111 1   1   1111       1111      1  1 "
]

total_samples = len(left_audio)
t = np.linspace(0, total_samples / sample_rate, total_samples, endpoint=False)
spectrogram_hint = np.zeros(total_samples, dtype=np.float32)

# Map bitmap pixels to frequencies between 14 kHz and 17 kHz
base_freq = 14000
freq_step = 600
cols = len(text_bitmap[0])
samples_per_col = total_samples // cols

for col_idx in range(cols):
    col_start = col_idx * samples_per_col
    col_end = (col_idx + 1) * samples_per_col
    t_col = t[col_start:col_end]
    
    for row_idx, row in enumerate(text_bitmap):
        if col_idx < len(row) and row[col_idx] == '1':
            freq = base_freq + (len(text_bitmap) - row_idx) * freq_step
            spectrogram_hint[col_start:col_end] += 0.05 * np.sin(2 * np.pi * freq * t_col)

# Combine audio tracks with high-frequency hint
left_channel = left_audio + spectrogram_hint
right_channel = right_audio + spectrogram_hint

# Normalize to 16-bit PCM WAV format
stereo_audio = np.column_stack((left_channel, right_channel))
stereo_audio = stereo_audio / np.max(np.abs(stereo_audio))
pcm_16bit = np.int16(stereo_audio * 32767)

wav.write("stereo_crypto_challenge.wav", sample_rate, pcm_16bit)
print("[+] Challenge saved to 'stereo_crypto_challenge.wav'")