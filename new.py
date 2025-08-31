import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

beam_status = "STAY HIGH"

# Debug toggles
show_gray = False
show_blur = False
show_thresh = False

print("[i] Press 1: Toggle Grayscale")
print("[i] Press 2: Toggle Blurred")
print("[i] Press 3: Toggle Thresholded Bright Spots")
print("[i] Press Q to quit")

windows_created = set()

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

# Helper function to put status text on a frame
def put_status_text(frame, status):
    color = (0, 0, 255) if status == "TURN LOW" else (0, 255, 0)
    cv2.putText(frame, status, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5)
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Detect very bright spots (headlights/flash)
    _, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)
    bright_pixels = cv2.countNonZero(thresh)

    # Decision: Default HIGH, switch to LOW if bright light
    if bright_pixels > 500:  # Adjust this value based on your lighting
        beam_status = "TURN LOW"
    else:
        beam_status = "STAY HIGH"

    # Show windows with status text
    show_window("Grayscale", put_status_text(gray.copy(), beam_status), show_gray)
    show_window("Blurred", put_status_text(blurred.copy(), beam_status), show_blur)
    show_window("Thresholded Bright Spots", put_status_text(thresh.copy(), beam_status), show_thresh)
    cv2.imshow("Final Frame", put_status_text(frame, beam_status))

    # Key handling
    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        show_gray = not show_gray
    elif key == ord('2'):
        show_blur = not show_blur
    elif key == ord('3'):
        show_thresh = not show_thresh
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
