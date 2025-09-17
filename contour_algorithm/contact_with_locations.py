import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from globals import FOLDER, W, H, LOCATIONS, PROCESSING_DATA_PATH
import numpy as np
import pandas as pd
import math
from PIL import Image
import warnings
import cv2
# Ignore FutureWarnings globally
warnings.simplefilter(action='ignore', category=FutureWarning)
def save_html(total_df, shoe_num) :
    """Plot fig"""

    scatter = go.Scatter(x=total_df['ROW'].to_list(), y=total_df['COL'].to_list(), mode='markers')
    fig = go.Figure(data=scatter)
    pyo.plot(fig, filename=f'{FOLDER}Shoes_RAC/plot_cont_{shoe_num}.html',auto_open=False)

    """Save Image"""
    """new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*total))] = True
    new_image = Image.fromarray(new_arr)
    new_image.show()"""





def dist_per_shoe(image_i, shoe_num ):
    locations_all = pd.read_csv(f'../shared_data/locations_new.csv')
    locations = locations_all[locations_all['shoe']==shoe_num]
    locations_coord = list(zip(locations['ROW'].to_list(), locations['COL'].to_list()))
    biggest_locations_coord = []
    for loc in locations_coord:
        biggest_locations_coord.extend([loc, (loc[0]+1,loc[1]),(loc[0]-1,loc[1]),(loc[0],loc[1]+1),(loc[0],loc[1]-1)])
    new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*biggest_locations_coord))] = True
    locations_img = np.zeros((H, W, 3), dtype=np.uint8)
    locations_img[new_arr] = [0, 0, 255]
    condition = np.all(locations_img == [0, 0, 255], axis=-1)
    result_array = np.where(condition[..., np.newaxis], locations_img, image_i)
    new_image = Image.fromarray(cv2.cvtColor(result_array, cv2.COLOR_BGR2RGB))
    new_image.save(f'{FOLDER}Shoes_RAC/im_{shoe_num}.png')


def set_outside_to_0():
    df = pd.read_csv(f'../shared_data/locations_new.csv')
    for alg in ['SNAKE', 'CONV']:
        for index, row in df[df[f'INSIDE_{alg}']==False][[f'HORIZ_DIST_{alg}', f'DIST_{alg}']].iterrows():
            if row[f'HORIZ_DIST_{alg}'] is not None : df.loc[index, f'HORIZ_DIST_{alg}'] = 0
            if row[f'DIST_{alg}'] is not None : df.loc[index,f'DIST_{alg}'] = 0
    df.to_csv(f'../shared_data/locations_new.csv', index=False)

def main():
    print(f"{FOLDER.split('/')[1]}\ncontact_with_locations_main")
    #init_locations_new()
    list_contour = list(np.load(f'{PROCESSING_DATA_PATH}list_contour.npy'))
    for i in tqdm(range(10)):#len(list_contour))
        image_i = cv2.imread(f'{FOLDER}Cleaned_Shoes/im_{i}.png')
        dist_per_shoe(image_i, i)
    #set_outside_to_0()

if __name__ == '__main__':
    main()