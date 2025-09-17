import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from globals import FOLDER, W, H, LOCATIONS, PROCESSING_DATA_PATH, SHARED_DATA_PATH
import numpy as np
import pandas as pd
import math
from PIL import Image
import warnings
import cv2
import os
import glob
# Ignore FutureWarnings globally
warnings.simplefilter(action='ignore', category=FutureWarning)

# def save_html(total_df, shoe_num) :
#     """Plot fig"""

#     scatter = go.Scatter(x=total_df['ROW'].to_list(), y=total_df['COL'].to_list(), mode='markers')
#     fig = go.Figure(data=scatter)
#     pyo.plot(fig, filename=f'{FOLDER}Shoes_RAC/plot_cont_{shoe_num}.html',auto_open=False)

#     """Save Image"""
#     """new_arr = np.zeros((H, W), dtype=bool)
#     new_arr[tuple(zip(*total))] = True
#     new_image = Image.fromarray(new_arr)
#     new_image.show()"""





def dist_per_shoe(image_i, shoe_num ):
    import os
    locations_all = pd.read_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'))
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
    import os
    df = pd.read_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'))
    for alg in ['SNAKE']:
        for index, row in df[df[f'INSIDE_{alg}']==False][[f'HORIZ_DIST_{alg}', f'DIST_{alg}']].iterrows():
            if row[f'HORIZ_DIST_{alg}'] is not None : df.loc[index, f'HORIZ_DIST_{alg}'] = 0
            if row[f'DIST_{alg}'] is not None : df.loc[index,f'DIST_{alg}'] = 0
    import os
    df.to_csv(os.path.join(SHARED_DATA_PATH, 'locations_new.csv'), index=False)

def main():
    print(f"{FOLDER.split('/')[1]}\ncontact_with_locations_main")
    #init_locations_new()

    # Load contour data with robust error handling
    try:
        list_contour = list(np.load(f'{PROCESSING_DATA_PATH}list_contour.npy'))
        print(f"Loaded list_contour with {len(list_contour)} elements")
    except ValueError as e:
        print(f"Error loading list_contour.npy: {e}")
        # Try loading without shape constraint and reshape manually
        try:
            raw_data = np.load(f'{PROCESSING_DATA_PATH}list_contour.npy', allow_pickle=True)
            print(f"Raw data shape: {raw_data.shape}, size: {raw_data.size}")
            # Calculate actual dimensions based on file size
            actual_size = raw_data.size
            # Try different possible shapes
            for num_shoes in [355, 386, 387]:
                expected_size = num_shoes * H * W
                if abs(actual_size - expected_size) < 1000:  # Allow small difference
                    try:
                        list_contour = list(raw_data.reshape(num_shoes, H, W))
                        print(f"Successfully reshaped to ({num_shoes}, {H}, {W})")
                        break
                    except:
                        continue
            else:
                print("Could not determine correct shape, using available shoe images instead")
                # Fallback: count actual shoe images
                import glob
                shoe_files = glob.glob(f'{FOLDER}Cleaned_Shoes/im_*.png')
                list_contour = [None] * len(shoe_files)  # Dummy list
        except Exception as e2:
            print(f"Failed to load contour data: {e2}")
            print("Using fallback approach with available shoe images")
            import glob
            shoe_files = glob.glob(f'{FOLDER}Cleaned_Shoes/im_*.png')
            list_contour = [None] * len(shoe_files)  # Dummy list

    # Process available shoe images
    import glob
    shoe_files = glob.glob(f'{FOLDER}Cleaned_Shoes/im_*.png')
    available_shoes = [int(f.split('im_')[1].split('.png')[0]) for f in shoe_files]
    available_shoes = sorted(available_shoes)[:20]  # Limit to first 20 for testing

    for i in tqdm(available_shoes):
        image_path = f'{FOLDER}Cleaned_Shoes/im_{i}.png'
        if os.path.exists(image_path):
            image_i = cv2.imread(image_path)
            if image_i is not None:
                dist_per_shoe(image_i, i)
            else:
                print(f"Failed to load image: {image_path}")
    #set_outside_to_0()

if __name__ == '__main__':
    main()