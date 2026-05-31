import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def leaf_vibration_model(x, k, m_init):
    leaf_freq = (1/ (2* np.pi) * np.sqrt(k /(m_init + x)))
    return leaf_freq

def get_pm_weight(leaf_freq, k, m_init):
    return (k / (( 2* np.pi * leaf_freq)**2)) - m_init

def run_calibration_analysis():
    try:
        df = pd.read_csv('experiment_data.csv')
        #df['Freq_Clean_Avg'] = df[['Freq_Clean_1'], 'Freq_Clean_2', 'Freq_Clean_3'].mean(axis=1)
        #df['Freq_PM_Avg']= df[['Freq_PM_1'], 'Freq_PM_2', 'Freq_PM_3'].mean(axis=1)
        #df['Freq_Diff'] = df['Freq_Clean_Avg'] - df['Freq_PM_Avg']

        df['Freq_Avg'] = df[['Freq_1', 'Freq_2', 'Freq_3']].mean(axis=1)
        x_real_data = df['PM_Weight'].to_numpy()
        y_real_data = df['Freq_Avg'].to_numpy()

        popt, pcov = curve_fit(leaf_vibration_model, x_real_data, y_real_data)
        k_est = popt[0]
        m_init_est = popt[1]

        y_pred = leaf_vibration_model(x_real_data, k_est, m_init_est)
        r2 = r2_score(y_real_data, y_pred)
        plt.figure()
        plt.scatter(x_real_data, y_real_data, color = 'red', label = 'Experiment Data')

        x_line = np.linspace(0, 2.5, 100)
        y_line = leaf_vibration_model(x_line, k_est, m_init_est)

        plt.plot(x_line, y_line, color = 'blue', label = 'Fitted Model')
        plt.legend()
        plt.grid()
        plt.show()
        return k_est, m_init_est, r2
    except FileNotFoundError:
        print("파일이 없습니다. 추가해주십시요, 일단 진행하겠습니다.")
        return None,None

