import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import difflib
import json

categories = ("baking tray", "ball", "blender", "bottle", "bowl", "box", "can", "chopping board", "clamp",
              "coffee maker", "cylinder", "dice", "drill", "food box", "fork", "fruit", "glass", "hammer",
              "kettle", "knife", "lego", "mug", "pan", "pen", "pill", "plate", "pot", "scissors", "screwdriver",
              "soda can", "spatula", "spoon", "thermos", "toaster", "wineglass", "wrench")

materials = ('ceramic', 'glass', 'metal', 'other', 'paper', 'plastic', 'water', 'wood')

global_xy = list()
global_categories = list()
global_materials = list()
final_dict = dict()


def get_cat_mat(cat_mat_str):
    cat_mat_split = cat_mat_str.split(" ")
    if len(cat_mat_split) > 2:
        # soda can metal -> ("soda can", metal)
        cat_fragments = cat_mat_split[0:len(cat_mat_split) - 1]
        category = ""
        for frag in cat_fragments:
            category += frag + " "
        category = category[0:len(category) - 1]
        cat_mat_split = (category, cat_mat_split[-1])
    return cat_mat_split


def on_press(event):

    # print('press', event.key)
    # sys.stdout.flush()
    new_str = ""
    if event.key == "backspace" and len(on_press.current_str) > 0:
        new_str = on_press.current_str[0:len(on_press.current_str)-1]
    else:
        new_str = on_press.current_str + (event.key if len(event.key) == 1 else "")
    on_press.current_str = new_str
    if event.key == "ctrl+n":
        if len(global_xy) == len(global_categories):
            # open next image
            # print(list(zip(global_xy, global_categories, global_materials)))
            final_dict[on_press.file_names[on_press.current_index]] = list(zip(global_xy, global_categories, global_materials))
            dict_yo = dict()
            dict_yo[on_press.file_names[on_press.current_index]] = list(zip(global_xy, global_categories, global_materials))

            if len(global_xy) > 0:
                with open(os.path.join(pred_dir, f"test_annotation{on_press.current_index}.json"), "w") as f:
                    json.dump(dict_yo, f)

            global_xy.clear()
            global_categories.clear()
            global_materials.clear()

            on_press.current_index += 1
            if not (on_press.current_index == len(on_press.file_names)):
                with Image.open(os.path.join(pred_dir, on_press.file_names[on_press.current_index])) as im:
                    ax.imshow(im)
                    plt.show()
        else:
            if len(global_xy) < len(global_categories):
                print("Missing xy point for", global_categories[-1], global_materials[:-1])
            else:
                print("Missing category and material for xy", global_xy[-1])

    if event.key == "enter":
        # print(on_press.current_str)
        # print(on_press.current_str.split(" "))
        # print(on_press.current_str.split())
        cat, mat = get_cat_mat(on_press.current_str)
        if cat not in categories:
            print(cat, "not in categories, try again! Closest matches:", difflib.get_close_matches(cat, categories))
        if mat not in materials:
            print(mat, "not in materials, try again! Closest matches:", difflib.get_close_matches(mat, materials))
        print("cat:", cat)
        print("mat:", mat)
        global_categories.append(cat)
        global_materials.append(mat)
        on_press.current_str = ""
        # print(cat, mat)
    print(on_press.current_str)
    # print(global_var)


def on_click(event):
    global_xy.append((event.xdata, event.ydata))
    print(event.xdata, event.ydata)


# Fixing random state for reproducibility
np.random.seed(19680801)
fig, ax = plt.subplots()
on_press.current_str = ""
on_press.current_index = 0
on_press.file_names = []
# pred_dir = "../square_images"
pred_dir = "../TEST"
select_every_nth = 10
for (dirpath, dirnames, filenames) in os.walk(pred_dir):
    image_files = [_ for _ in filenames if ".jpg" in _ or ".png" in _]  # select jpg and pngs
    selected_image_files = list()
    if select_every_nth > 1:
        for i in range(0, len(image_files), select_every_nth):
            selected_image_files.append(image_files[i])
    else:
        selected_image_files = image_files
    print("number of images selected:", len(selected_image_files))
    on_press.file_names.extend(selected_image_files)

fig.canvas.mpl_connect('key_press_event', on_press)
fig.canvas.mpl_connect('button_press_event', on_click)

# ax.plot(np.random.rand(12), np.random.rand(12), 'go')
xl = ax.set_xlabel("L-click to set x,y. Then type \"category material\" then enter to submit. E.g. \"spoon metal\".")
yl = ax.set_ylabel("ctrl+n: next image")
ax.set_title('Point annotator')
fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)

with Image.open(pred_dir + "\\" + on_press.file_names[on_press.current_index]) as im:
    ax.imshow(im)
    plt.show()
# plt.show()
"""
          'keymap.all_axes': ['a'],
          'keymap.back': ['left', 'c', 'backspace', 'MouseButton.BACK'],
          'keymap.copy': ['ctrl+c', 'cmd+c'],
          'keymap.forward': ['right', 'v', 'MouseButton.FORWARD'],
          'keymap.fullscreen': ['f', 'ctrl+f'],
          'keymap.grid': ['g'],
          'keymap.grid_minor': ['G'],
          'keymap.help': ['f1'],
          'keymap.home': ['h', 'r', 'home'],
          'keymap.pan': ['p'],
          'keymap.quit': ['ctrl+w', 'cmd+w', 'q'],
          'keymap.quit_all': [],
          'keymap.save': ['s', 'ctrl+s'],
          'keymap.xscale': ['k', 'L'],
          'keymap.yscale': ['l'],
          'keymap.zoom': ['o'],
"""
