#%%
import cv2
import numpy as np


def get_roi_by_select(video_path):
    # 1. 영상 열고 첫 프레임 읽기
    cap = cv2.VideoCapture(video_path)
    success, first_frame = cap.read()
    cap.release()

    if not success:
        return None

    # 2. ROI 드래그로 선택
    roi = cv2.selectROI("Select Leaf Tip ROI", first_frame, showCrosshair=True)

    cv2.destroyAllWindows()

    # 3. 결과 처리
    roi_x, roi_y, roi_w, roi_h = roi

    if roi_h == 0 or roi_w == 0:
        return None

    return roi_x, roi_y, roi_w, roi_h

def extract_leaf_position (video_path, roi):
    roi_x, roi_y, roi_w, roi_h = roi
    debug = False
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    success,first_frame = cap.read()
    if not success:
        return None
    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    mask = np.zeros_like(first_gray)
    mask[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = 255

    points = cv2.goodFeaturesToTrack(
        first_gray,
        maxCorners=1,
        qualityLevel=0.05,
        minDistance=10,
        mask=mask
    )

    prev_gray = first_gray
    prev_points = points
    cy_array = []


    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        next_points, status, error = cv2.calcOpticalFlowPyrLK(
            prev_gray, gray, prev_points, None
        )
        if status[0] == 1:
            x, y = next_points[0].ravel()
            cy_array.append(y)
        else:
            cy_array.append(np.nan)

        prev_gray = gray
        prev_points = next_points

        if debug:
            cv2.imshow("Window", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(30)
    nan_count = sum(1 for x in cy_array if np.isnan(x))
    nan_per = nan_count / len(cy_array) * 100
    return cy_array, fps, nan_per
