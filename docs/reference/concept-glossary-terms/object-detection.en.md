## object detection

- Meaning: Object detection is a vision task that predicts not only what is in an image, but also where each object is. It does not stop at `there is a cat`; it also asks where the cat is and how much space it occupies. The output is usually a set of `category + location` results for each detected object, not a single label.
- Why it matters: Object detection has a more complex output structure than image classification, and it is a representative example of deep learning expanding from category prediction to category and location prediction together. It helps separate classification, detection, and segmentation even when they all use image inputs. Understanding object detection also makes it easier to see why models such as YOLO are described as turning a multi-step vision pipeline into one prediction problem.
- Related concepts: `bounding box`, `YOLO`, `image recognition`, `output structure`
- Core Section: `P1-9.2`
- Appears in: `P1-9.3`, `P1-10.1`, `P5-11.1`, `P6-19.2`
