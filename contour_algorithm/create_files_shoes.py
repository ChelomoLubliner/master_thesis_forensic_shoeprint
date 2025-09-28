import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image
my_dict = {1: True, 0: False}
import cv2
import os
from globals import FOLDER, DATASET, W, H, DATA_PATH, SHARED_DATA_PATH,IMAGES_PATH
from active_contour_snake import active_contour_on_prototype


# Opened file, save list_lines, and images
def contacts_data():
    list_lines = []
    with open(os.path.join(DATA_PATH, DATASET), 'r') as f:
        lines = f.readlines()
        print('Total lines:', len(lines))
        for i in tqdm(range(len(lines))):
            line = list(lines[i])
            line = np.array(list(map(int, line[:-1]))).reshape(H, W)
            line = np.vectorize(my_dict.get)(line)
            list_lines.append(np.matrix(line)   )
            img = Image.fromarray(line)
            img.save(os.path.join(IMAGES_PATH, 'Shoes', f'im{i}.png'))
        # flip the image8 because it's left shoes
        if FOLDER == 'Images/Old_Shoes/':
            list_lines[8] = np.fliplr(list_lines[8])
            line = np.vectorize(my_dict.get)(list_lines[8])
            im8 = Image.fromarray(line)
            im8.save(os.path.join(SHARED_DATA_PATH, 'Shoes', 'im8.png'))
        # save list_lines
        np.save(os.path.join(SHARED_DATA_PATH, 'list_matrices.npy'), list_lines)

def superposition_all_shoes(list_lines):
    print('superposition_all_shoes')
    total = list_lines.sum(axis=0)
    Image.fromarray(total.astype(bool)).save(os.path.join(SHARED_DATA_PATH, 'all_shoes_superposed.png'))


def superposed_pixels(list_lines):
    print('Superposed_pixels')
    # Dict to convert 0->False and non 0->True
    new_dict = {0: False}
    # max_pixel occurrence
    # total = superposed pixels
    total = list_lines.sum(axis=0)
    max_pixel = total.max()
    for max_pix in tqdm(range(max_pixel, 0, -1)):  # -1 -1
        new_dict[max_pix] = True
        line = np.vectorize(new_dict.get)(total)
        if max_pix == 18:
            np.save(os.path.join(SHARED_DATA_PATH, 'freq_min_18.npy'), line)
            Image.fromarray(line).save(os.path.join(SHARED_DATA_PATH, 'freq_min_18.png'))
            Image.fromarray(line).save(os.path.join(SHARED_DATA_PATH, 'old_freq_min_18.png'))
        if (max_pix % 10 == 0) | (max_pix < 25):
            img = Image.fromarray(line)
            img.save(os.path.join(IMAGES_PATH, 'Superposed_Pixels', f'old_freq_min_{max_pix}.png'))

def superposed_pixels_reversed(list_lines):
    # Dict to convert 0->False and non 0->True
    print('Superposed_pixels_reversed')
    new_dict = {0: False}
    total = list_lines.sum(axis=0)
    max_pixel = total.max()
    for max_pix in tqdm(range(1, max_pixel)):  # -1 -1
        new_dict[max_pix] = True
        line = np.vectorize(new_dict.get)(total)
        if (max_pix % 10 == 0) | (max_pix < 25):
            img = Image.fromarray(line)
            img.save(os.path.join(IMAGES_PATH, 'Superposed_Pixels_Reversed', f'freq_max_{max_pix}.png'))

def heatmap_superposed(list_lines):
    print('Heatmap_superposed')
    plt.imshow(list_lines.sum(axis=0), cmap='jet', interpolation='sinc')
    plt.savefig(os.path.join(SHARED_DATA_PATH, 'heatmap_superposed.png'))





def main():
    print(f"main_create_files_init")
    contacts_data()
    list_lines = np.load(os.path.join(SHARED_DATA_PATH, 'list_matrices.npy'))
    len_lines = len(list_lines)
    print(f'Array of {len_lines} lines')
    superposition_all_shoes(list_lines)
    superposed_pixels(list_lines)
    #superposed_pixels_reversed(list_lines)
    #heatmap_superposed(list_lines)
    #active_contour_on_prototype()


#def main_create_files_init():
if __name__ ==  '__main__':
    main()