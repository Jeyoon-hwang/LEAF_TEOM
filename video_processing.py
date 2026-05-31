#%%
import cv2
import numpy as np

def extract_leaf_position (video_path):
    debug = False
    cap = cv2.VideoCapture(video_path)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    fps = cap.get(cv2.CAP_PROP_FPS)

    cy_array = []

    while cap.isOpened():
        success, frame = cap.read()
        
        if not success:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_white, upper_white)

        M = cv2.moments(mask)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cy_array.append(cy)
            #print(f"마커 중심 y좌표 : {cy}")
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        else:
            cy_array.append(np.nan)
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
