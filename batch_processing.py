from calibrataion_diff import get_pm_weight_normalized
from fft_analysis import get_natural_frequency
from video_processing import get_roi_by_select, extract_leaf_position
import pandas as pd


def process_one_leaf(video_clean_path, video_pm_path, m_leaf, slope, roi_clean=None, roi_pm=None):
    if roi_clean is None:
        roi_clean = get_roi_by_select(video_clean_path)

    if roi_clean is None:
        return None

    rx_c, ry_c, rw_c, rh_c = roi_clean

    # 2. 깨끗 영상 분석
    cy_clean, fps, nan_per_c = extract_leaf_position(video_clean_path, rx_c, ry_c, rw_c, rh_c)
    freq_clean, _, _ = get_natural_frequency(cy_clean, fps)

    # 3. PM 영상 ROI
    if roi_pm is None:
        roi_pm = get_roi_by_select(video_pm_path)

    if roi_pm is None:
        return None

    rx_p, ry_p, rw_p, rh_p = roi_pm

    # 4. PM 영상 분석
    cy_pm, fps, nan_per_p = extract_leaf_position(video_pm_path, rx_p, ry_p, rw_p, rh_p)
    freq_pm, _, _ = get_natural_frequency(cy_pm, fps)

    # 5. PM 무게 추정
    predicted_pm = get_pm_weight_normalized(freq_clean, freq_pm, m_leaf, slope)

    # 6. 반환 (dict 형태)
    return {
        'freq_clean': freq_clean,
        'freq_pm': freq_pm,
        'predicted_pm': predicted_pm,
        'roi_clean': roi_clean,
        'roi_pm': roi_pm,
        'nan_per_clean': nan_per_c,
        'nan_per_pm': nan_per_p
    }


def process_all_leaves(csv_path, slope):
    df = pd.read_csv(csv_path)
    
    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()

    for index, row in df.iterrows():
        leaf_inex = row.get('잎번호')
        video_clean_path = row.get('영상_clean')
        video_pm_path = row.get('영상_pm')
        m_leaf = row.get('m_leaf')

        if pd.isna(video_clean_path) or pd.isna(video_pm_path) or pd.isna(m_leaf):
            print(f"잎 {leaf_inex}: 데이터 누락(영상 경로 또는 잎 무게), 건너뜀")
            continue

        print(f"\n=== 잎 {leaf_inex} 분석 ===")

        result = process_one_leaf(
            video_clean_path=video_clean_path,
            video_pm_path=video_pm_path,
            m_leaf=m_leaf,
            slope=slope
        )

        if result is None:
            print(f"잎 {leaf_inex}: 분석 실패")
            continue

        # CSV에 결과 기록 (1회 측정)
        df.loc[index, 'Freq_Clean_1'] = result['freq_clean']
        df.loc[index, 'Freq_PM_1'] = result['freq_pm']
        df.loc[index, '잎_예측무게'] = result['predicted_pm']

        print(f"잎 {leaf_inex}: 깨끗 {result['freq_clean']:.4f}, PM 후 {result['freq_pm']:.4f}")
        print(f"잎 {leaf_inex}: 예측 PM {result['predicted_pm']:.4f} mg")

    # 저장
    df.to_csv(csv_path, index=False)
    print(f"\n=== 전체 분석 완료, {csv_path} 업데이트됨 ===")

    return df
