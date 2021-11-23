import numpy as np
import cv2
import os

pred_dir = "../test_images_ipalm"
file_names = []
for (dirpath, dirnames, filenames) in os.walk(pred_dir):
    file_names.extend(filenames)

new_dir = "../square_images"
if not os.path.isdir(new_dir):
    os.makedirs(new_dir)

for file_name in file_names:
    # print(file_name)
    im = cv2.imread(os.path.join(pred_dir, file_name))
    # print(type(im))
    h = len(im)
    w = len(im[0])
    dx = h - w
    if dx > 0:  # keep width
        im = im[dx//2:h - dx//2, 0:w]
    else:
        im = im[0:h, -dx//2:w + dx//2]
    # print(im.shape)
    dst = np.array([])
    im = cv2.resize(im, (1000, 1000))
    cv2.imwrite(os.path.join(new_dir, file_name), im)
    # print(im.shape)
    # cv2.imshow("smaller image", im)
    # cv2.waitKey(0)  # waits until a key is pressed
    # cv2.destroyAllWindows()  # destroys the window showing image

    # exit()
