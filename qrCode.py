import cv2
import time
import signal 
import logging

data_path = '/Users/shivam_goyal/Desktop/ECE601/Sprint3/qrValues/'


def read_qrCode_and_save():
    # Open the camera (default camera index is 0)
    cap = cv2.VideoCapture(0)

    # Create QRCodeDetector object
    qr_code_detector = cv2.QRCodeDetector()

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Flag to track if QR code is detected
    qr_code_detected = False

    # Open a file for writing
    with open("qr_code_value.txt", "w") as file:
        while not qr_code_detected:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Detect and decode QR Code
            value, pts, qr_code = qr_code_detector.detectAndDecode(frame)

            if value:
                print("Processing QR code data...")
                print(f"Detected Value is: {value}")
                file.write(value + "\n")

                # Draw rectangle around the QR Code
                pts = pts.astype(int)  # Ensure that pts has integer values
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                # Set the flag to True to break out of the loop
                qr_code_detected = True

            # Display the frame
            cv2.imshow('QR Code', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the camera
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()
    # time.sleep(2)

def cleanup(signum, frame):
    log.info("Cleanup called with {0} and {1}".format(signum, frame))




if __name__ == "__main__":
    read_qrCode_and_save()
    # signal.signal(signal.SIGKILL, cleanup)
