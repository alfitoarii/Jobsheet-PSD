import numpy as np
import scipy.signal as signal
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

# Fungsi untuk membuat filter lowpass IIR elliptic
def design_lowpass_iir(order, cutoff, fs, rp, rs):
    nyquist = 0.5 * fs
    norm_cutoff = cutoff / nyquist
    b, a = signal.ellip(order, rp, rs, norm_cutoff, btype='low', analog=False)
    return b, a

# Baca file WAV
input_wav_path = r'C:\Users\T530 ThinkPad\Documents\VS CODE\UAS PSD\Input.wav'
output_wav_path = r'C:\Users\T530 ThinkPad\Documents\VS CODE\UAS PSD\Output\Output_Elliptic.wav'
fs, data = wavfile.read(input_wav_path)

# Pastikan data adalah array 1D
if data.ndim > 1:
    data = data[:, 0]

# Desain filter IIR elliptic
order = 5  # Orde filter
cutoff_freq = 1000  # Frekuensi cutoff dalam Hz
rp = 0.5  # Ripple di passband (dB)
rs = 40  # Attenuation di stopband (dB)
b, a = design_lowpass_iir(order, cutoff_freq, fs, rp, rs)

# Terapkan filter ke sinyal
filtered_data = signal.filtfilt(b, a, data)

# Simpan hasil sinyal terfilter ke file WAV
wavfile.write(output_wav_path, fs, filtered_data.astype(np.int16))

# Plot sinyal asli dan hasil filter
plt.figure(figsize=(14, 10))

plt.subplot(4, 1, 1)
plt.plot(data)
plt.title('Sinyal Asli')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.subplot(4, 1, 2)
plt.plot(filtered_data)
plt.title('Sinyal Setelah Filter')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Plot impulse response
impulse = np.zeros(100)
impulse[0] = 1
impulse_response = signal.lfilter(b, a, impulse)
plt.subplot(4, 1, 3)
plt.plot(impulse_response)
plt.title('Impulse Response')
plt.xlabel('Tap')
plt.ylabel('Amplitude')

# Plot frequency response
w, h = signal.freqz(b, a, worN=8000)
plt.subplot(4, 1, 4)
plt.plot(0.5*fs*w/np.pi, np.abs(h))
plt.title('Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')

plt.tight_layout()
plt.show()
