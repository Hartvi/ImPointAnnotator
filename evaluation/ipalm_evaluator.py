from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt
from label_container import *
from sklearn.metrics import confusion_matrix
from image_utils import *
from ipalm_load_json import *
import cv2
import os
from mapping_utils import *

"""
all bboxes:
  inputs: list of all box_results
  outputs: confusion matrix for categories, confusion matrix for materials, 
           confidence list for categories,  confidence list for materials
"""
"""
single bbox:
  inputs: box_result: {im_name: str, bbox: 4 Tuple[float], category_list: 36 List[float], material_list 8 List[float]}
  outputs: correctness, confidence
"""


def is_inside_box(point, corner1, corner2):
    return corner1[0] < point[0] < corner2[0] and corner1[1] < point[1] < corner2[1]


def eval_box_result(box_result: BoxResult, box_labels: List[BoxLabel]):
    gt_category_ret = -1
    gt_material_ret = -1
    category_order = np.argsort(box_result.category_list)
    material_order = np.argsort(box_result.material_list)
    max_category = category_order[-1]
    max_material = material_order[-1]
    category_confidence = box_result.category_list[max_category] - box_result.category_list[category_order[-2]]
    material_confidence = box_result.material_list[max_material] - box_result.material_list[material_order[-2]]
    for box_label in box_labels:
        inside_box = is_inside_box(box_label.xy, box_result.initial_bbox[0:2], box_result.initial_bbox[2:4])
        if inside_box:
            gt_category_ret = box_label.gt_category
            gt_material_ret = box_label.gt_material

    return max_category, gt_category_ret, category_confidence, max_material, gt_material_ret, material_confidence


def eval_image_boxes(box_results: List[BoxResult], box_labels: List[BoxLabel]):
    category_predictions = list()
    category_gts = list()
    category_confidences = list()
    material_predictions = list()
    material_gts = list()
    material_confidences = list()
    for box_result in box_results:
        cat_pred, cat_gt, cat_conf, mat_pred, mat_gt, mat_conf = eval_box_result(box_result, box_labels)
        # category
        category_predictions.append(cat_pred)
        category_gts.append(cat_gt)
        category_confidences.append(cat_conf)
        # material
        material_predictions.append(mat_pred)
        material_gts.append(mat_gt)
        material_confidences.append(mat_conf)
    return category_predictions, category_gts, category_confidences, material_predictions, material_gts, material_confidences


def eval_all_images(pred_dict, gt_labels: AllLabels):
    category_predictions = list()
    category_gts = list()
    category_confidences = list()
    material_predictions = list()
    material_gts = list()
    material_confidences = list()
    results = (category_predictions, category_gts, category_confidences, material_predictions, material_gts, material_confidences)
    for image_name in pred_dict:
        # print(image_name, )
        result = eval_image_boxes(pred_dict[image_name],
                                  gt_labels.image_labels_dict[image_name])
        # print(result)
        append_to_2D_list(results, result)
    for k,category in enumerate(category_gts):
        if category != -1:
            category_gts[k] = str_to_shortened_id[category]
    for k, material in enumerate(material_gts):
        if material != -1:
            if material in real_material_to_ipalm_material:
                material = real_material_to_ipalm_material[material]
            material_gts[k] = material_str2ipalm_id[material]
    print("category confusion matrix:")
    category_cm = confusion_matrix(category_gts, category_predictions).tolist()
    plot_confusion_matrix(category_cm)
    print(confusion_matrix(category_gts, category_predictions).tolist())
    print("material confusion matrix:")
    material_cm = confusion_matrix(material_gts, material_predictions).tolist()
    print(confusion_matrix(material_gts, material_predictions).tolist())
    plot_confusion_matrix(material_cm)


def append_to_2D_list(list2d, item1d):
    for i in range(len(list2d)):
        list2d[i].extend(item1d[i])


def plot_confusion_matrix(xy_data):
    fig, ax = plt.subplots(1, 1)
    ax.set(xlabel='x axis', ylabel='y axis')
    # ax.set_xlim([-10, 10])
    # ax.set_ylim([-10, 10])
    # ax.yaxis.set_ticks([-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10])
    # ax.yaxis.set_ticks([])
    # ax.xaxis.set_ticks([-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10])
    # labels = [item.get_text() for item in ax.get_xticklabels()]
    # print(ax.get_xticklabels())
    # print(ax.get_yticklabels())
    # print(len(labels))
    # labels[3] = 'x0'
    # labels[4] = 'x0+dx'
    # ax.set_xticklabels(labels)

    # We want to show all ticks...
    # ax.set_xticks(np.arange(field_side))
    # ax.set_yticks(np.arange(field_side))
    # ... and label them with the respective list entries
    # tick_names = [str(i - field_side // 2) for i in range(field_side)]
    # tick_names = ["-10", "-7.5", "-5", "-2.5", "0", "2.5", "5", "7.5", "10"]
    # ax.set_xticklabels(tick_names)
    # ax.set_yticklabels(tick_names)
    ax.pcolormesh(xy_data, cmap='RdBu', label="Positions in square")
    # for i in range(field_side):
    #     for j in range(field_side):
    #         text = ax.text(j, i, data[i, j],
    #                        ha="center", va="center", color="w")
    # ax.legend()
    ax.set_title('Confusion matrix')
    fig.set_figwidth(8)
    fig.set_figheight(8)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    pred_dict = load_ipalm_outputs()
    # gt_labels = load_test_annotations()  # only from the annotator
    gt_labels = load_annotations_from_files()  # detectron2 test data + from annotator
    eval_all_images(pred_dict, gt_labels)

