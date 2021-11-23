from typing import Dict


class BoxLabel:
    def __init__(self, xy, gt_category, gt_material):
        self.xy = xy
        self.gt_category = gt_category
        self.gt_material = gt_material


class ImageLabel:
    def __init__(self, im_name, points, categories, materials):
        self.im_name = im_name
        self.box_labels = list()
        for xy, gt_category, gt_material in zip(points, categories, materials):
            self.box_labels.append(BoxLabel(xy, gt_category, gt_material))

    def __iter__(self):
        yield from self.box_labels

    def __getitem__(self, item):
        return self.box_labels[item]

    def __len__(self):
        return len(self.box_labels)


class AllLabels:
    def __init__(self, test_annotations: Dict):
        self.image_labels_dict = dict()
        for key in test_annotations:
            im_name = key
            points = list()
            categories = list()
            materials = list()
            values = test_annotations[key]
            for value in values:
                points.append(value[0])
                categories.append(value[1])
                materials.append(value[2])
            # print(im_name, len(points), len(categories), len(materials))
            self.image_labels_dict[im_name] = ImageLabel(im_name, points, categories, materials)

    def __getitem__(self, item):
        return self.image_labels_dict[item]

