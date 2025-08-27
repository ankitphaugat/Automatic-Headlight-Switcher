import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale and HSV
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect red regions (tail lamps)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

    # Blur and threshold for bright spots
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

            # Ignore mostly red (tail lamps)
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
    if beam_status == "TURN LOW":
        cv2.putText(frame, beam_status, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    else:
        cv2.putText(frame, beam_status, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

    # Show debug views
    # Show debug views
    if show_gray:
        cv2.imshow('Grayscale', gray)
    else:
        if cv2.getWindowProperty('Grayscale', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Grayscale')

    if show_blur:
        cv2.imshow('Blurred', blurred)
    else:
        if cv2.getWindowProperty('Blurred', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Blurred')

    if show_thresh:
        cv2.imshow('Thresholded Bright Spots', thresh)
    else:
        if cv2.getWindowProperty('Thresholded Bright Spots', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Thresholded Bright Spots')

    if show_red_mask:
        cv2.imshow('Red Mask (Tail Lamps)', red_mask)
    else:
        if cv2.getWindowProperty('Red Mask (Tail Lamps)', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Red Mask (Tail Lamps)')

    if show_red_overlay:
        red_overlay = cv2.bitwise_and(frame, frame, mask=red_mask)
        cv2.imshow('Red Light Overlay', red_overlay)
    else:
        if cv2.getWindowProperty('Red Light Overlay', cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyWindow('Red Light Overlay')


    if show_red_overlay:
        red_overlay = cv2.bitwise_and(frame, frame, mask=red_mask)
        cv2.imshow('Red Light Overlay', red_overlay)
    else:
        try:
            cv2.destroyWindow('Red Light Overlay')
        except:
            pass

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

# Release resources
cap.release()
cv2.destroyAllWindows()

