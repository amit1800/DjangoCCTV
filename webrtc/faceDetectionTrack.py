import cv2
from aiortc import VideoStreamTrack
from av import VideoFrame
import asyncio


class FaceDetectionTrack(VideoStreamTrack):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    def __init__(self, track) -> None:
        self.track = track
        super().__init__()

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")

        def detect_faces(img):
            # Convert the image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            if len(faces) == 0:
                return img
            # Draw rectangles around the faces
            for x, y, w, h in faces:
                img2 = cv2.rectangle(
                    img,
                    (x, y),
                    (x + w, y + h),
                    (255, 0, 0),
                    2,
                )
                # return img2
            return img2

        new_frame = VideoFrame.from_ndarray(detect_faces(img), format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
