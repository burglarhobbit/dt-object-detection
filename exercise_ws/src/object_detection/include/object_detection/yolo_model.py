
from .yolov5.models.yolo import Model
import torch
import numpy as np
from .yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from PIL import Image, ImageDraw

class NoGPUAvailable(Exception):
    def __init__(self):
        print("GPU not available")

class Wrapper():
    def __init__(self, model_file):
        # if not torch.cuda.is_available():
        #     raise NoGPUAvailable()

        # TODO Instantiate your model and other class instances here!
        # TODO Don't forget to set your model in evaluation/testing/production mode, and sending it to the GPU
        # TODO If no GPU is available, raise the NoGPUAvailable exception

        self.device = torch.device("cuda") if (torch.cuda.is_available() else torch.device("cpu")
        self.model = Model("/code/exercise_ws/src/object_detection/include/object_detection/yolov5/models/yolov5s.yaml", ch=3, nc=4)
        self.model.load_state_dict(torch.load(model_file))
        self.model.to(self.device)
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

        self.model.eval()

    def draw_boxes(self, image, bboxes, classes=None):
        img =  Image.fromarray(image.copy())
        draw_obj = ImageDraw.Draw(img)
        for box in bboxes:
            draw_obj.rectangle(box)
        # img.show()
        return np.array(img)

    def predict(self, batch_or_image):

        # See this pseudocode for inspiration
        boxes = []
        labels = []
        scores = []
        for im0s in batch_or_image:  # or simply pipe the whole batch to the model instead of using a loop!

            # Padded resize
            # img = letterbox(im0s, new_shape=self.img_size)[0]

            img = im0s.transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    
            img = np.ascontiguousarray(img)
            
            half = False
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = self.model(img, augment=False)[0]
            # Apply NMS
            pred = non_max_suppression(pred, 0.25, 0.45, classes=0, agnostic=False)
            # print(pred)
            for i, det in enumerate(pred):  # detections per image
                if len(det):
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()

                    # Print results
                    # for c in det[:, -1].unique():
                    #     n = (det[:, -1] == c).sum()  # detections per class
                        # s += f'{n} {self.names[int(c)]}s, '  # add to string
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        # label = f'{names[int(cls)]} {conf:.2f}'
                        # plot_one_box(xyxy, im0, color=colors[int(cls)], line_thickness=3)
                        # plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)            

                        # box, label, score = self.model.predict(img) # TODO you probably need to send the image to a tensor, etc.

                        boxes.append(xyxy)
                        labels.append(self.names[int(cls)])
                        scores.append(conf)

        return boxes, labels, scores

if __name__ == "__main__":
    model_wrapper = Wrapper("yolov5/models/yolov5s.yaml")

