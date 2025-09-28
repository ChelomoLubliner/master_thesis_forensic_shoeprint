import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from globals import FOLDER, W, H, PROCESSING_DATA_PATH, LOCATIONS, LOCATIONS_HAS_HEADER, LOCATIONS_SEPARATOR, LOCATIONS_SCALE_FACTOR, DATA_PATH, SHARED_DATA_PATH
import numpy as np
import pandas as pd
import math
import os
from PIL import Image


# Create output directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_output_dir = os.path.join(project_root, f"{FOLDER.strip('../')}RAC_html")
os.makedirs(html_output_dir, exist_ok=True)

"""
aspix_x converts the x coordinate to the x pixel
INPUT:
======
x - the x coordinate
col_shoe - the number of columns in each shoe
rel_col_shoe -the number of relevant columns 
  #out of the 307 columns only 150 are relevant (contain non zero pixels in some shoes)
rel_x_cord - the relevant coordintes 
 (using coordinates as in the locations_data.CSV file. The relevant x coordinates are between -.25 and 0.25)
"""
def aspix_x(x, rel_col_shoe=150, rel_x_cord=0.25):
    not_rel_col = math.ceil((W - rel_col_shoe) / 2)
    delx = (2 * rel_x_cord) / rel_col_shoe
    temp = ((x + rel_x_cord) / delx).apply(lambda x: math.floor(x)) + not_rel_col
    pix_x = W - temp
    return pix_x

def aspix_y(y, rel_row_shoe=300, rel_Y_cord=0.5):
    not_rel_row = math.ceil((H - rel_row_shoe) / 2)
    dely = (2 * rel_Y_cord) / rel_row_shoe
    temp = ((y + rel_Y_cord) / dely).apply(lambda x: math.floor(x)) + not_rel_row
    pix_y = H - temp
    return pix_y

def init_locations_new():
    import os
    locations_file = os.path.join(DATA_PATH, LOCATIONS)
    if LOCATIONS_HAS_HEADER:
        locations = pd.read_csv(locations_file, sep=LOCATIONS_SEPARATOR)
    else:
        locations = pd.read_csv(locations_file, sep=LOCATIONS_SEPARATOR, header=None)
        locations = locations[[1,2,3,4,5]]
        locations.columns = ["shoe","rac_num","x","y","type"]

    # Apply scaling factor if needed
    if LOCATIONS_SCALE_FACTOR != 1.0:
        locations['x'] = locations['x'] / LOCATIONS_SCALE_FACTOR
        locations['y'] = locations['y'] / LOCATIONS_SCALE_FACTOR

    locations['shoe'] = locations['shoe'] -1
    new_cols = {'COL':  aspix_x(locations['x']),
                'ROW': aspix_y(locations['y']),
                'INSIDE_SNAKE': np.nan,
                'HORIZ_DIST_SNAKE': np.nan,
                'DIST_SNAKE': np.nan}
    locations = pd.concat([locations, pd.DataFrame(new_cols)], axis=1)
    """
    locations['COL'] = round((locations['x'] * PIXEL_SIZE) + col0_old)
    locations['ROW'] = round((locations['y'] * PIXEL_SIZE) + row0_old)
    col0_old = math.floor(W / 2)
    row0_old = math.floor(H / 2)
    locations[['COL', 'ROW']] = locations[['COL', 'ROW']].astype(int)
    """
    import os
    locations.to_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'), index=False)

def save_html(total_df, shoe_num):
    """Plot fig"""
    scatter = go.Scatter(x=total_df['ROW'].to_list(), y=total_df['COL'].to_list(), mode='markers')
    fig = go.Figure(data=scatter)

    # Use the already created html_output_dir
    output_file = os.path.join(html_output_dir, f'plot_cont_{shoe_num}.html')
    pyo.plot(fig, filename=output_file, auto_open=False)
    
    """Save Image"""
    new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*total_df.values))] = True
    new_image = Image.fromarray(new_arr)
    #new_image.show()
    #new_image.save(f'{FOLDER}Distance_Extremities/plot_cont_{shoe_num}.png')

def shortest_distance(shoe_df,shoe_num, locations_all, algo):
    """"Check if is inside"""
    for index, rac in locations_all[locations_all['shoe']==shoe_num].iterrows():
        df2 = shoe_df.copy()
        distance_list = []
        for _, shoe in df2.iterrows():
            distance_list.append(round(math.dist([rac['COL'], rac['ROW']], [shoe['COL'], shoe['ROW']]),0))
        locations_all.at[index, f'DIST_{algo}'] = min(distance_list)

    locations_all.to_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'), index=False)

def horiz_distance(shoe_df,shoe_num, locations_all, algo):
    """"Check if is inside"""
    for index, row in locations_all[locations_all['shoe']==shoe_num].iterrows():
        df2 = shoe_df[shoe_df['ROW'] == row['ROW']]
        if (df2.shape[0] < 2):
            locations_all.at[index, f'INSIDE_{algo}'] = False
        else:
            distance_list = []
            for _, row2 in df2.iterrows():
                distance_list.append(row2['COL'] -row['COL'])
            distance_list = sorted(distance_list, key=abs)
            distance_list_new = [distance_list[0]]
            for i in range(1,len(distance_list)):
                if abs(distance_list[i-1] - distance_list[i]) != 1:
                    distance_list_new.append(distance_list[i])
            if(len(distance_list_new) <2 ): distance_list_new.append(distance_list[1])
            d1 = distance_list_new[0]
            d2 = distance_list_new[1]
            if (d1 * d2 <= 0) | (d1==0):
                locations_all.at[index, f'INSIDE_{algo}'] = True
            else:
                locations_all.at[index, f'INSIDE_{algo}'] = False
            locations_all.at[index, f'HORIZ_DIST_{algo}'] = abs(d1)
    locations_all.to_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'), index=False)



def dist_per_shoe(shoe_arr, shoe_num, algo ):
    locations_all = pd.read_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'))
    locations = locations_all[locations_all['shoe']==shoe_num]
    locations_coord = list(zip(locations['ROW'].to_list(), locations['COL'].to_list()))
    shoe_coord = list(np.argwhere(shoe_arr[shoe_num] == True))
    shoe_df = pd.DataFrame(shoe_coord, columns = ['ROW', 'COL'])
    total_df = pd.DataFrame(locations_coord + shoe_coord, columns=['ROW', 'COL'])

    shortest_distance(shoe_df,shoe_num, locations_all, algo)
    horiz_distance(shoe_df, shoe_num, locations_all, algo)
    save_html(total_df, shoe_num)

def set_outside_to_0():
    df = pd.read_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'))
    for index, row in df[df[f'INSIDE_SNAKE']==False][[f'HORIZ_DIST_SNAKE', f'DIST_SNAKE']].iterrows():
        if row[f'HORIZ_DIST_SNAKE'] is not None : df.loc[index, f'HORIZ_DIST_SNAKE'] = 0
        if row[f'DIST_SNAKE'] is not None : df.loc[index,f'DIST_SNAKE'] = 0
    df.to_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'), index=False)

def main():
    print(f"distance_extremities_main")
    init_locations_new()
    list_snake = list(np.load(f'{PROCESSING_DATA_PATH}active_contour_all.npy'))
    for i in tqdm(range(len(list_snake))):#len(list_snake))
        dist_per_shoe(list_snake, i, 'SNAKE') 
    set_outside_to_0()

if __name__ == '__main__':  
    main()