import numpy as np
from tqdm import tqdm
from PIL import Image
from globals import FOLDER, W, H, PROCESSING_DATA_PATH
from extreme_values_x_y import get_contour
"""
This file processes contours and includes noise removal functions
"""

def save_cleaned_shoes(list_matrices, im_num):
    """Delete every pixel that isn't in the prototype shoe (bitwise_and)"""
    contour = np.load(f'{PROCESSING_DATA_PATH}freq_min_18.npy')
    combined_arr = np.bitwise_and(list_matrices[im_num], contour)
    combined_image = Image.fromarray(combined_arr)
    combined_image.save(f'{FOLDER}Cleaned_Shoes/im_{im_num}.png')
    return combined_arr



def save_new_contour_shoe(new_points, im_num):
    new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*new_points))] = True
    return new_arr


# this is a complete flow for an image
def remove_noise_get_contour(list_matrices, im_num):
    new_im = save_cleaned_shoes(list_matrices, im_num)
    new_points = get_contour(new_im)
    return save_new_contour_shoe(new_points, im_num)

def main():
    print(f"main_remove_noise_get_extreme_values")
    list_lines = np.load(f'{PROCESSING_DATA_PATH}list_matrices.npy')
    list_contour = []
    for i in tqdm(range(len(list_lines))):
        contour_item = remove_noise_get_contour(list_lines, i)
        list_contour.append(np.matrix(contour_item))
        np.save(f'{PROCESSING_DATA_PATH}list_contour.npy', list_contour)

if __name__ == '__main__':
    main()



