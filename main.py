

# from statistatics import compare_with_airkorea
from video_processing import extract_leaf_position, get_roi_by_select
from fft_analysis import get_natural_frequency
from calibrataion_diff import run_calibration_analysis, get_pm_weight_normalized


def main():
    slope, _ = run_calibration_analysis()

    file_clean_path = 'test.mp4'
    print("깨긋한 잎 영상의 잎 끝을 드래그하세요")
    roi_clean = get_roi_by_select(file_clean_path)
    if roi_clean is None:
        print("ROI 지정 실패")
        return
    roi_x_c, roi_y_c, roi_w_c, roi_h_c = roi_clean
    print(f"깨끗한 잎 영상의 ROI: ({roi_x_c}, {roi_y_c}, {roi_w_c}, {roi_h_c})")
    cy_array_clean, fps, nan_per_clean = extract_leaf_position(file_clean_path, roi_x_c, roi_y_c, roi_w_c, roi_h_c)
    freq_clean, nan_per_fft_clean, snr_clean = get_natural_frequency(cy_array_clean, fps)

    file_pm_path = 'test_pm.mp4'

    print("PM 부착 후 영상의 잎 끝을 드래그하세요")
    roi_pm = get_roi_by_select(file_pm_path)

    if roi_pm is None:
        print("PM 영상 ROI 지정 실패")
        return

    roi_x_p, roi_y_p, roi_w_p, roi_h_p = roi_pm
    print(f"PM ROI: x={roi_x_p}, y={roi_y_p}, w={roi_w_p}, h={roi_h_p}")

    cy_array_pm, fps, nan_per_pm = extract_leaf_position(
        file_pm_path, roi_x_p, roi_y_p, roi_w_p, roi_h_p
    )
    freq_pm, nan_per_fft_pm, snr_pm = get_natural_frequency(cy_array_pm, fps)


    m_leaf = 2000


    predicted_pm = get_pm_weight_normalized(freq_clean, freq_pm, m_leaf, slope)

    #final_score = compare_with_airkorea('experiment_data.csv')


    print("=== LeafTEOM Pilot 분석 ===")
    print(f"깨끗한 잎 진동수: {freq_clean:.4f} Hz")
    print(f"PM 부착 후 진동수: {freq_pm:.4f} Hz")
    print(f"진동수 변화: {freq_clean - freq_pm:.4f} Hz")
    print(f"잎 무게: {m_leaf} mg")
    print(f"캘리브레이션 slope: {slope:.4f}")
    print(f"예측 PM 무게: {predicted_pm:.4f} mg")

if __name__ == "__main__":
    main()
