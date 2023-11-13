import cv2
data_path='/Users/shivam_goyal/Desktop/ECE601/Sprint3/qrValues/'
def read_qrCode_and_save():
    # Open the camera (default camera index is 0)
    cap = cv2.VideoCapture(0)

    # Create QRCodeDetector object
    qr_code_detector = cv2.QRCodeDetector()

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Open a file for writing
    with open("qr_code_value.txt", "w") as file:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Detect and decode QR Code
            value, pts, qr_code = qr_code_detector.detectAndDecode(frame)

            if value:
                # Print the decoded value
                print(f"Deteched Value is: {value}")

                # Write the value to the file
                file.write(value + "\n")

                # Draw rectangle around the QR Code
                pts = pts.astype(int)  # Ensure that pts has integer values
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                # Break the loop after processing the QR code
                break

            # Display the frame
            cv2.imshow('QR Code', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    read_qrCode_and_save()
