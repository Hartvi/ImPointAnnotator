import json
import numpy as np
from image_utils import *
from label_container import *
from typing import List
from load_detectron2_test_data import *

"""
for info in infos:
        image_boxes = list()
        for box in info.box_results:
            tmp = dict()
            tmp["initial_bbox"] = np.array(box.initial_bbox).tolist()
            tmp["category_list"] = np.array(box.category_list).tolist()
            tmp["material_list"] = np.array(box.material_list).tolist()
            image_boxes.append(tmp)
        dict_to_save[info.name] = image_boxes
    with open("deez_outputs.json", "w") as f:
        json.dump(dict_to_save, f)
"""


def load_ipalm_outputs(json_file="deez_outputs.json"):
    with open(json_file, "r") as f:
        json_dict = json.load(f)
        ret = dict()
        for source_image_path in json_dict:
            image_file = source_image_path.split("/")[-1]
            box_results = list()
            for box_dict in json_dict[source_image_path]:
                box_result = BoxResult()
                box_result.material_list = box_dict["material_list"]
                box_result.category_list = box_dict["category_list"]
                box_result.initial_bbox = box_dict["initial_bbox"]
                box_results.append(box_result)
            ret[image_file] = box_results
        return ret


def load_test_annotations(json_file="../test_annotations.json"):
    with open(json_file, "r") as f:
        json_dict = json.load(f)
        all_labels = AllLabels(json_dict)
        return all_labels
        # print(all_labels)


def load_annotations_from_files():
    json_files = ("../test_annotations.json", "../test_clean.data.txt")
    ret_dict = dict()
    with open(json_files[1], "r") as f:
        data = json.load(f)
        annotation_dict = get_image_annotations_list(data)
        ret_dict.update(annotation_dict)
        # print(len(ret_dict))
    with open(json_files[0], "r") as f:
        json_dict = json.load(f)
        ret_dict.update(json_dict)
        # print(len(ret_dict))
    all_labels = AllLabels(ret_dict)
    return all_labels


if __name__ == "__main__":
    print("testing load_test_annotations")
    print(load_test_annotations())
    print("testing load_ipalm_outputs")
    print(load_ipalm_outputs())


