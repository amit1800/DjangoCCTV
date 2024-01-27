import cv2
from aiortc import VideoStreamTrack
from av import VideoFrame
import asyncio
from from_root import from_root
from ultralytics import YOLO
import os
from from_root import from_root

ROOT = os.path.dirname(__file__)


classes = ["bag", "human", "smoke", "fire", "number-plate"]

# Load a model
model = YOLO(os.path.join(ROOT, "new-best.pt"))


def get_infer_data(output):
    infer_data = []
    for box in output[0].boxes:
        box_data = {
            "class": int(box.cls.numpy().data.tolist()[0]),
            "conf": box.conf.numpy().data.tolist()[0],
            "box": [int(p) for p in box.xyxy.numpy().data.tolist()[0]],
        }
        infer_data.append(box_data)
    return infer_data


def overlay_prediction(img, infer_data, with_p=False):
    probability = round(infer_data["conf"], 2)
    class_name = classes[infer_data["class"]]
    class_name_with_p = f"{class_name} {probability:.2f}"
    text = class_name_with_p if with_p else class_name
    start_point = infer_data["box"][0], infer_data["box"][1]
    org = start_point[0], start_point[1] - 15
    font_scale = 1
    end_point = infer_data["box"][2], infer_data["box"][3]
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)
    thickness = 2
    line_type = cv2.LINE_AA
    rect_drawn = cv2.rectangle(img, start_point, end_point, color, thickness)
    class_drawn = cv2.putText(
        rect_drawn, text, org, font, font_scale, color, thickness, line_type
    )
    return class_drawn


class MLTrack(VideoStreamTrack):
    # face_cascade = cv2.CascadeClassifier(
    #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    # )

    def __init__(self, track) -> None:
        self.track = track
        super().__init__()

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")

        # def detect_faces(img):
        #     # Convert the image to grayscale
        #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #     # Detect faces in the image
        #     faces = self.face_cascade.detectMultiScale(
        #         gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        #     )
        #     if len(faces) == 0:
        #         return img
        #     # Draw rectangles around the faces
        #     for x, y, w, h in faces:
        #         img2 = cv2.rectangle(
        #             img,
        #             (x, y),
        #             (x + w, y + h),
        #             (255, 0, 0),
        #             2,
        #         )
        #         # return img2
        #     return img2

        # results = model(frame)
        def process_frame(frame):
            model = YOLO(os.path.join(ROOT, "new-best.pt"))
            results = model(frame)
            # print("result", results)
            annotated_frame = results[0].plot()
            # annot_data = get_infer_data(results)
            # annotated_frame = overlay_prediction(frame, annot_data[0])
            # print("annotated", annotated_frame.dtype)
            return annotated_frame

        # print(model.type)
        # inference_data = get_infer_data(results)
        new_frame = VideoFrame.from_ndarray(
            # overlay_prediction(img, inference_data[0]),
            process_frame(img),
            format="bgr24",
        )
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
