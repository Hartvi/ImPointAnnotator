import pickle
import numpy as np
import json
import mapping_utils
from label_container import *


def get_points(annotations): # list of dicts
    category_list = list()
    material_list = list()
    points = list()
    for annotation in annotations:
        category = mapping_utils.raw_id_to_catstr[annotation["category_id"]]
        material = mapping_utils.raw_id_to_matstr[annotation["category_id"]]

        category_list.append(category)
        material_list.append(material)
        points.append( ((annotation["bbox"][0]+annotation["bbox"][2])*0.5,
                        (annotation["bbox"][1]+annotation["bbox"][3])*0.5) )
    return points, category_list, material_list


def get_image_annotations(image_dict):
    im_name = image_dict["file_name"]
    points, categories, materials = get_points(image_dict["annotations"])
    return im_name, list(zip(points, categories, materials))


def get_image_annotations_list(dict_list):
    annotation_dict = dict()
    for image_dict in dict_list:
        im_name, values = get_image_annotations(image_dict)
        annotation_dict[im_name] = values
    # print(annotation_dict)
    return annotation_dict


# with open("../test_clean.data.txt", "r") as f:
#     data = json.load(f)
#     annotation_dict = get_image_annotations_list(data)
#     all_labels = AllLabels(annotation_dict)
#     print(all_labels)



"""
with open("../test.data.txt", "r") as f:
    text = f.read()
    # print(text)
    # if "<BoxMode.XYXY_ABS: 0>" in text:
    #     print("found the bastard")
    text = text.replace(r"'file_name'", "\"file_name\"")
    text = text.replace("'/local/temporary/DATASET/TEST/", "\"")  # )
    text = text.replace(".jpg'", ".jpg\"")
    # 'height': 2848, 'width': 4272, 'image_id': 25837, 'annotations': [{'bbox_mode': 'xyxy', 'category_id': 15, 'segmentation': {'size': [2848, 4272], 'counts'
    text = text.replace("'width'", "\"width\"")
    text = text.replace("'height'", "\"height\"")
    text = text.replace("'image_id'", "\"image_id\"")
    text = text.replace("'annotations'", "\"annotations\"")
    text = text.replace("'bbox_mode'", "\"bbox_mode\"")
    text = text.replace(r"<BoxMode.XYXY_ABS: 0>", "\"xyxy\"")
    text = text.replace("'category_id'", "\"category_id\"")
    text = text.replace("'segmentation'", "\"segmentation\"")
    text = text.replace("'size'", "\"size\"")
    text = text.replace("'counts'", "\"counts\"")
    text = text.replace(": b'", ": \"")
    text = text.replace(": '", ": \"")
    text = text.replace("', \"", "\", \"")
    text = text.replace("'}, ", "\"}, ")
    text = text.replace("'bbox'", "\"bbox\"")
    with open("../test_clean.data.txt", "w") as fw:
        fw.write(text)

    data = json.loads(text)
    for k in range(len(data)):
        print(data[k])
        break
"""



