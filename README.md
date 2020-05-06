# keras-yolo3

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Introduction

A Keras implementation of YOLOv3 (Tensorflow backend) based on [qqwweee/keras-yolo3](https://github.com/qqwweee/keras-yolo3).


---

## Quick Start

1. Download YOLOv3 config and weights from [YOLO website](http://pjreddie.com/darknet/yolo/).
2. Convert darknet YOLO weights to Keras weights.
3. Run YOLO detection.

```
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
python yolo_video.py [OPTIONS...] --image, for image detection mode, OR
python yolo_video.py [video_path] [output_path (optional)]
```

For Tiny YOLOv3, specify model path and anchor path with `--model model_file` and `--anchors anchor_file`.

<!--
### Usage
Use --help to see usage of yolo_video.py:
```
usage: yolo_video.py [-h] [--model MODEL] [--anchors ANCHORS]
                     [--classes CLASSES] [--gpu_num GPU_NUM] [--image]
                     [--input] [--output]

positional arguments:
  --input        Video input path
  --output       Video output path

optional arguments:
  -h, --help         show this help message and exit
  --model MODEL      path to model weight file, default model_data/yolo.h5
  --anchors ANCHORS  path to anchor definitions, default
                     model_data/yolo_anchors.txt
  --classes CLASSES  path to class definitions, default
                     model_data/coco_classes.txt
  --gpu_num GPU_NUM  Number of GPU to use, default 1
  --image            Image detection mode, will ignore all positional arguments
```
---
-->


4. MultiGPU usage: use `--gpu_num N` to use N GPUs. It is passed to the [Keras multi_gpu_model()](https://keras.io/utils/#multi_gpu_model).

## Training

1. Generate txt files for classes and annotations.  
    
    #### Classes
    Format: One class name in each row   
    Example: classes.txt
    ```
    person
    bicycle
    car
    motorbike
    aeroplane
    ...
    ```
    #### Annotations
    One row for one image   
    Row format: `image_file_path box1 box2 ... boxN`   
    Box format: `x_min,y_min,x_max,y_max,class_id`   
    To convert VOC XML annotations to YOLO format, use `python convert_voc_to_yolo.py --train_dir data/images/train/ --test_dir data/images/test --class_path data/classes.txt`
    
    Example: train.txt
    ```
    path/to/img1.jpg 50,100,150,200,0 30,50,200,120,3
    path/to/img2.jpg 120,300,250,600,2
    ...
    ```


2. Convert darknet yolov3 weights to keras weights 

    >Yolov3-tiny  
    >`python convert.py -w data/yolov3-tiny.cfg data/yolov3-tiny.weights data/tiny_yolo_weights.h5`

    >Yolov3   
    >`python convert.py -w data/yolov3.cfg data/yolov3.weights data/yolo_weights.h5`

    The file model_data/yolo_weights.h5 is used to load pretrained weights.


3. Generate new anchors (generally 6 for yolov3-tiny and 9 for yolov3) using
    
    >Yolov3-tiny   
    `python yolo_anchors_kmeans.py --train_path data/train.txt --anchor_path data/yolo_anchors.txt  --no_anchors 6`

    >Yolov3   
    >`python yolo_anchors_kmeans.py --train_path data/train.txt --anchor_path data/yolo_anchors.txt --no_anchors 9`


4. Modify the following variables in train.py:
    
    * *annotation_path*: Path for train.txt
    * *classes_path*: Path for classes.txt
    * *anchors_path*: Path for anchors.txt
    * *input_shape*: Image input shape (multiple of 32)
    
    Start training using `python train.py`

5. To evauate **images**, use *yolo3_eval_images.ipynb* jupyter notebook.

6. To eval **video**, use your weights stored in `trained_weights/` dir or checkpoint weights stored in `logs/` with command line option --model model_file when using yolo_video.py Remember to modify class path or anchor path, with --classes class_file and --anchors anchor_file.



Note:
To use original pretrained weights for YOLOv3:  
    1. `wget https://pjreddie.com/media/files/darknet53.conv.74`  
    2. rename it as darknet53.weights  
    3. `python convert.py -w darknet53.cfg darknet53.weights model_data/darknet53_weights.h5`  
    4. use model_data/darknet53_weights.h5 in train.py

---

## Some issues to know

1. The test environment is
    - Python 3.6.9
    - Keras 2.2.4
    - tensorflow 1.12.3

2. If you use your own anchors, probably some changes are needed.

3. The inference result is not totally the same as Darknet but the difference is small.

4. The speed is slower than Darknet. Replacing PIL with opencv may help a little.

5. Always load pretrained weights and freeze layers in the first stage of training. Or try Darknet training. It's OK if there is a mismatch warning.

6. The training strategy is for reference only. Adjust it according to your dataset and your goal. And add further strategy if needed.

7. For speeding up the training process with frozen layers train_bottleneck.py can be used. It will compute the bottleneck features of the frozen model first and then only trains the last layers. This makes training on CPU possible in a reasonable time. See [this](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html) for more information on bottleneck features.
