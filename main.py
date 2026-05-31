from batch_processing import process_all_leaves
from calibrataion_diff import run_calibration_analysis


def main():
    slope, _ = run_calibration_analysis()

    if slope is None:
        print("캘리브레이션 실패, 프로그램을 종료합니다.")
        return

    process_all_leaves('experiment_data.csv', slope)


if __name__ == "__main__":
    main()
