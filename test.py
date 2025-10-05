# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow
# if not cap.isOpened():
#     print("❌ Error: Could not open webcam.")
#     exit()

# print("📸 Opening webcam... Press 'q' to exit.")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("❌ Error: Failed to capture frame.")
#         break

#     cv2.imshow("Camera Test", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


# import bcrypt

# hashed_password = b"$2b$12$LHwwwpUCsdTMxF8BAR/C9.te2.g0CGkgEW1S7njTtwImoPdupwYxq"
# plain_password = b"yashsb07"  # Try your guess

# if bcrypt.checkpw(plain_password, hashed_password):
#     print("✅ Password matches!")
# else:
#     print("❌ Password does not match.")
