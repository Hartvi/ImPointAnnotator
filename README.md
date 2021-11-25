### Test data generator
- `annotation/annotator.py` - script for creating test data for the detectron+mobilenet pipeline by clicking on images
- `evaluation/ipalm_evaluator.py` - script to generate confusion matrix from which to calculate the precision for Andrej

The goal of this project is to have some way of evaluating the precision of an object detection/instance segmentation framework. This particular case has two outputs per bounding box, namely object category and material. Precision can be calculated from a confusion matrix, however confusion matrices are not well defined for outputs with a spatial dimension. Therefore, in this project we have defined an additional evaluation class for the case when the prediction misses the location of a class label in the test image, the class being the first row and column of the final confusion matrix.

<div align=center>
  <img src="https://i.imgur.com/1p9GkQb.png" width=600>
  <br>
  Figure 1. Evaluation process.
</div>
