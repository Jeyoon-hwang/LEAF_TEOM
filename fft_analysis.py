import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_natural_frequency(cy_array, fps):
    cy_clean = pd.Series(cy_array).interpolate().bfill().to_numpy()
    cy_clean = cy_clean - np.mean(cy_clean)

    n = len(cy_clean)
    d = 1 / fps
    cy_clean = cy_clean * np.hanning(len(cy_clean))

    fft_result = np.abs(np.fft.fft(cy_clean))
    freq = np.fft.fftfreq(n, d)

    half = n // 2
    freq_half = freq[:half]
    fft_result_half = fft_result[:half]

    valid_idx = np.where((freq_half >= 1.0) & (freq_half <= 15.0))
    freq_resolution = freq_half[valid_idx]
    valid_ffts = fft_result_half[valid_idx]

    peak_index = np.argmax(valid_ffts)
    if peak_index == 0 or peak_index == len(valid_ffts) - 1:
        leaf_freq = freq_resolution[peak_index]
    else:
        Y_minus1 = valid_ffts[peak_index - 1]
        Y_0 = valid_ffts[peak_index]
        Y_plus1 = valid_ffts[peak_index + 1]

        denominator = Y_minus1 - 2*Y_0 + Y_plus1

        if denominator != 0:
            correction = 0.5 * (Y_minus1 - Y_plus1) / denominator
        else:
           correction = 0

        df = freq_resolution[1] - freq_resolution[0]
        leaf_freq = freq_resolution[peak_index] + correction * df

    #plt.plot(freq_resolution, valid_ffts)
    #plt.show()

    nan_fft_per = np.isnan(cy_array).sum() / len(cy_array) * 100
    snr = valid_ffts[peak_index] / np.mean(valid_ffts)
    return leaf_freq, nan_fft_per, snr
