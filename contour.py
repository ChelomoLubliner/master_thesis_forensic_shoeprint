import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from globals import PATH, FOLDER, W, H
from remove_noise import superpose_image_prototype, save_cleaned_shoes
from extreme_values_x_y import get_contour
"""
This file use remove_noise and extreme_values_x_y
"""


# get an array of coordinates (such as contour pixels)
# return a scatter plot of these points
def scatter_plot_contour(coordinates,im_num):
    x = np.array([coord[0] for coord in coordinates])
    y = np.array([coord[1] for coord in coordinates])
    trace = go.Scatter(x=x, y=y, mode='markers')
    layout = go.Layout(title='Scatter plot of contour Image '+str(im_num))
    fig = go.Figure(data=[trace], layout=layout)
    pyo.plot(fig, filename=PATH + FOLDER +f'Extreme_Values/plot_cont_{im_num}.html', auto_open=False)

def save_new_contour_shoe(new_points, im_num):
    new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*new_points))] = True
    return new_arr
    #new_image = Image.fromarray(new_arr)
    #new_image.save(PATH + FOLDER +f'Contour_Shoes/cont_im_{im_num}.png')


# this is a complete flow for an image
def remove_noise_get_contour(list_matrices, im_num):
    #Shoe_On_Prototype
    superpose_image_prototype(im_num)
    #Cleaned_Shoes
    new_im = save_cleaned_shoes(list_matrices, im_num)
    new_points = get_contour(new_im)
    #Extreme_values_html
    scatter_plot_contour(new_points, im_num)
    #Contour_Shoes
    return save_new_contour_shoe(new_points, im_num)

def main():
    print(f"{FOLDER.split('/')[1]}\nmain_remove_noise_get_extreme_values")
    list_lines = np.load(f'{PATH}{FOLDER}Saved/list_matrices.npy')
    list_contour = []
    for i in tqdm(range(len(list_lines))):
        contour_item = remove_noise_get_contour(list_lines, i)
        list_contour.append(np.matrix(contour_item))
        np.save(f'{PATH}{FOLDER}Saved/list_contour.npy', list_contour)

if __name__ == '__main__':
    main()



