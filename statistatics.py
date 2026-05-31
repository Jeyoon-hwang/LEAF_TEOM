import numpy as np
import pandas as pd
from dotenv import load_dotenv
from matplotlib.lines import lineStyles
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
from calibrataion_diff import get_pm_weight_normalized
import requests
import json
import os


def compare_with_airkorea(csv_file_path):

    load_dotenv()
    df = pd.read_csv('experiment_data.csv')

    API_KEY = os.getenv('AIRKOREA_API_KEY')
    url = 'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'

    real_pm10_list = []

    for index, row in df.iterrows():
        station_name = row['측정소명']

        params = {
            'serviceKey': API_KEY,
            'returnType': 'json',
            'numOfRows': '24',
            'pageNo': '1',
            'stationName': station_name,
            'dataTerm': 'DAILY',
            'ver': '1.3'
        }

        response = requests.get(url, params=params)
        data = json.loads(response.text)

        try:
            items = data['response']['body']['items']
            target_time = row['측정일시']

            pm10_value = None
            for item in items:
                if item['dataTime'] == target_time:
                    pm10_value = float(item['pm10Value'])
                    break
            real_pm10_list.append(pm10_value)
        except (KeyError, TypeError):
            real_pm10_list.append(None)

    df['실제_PM10'] = real_pm10_list

    df_clean = df.dropna()

    correlation, p_value = pearsonr(df_clean['실제_PM10'], df_clean['잎_예측무게'])

    print("\n" + "="*40)
    print("캘린브레이션 검증 결과 : ")
    print("="*40)
    print(f"피어슨 상관계수 : {correlation:.4f}")
    print(f"\n p-value: {p_value:.4f}")
    print("="*40)

    plt.figure(figsize=(8, 6))

    plt.scatter(df_clean['실제_PM10'], df_clean['잎_예측무게'], alpha=0.7, color='blue', label='Measured Data')

    z = np.polyfit(df_clean['실제_PM10'], (df_clean['잎_예측무게']), 1)
    p = np.poly1d(z)
    plt.plot(df_clean['실제_PM10'], p(df_clean['잎_예측무게']), "r--", label=f'Trendline (R={correlation:.2f})')

    plt.legend()
    plt.title('Real-world Verification', fontsize=14)
    plt.xlabel('AirKorea PM10 conecntration', fontsize=12)
    plt.ylabel('Predicted PM weight on Leaf', fontsize=12)
    plt.grid(True, lineStyles='--', alpha=0.5)
    plt.show()
    return correlation
