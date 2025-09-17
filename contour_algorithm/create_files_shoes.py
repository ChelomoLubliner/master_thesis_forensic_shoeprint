import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from PIL import Image
my_dict = {1: True, 0: False}
import cv2
from globals import  FOLDER, DATASET, W, H, PROCESSING_DATA_PATH
from active_contour_snake import active_contour_on_prototype


# Opened file, save list_lines, and images
def contacts_data():
    list_lines = []
    with open(f'../Data/{DATASET}', 'r') as f:
        lines = f.readlines()
        print('Total lines:', len(lines))
        for i in tqdm(range(len(lines))):
            line = list(lines[i])
            line = np.array(list(map(int, line[:-1]))).reshape(H, W)
            line = np.vectorize(my_dict.get)(line)
            list_lines.append(np.matrix(line)   )
            # img = Image.fromarray(line)
            # img.save(f'{FOLDER}Shoes/im{i}.png')
        # flip the image8 because it's left shoes
        if FOLDER == 'Images/Old_Shoes/':
            list_lines[8] = np.fliplr(list_lines[8])
            line = np.vectorize(my_dict.get)(list_lines[8])
            # im8 = Image.fromarray(line)
            # im8.save(f'{FOLDER}Shoes/im8.png')
        # save list_lines
        np.save(f'{PROCESSING_DATA_PATH}list_matrices.npy', list_lines)



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
            Image.fromarray(line.astype(np.uint8) * 255).save(PROCESSING_DATA_PATH + 'old_freq_min_18.png')
            break
        
       


def create_cleaned_shoes():
    """Create cleaned shoe images for statistical analysis"""
    print("Creating cleaned shoe images...")
    import os
    os.makedirs(f'{FOLDER}Cleaned_Shoes', exist_ok=True)

    # Load original matrices and create cleaned versions
    list_lines = np.load(f'{PROCESSING_DATA_PATH}list_matrices.npy')

    for i in tqdm(range(len(list_lines))):
        # Convert matrix to image
        line = np.array(list_lines[i], dtype=bool)
        img = Image.fromarray((line * 255).astype(np.uint8))
        img.save(f'{FOLDER}Cleaned_Shoes/im_{i}.png')

    print(f"Created {len(list_lines)} cleaned shoe images")

def main():
    print(f"main_create_files_init")
    contacts_data()
    list_lines = np.load(f'{PROCESSING_DATA_PATH}list_matrices.npy')
    len_lines = len(list_lines)
    print(f'Array of {len_lines} lines')
    superposed_pixels(list_lines)
    create_cleaned_shoes()
    active_contour_on_prototype()


#def main_create_files_init():
if __name__ ==  '__main__':
    main()

