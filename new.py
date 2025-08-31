import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Set initial values
high_detected = False
no_light_counter = 0
distance_threshold = 1500
detection_time_threshold = 120
beam_status = "STAY HIGH"

# Debug view toggles
show_gray = False
show_blur = False
show_thresh = False
show_red_mask = False
show_red_overlay = False

print("[i] Press 1: Toggle Grayscale")
print("[i] Press 2: Toggle Blurred")
print("[i] Press 3: Toggle Bright Spot Threshold")
print("[i] Press 4: Toggle Red Mask")
print("[i] Press 5: Toggle Red Overlay")
print("[i] Press Q to quit")

# Store created windows to avoid NULL window errors
windows_created = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect red regions (tail lamps)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    _, thresh = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    high_detected = False

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 100 < area < 4000:
            x, y, w, h = cv2.boundingRect(cnt)
            roi_red = red_mask[y:y+h, x:x+w]
            red_pixels = cv2.countNonZero(roi_red)
            total_pixels = w * h
            red_ratio = red_pixels / (total_pixels + 1e-5)

            if red_ratio > 0.5:
                continue

            if y + h > frame.shape[0] * 0.5:
                high_detected = True
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                if area > distance_threshold:
                    beam_status = "TURN LOW"
                    no_light_counter = 0
                else:
                    beam_status = "STAY HIGH"

    if not high_detected:
        no_light_counter += 1
        if no_light_counter > detection_time_threshold:
            beam_status = "STAY HIGH"

    # Display the beam status
    color = (0, 0, 255) if beam_status == "TURN LOW" else (0, 255, 0)
    cv2.putText(frame, beam_status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5)

    # Helper function to safely show/destroy windows
    def show_window(name, image, show_flag):
        if show_flag:
            if name not in windows_created:
                cv2.namedWindow(name, cv2.WINDOW_NORMAL)
                windows_created.add(name)
            cv2.imshow(name, image)
        else:
            if name in windows_created:
                try:
                    cv2.destroyWindow(name)
                    windows_created.remove(name)
                except:
                    pass

    show_window('Grayscale', gray, show_gray)
    show_window('Blurred', blurred, show_blur)
    show_window('Thresholded Bright Spots', thresh, show_thresh)
    show_window('Red Mask (Tail Lamps)', red_mask, show_red_mask)
    red_overlay = cv2.bitwise_and(frame, frame, mask=red_mask)
    show_window('Red Light Overlay', red_overlay, show_red_overlay)

    # Show final frame
    cv2.imshow('Final Frame', frame)

    # Handle keypresses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        show_gray = not show_gray
    elif key == ord('2'):
        show_blur = not show_blur
    elif key == ord('3'):
        show_thresh = not show_thresh
    elif key == ord('4'):
        show_red_mask = not show_red_mask
    elif key == ord('5'):
        show_red_overlay = not show_red_overlay
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
