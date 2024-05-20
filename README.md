# Research-Practice Course 
> This File contains all the updates and Modification  Achieved from one week to the other
> , We are using :
> - python 3.6
> - TensorFlow 1.14
> - Tf-slim
> - Keras 2.2.4
> - Protobuf 3.20.3
> - h5py 2.10.0
> - Numpy 1.19.5
> - Lvis

## Week One to Week Four

Recieve The Dataset from My Supervisor and Start Labeling the dataset Using [LabelImg](https://github.com/HumanSignal/labelImg) Tools , The Dataset Contain More Than **400** Rock art Images From sevral places (Arminia, US, Bulgaria, Spain, Italy ), The Dataset contain Seven Classes : 
- Person
- Goat
- Stag
- Circle
- Spiral
- Zigzag
- Cross

## Week Five

Preprocess The dataset , Starting by generating CVS file From the Images XML **(For each Location)** files than create a TFrecord and a Label Map file and set the Model Parametere 

## Week six
Training the Dataset (US Dataset) on a Single Model " Faster R-CNN Inception v2" To make sure our dataset is Labelled well and the model can handle our data without issues,We Than test it on new Data never seen by the Model from (US, Armenia).

## Week Seven
 We select the pre-trained models that we will  use from [TensorFlow 1 Detection Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md), the models we are using are faster_rcnn_inception_v2_coco, faster_rcnn_resnet50_coco, faster_rcnn_resnet101_coco. we started training the USA (teacher1) data than Italy (techer2) on faster_rcnn_inception_v2_coco we **faced overfitting** due to the limited number of images.

## Week Eight to  Week Ten
We have been experiencing persistent overfitting with our model, despite multiple adjustments. Initially, we tried different learning rates and batch sizes, but the overfitting issue remained. We then changed our model architecture to use Faster R-CNN ResNet-50 COCO, yet the overfitting persisted.

To address this, we aggregated our data and split it into three subsets, ensuring an equal number of images in each. This approach did not alleviate the problem. We further adjusted the subsets to maintain an equal distribution of classes rather than the number of images, but overfitting was still an issue.

We then applied various data augmentation techniques, including flips, rotations, and image scaling, as well as regularization (L2), but these efforts were unsuccessful in reducing overfitting.

In an attempt to expand our dataset, we generated grayscale and stretched versions of our images and applied the same augmentation techniques. The model is currently in the training process with this expanded dataset.




