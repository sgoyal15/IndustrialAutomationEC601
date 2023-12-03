import cv2
import time
import numpy as np

# Create an image with a red box
image = 255 * np.ones((300, 500, 3), dtype=np.uint8)
cv2.rectangle(image, (50, 50), (450, 250), (0, 0, 255), -1)
cv2.putText(image, "Waiting for Fingerprint.", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

while True:
    # Display the initial red box
    cv2.imshow('Authentication', image)
    cv2.waitKey(1000)  # 1-second delay

    key = cv2.waitKey(0)

    if key == ord('0'):  # User presses '0' for authentication
        cv2.rectangle(image, (50, 50), (450, 250), (0, 0, 255), -1)
        cv2.putText(image, "Authenticating...", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Authentication', image)
        cv2.waitKey(1000)  # 1-second delay
        # Simulate authentication success
        cv2.rectangle(image, (50, 50), (450, 250), (0, 255, 0), -1)
        cv2.putText(image, "Authenticated! ", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                    cv2.LINE_AA)
        cv2.imshow('Authentication', image)
        cv2.waitKey(1000)  # 1-second delay
        break  # Exit the loop after authentication

    elif key == ord('9'):  # User presses '9' to retry
        cv2.rectangle(image, (50, 50), (450, 250), (0, 0, 255), -1)
        cv2.putText(image, "Try Again.", (80, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow('Authentication', image)
        cv2.waitKey(1000)  # 1-second delay

    elif key == ord('q'):  # User presses 'q' to exit
        break

# Close the window
cv2.destroyAllWindows()
