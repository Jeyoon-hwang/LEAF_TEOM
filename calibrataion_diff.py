import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def normalized_diff_model(delta_m_over_m, slope):
    return slope * delta_m_over_m

def get_pm_weight_normalized(freq_clean, freq_pm, m_leaf, slope):
    delta_f = freq_clean - freq_pm
    delta_f_over_f = delta_f / freq_clean
    delta_m_over_m = delta_f_over_f / slope
    delta_m = m_leaf * delta_m_over_m

    return abs(delta_m)

def run_calibration_analysis():
    try:
        df = pd.read_csv('experiment_data.csv')
        df['Freq_Clean_Avg'] = df[['Freq_Clean_1', 'Freq_Clean_2', 'Freq_Clean_3']].mean(axis=1)
        df['Freq_PM_Avg']= df[['Freq_PM_1', 'Freq_PM_2', 'Freq_PM_3']].mean(axis=1)

        df['Delta_f_over_f'] = (df['Freq_Clean_Avg'] - df['Freq_PM_Avg']) / df['Freq_Clean_Avg']
        df['Delta_m_over_m'] = df['PM_Weight'] / df['m_leaf']

        x_data = df['Delta_m_over_m'].to_numpy()
        y_data = df['Delta_f_over_f'].to_numpy()

        popt, pcov = curve_fit(normalized_diff_model, x_data, y_data)
        slope_est = popt[0]

        y_pred = normalized_diff_model(x_data, slope_est)
        ss_res = np.sum((y_data - y_pred)**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r2 = 1- ss_res / ss_tot
        plt.figure(figsize=(8, 6))
        plt.scatter(x_data, y_data, color='red', label='Experiment')

        x_line = np.linspace(min(x_data), max(x_data), 100)
        y_fit = normalized_diff_model(x_line, slope_est)
        y_theory = normalized_diff_model(x_line, -0.5)

        plt.plot(x_line, y_fit, 'b-', label=f'Fitted (slope={slope_est:.3f})')
        plt.plot(x_line, y_theory, 'g--', label='Theory (slope=-0.5)')

        plt.xlabel('Δm / m_leaf')
        plt.ylabel('Δf / f_clean')
        plt.title(f'Normalized Calibration (R²={r2:.3f})')
        plt.legend()
        plt.grid()
        plt.show()
        return slope_est, r2

    except FileNotFoundError:
        print("파일이 없습니다. 추가해주십시요, 일단 진행하겠습니다.")
        return None,None

