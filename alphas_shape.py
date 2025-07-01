import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from globals import FOLDER, W, H
import numpy as np
from PIL import Image, ImageDraw
import alphashape
from skimage import img_as_ubyte, measure
import io
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon



def get_image(entire_shoe, im_num,list_contour):
    img = np.nan
    if entire_shoe:
        img = img_as_ubyte(Image.open(f'{FOLDER}Cleaned_Shoes/im_{im_num}.png'))
    else:
        img = img_as_ubyte(Image.fromarray(list_contour[im_num]))
    return img



def save_img(original_img, temporal_arr, final_arr, alpha,sec_alpha, im_num):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(original_img, cmap=plt.cm.gray)

    # temporal masque (optionnel) : temporal_arr en bleu
    if temporal_arr is not None:
        temp_contours = measure.find_contours(temporal_arr, level=0.5)
        for contour in temp_contours:
            ax.plot(contour[:, 1], contour[:, 0], color='blue', lw=3)


    if final_arr is not None:
        contours = measure.find_contours(final_arr, level=0.5)
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], color='red', lw=3)


    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis([0, original_img.shape[1], original_img.shape[0], 0])

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close('all')
    img = Image.open(buf)
    if final_arr is not None:
        img.save(f'{FOLDER}Alpha_Shape/im_{im_num}_al_{alpha}_sec_al_{sec_alpha}.png')
    else:
        img.save(f'{FOLDER}Alpha_Shape/im_{im_num}_al_{alpha}.png')

def alpha_func(points, alpha):
    shape = alphashape.alphashape(points, alpha)
    image = Image.new('1', (W, H), color=0)
    draw = ImageDraw.Draw(image)

    if isinstance(shape, Polygon):
        draw_polygon(shape, draw)
    elif isinstance(shape, MultiPolygon):
        for poly in shape.geoms:
            draw_polygon(poly, draw)
    new_points = np.argwhere(np.array(image, dtype=bool) == True)
    return new_points, image

def get_alpha_shape_mask(list_contour, im_num, alpha, second_alpha):
    original_img = get_image(True, im_num, list_contour)
    original_points = np.argwhere(original_img > 0)
    final_arr = np.zeros((H, W), dtype=bool)
    first_tep_arr = np.zeros((H, W), dtype=bool)
    first_step_points, new_image = alpha_func(original_points, alpha)
    first_tep_arr[tuple(zip(*list(first_step_points)))] = True
    for sec_alpha in [0.01]:
        final_points, final_image = alpha_func(first_step_points, alpha=sec_alpha)
        final_arr[tuple(zip(*list(final_points)))] = True
        save_img(original_img, first_tep_arr, final_arr,alpha, sec_alpha, im_num)
        #save_img(original_img, first_tep_arr, None, alpha, '', im_num)
    return None#(np.array(final_image, dtype=bool) == True)

def draw_polygon(polygon, draw):
        coords = [(int(y), int(x)) for x, y in polygon.exterior.coords]
        draw.line(coords + [coords[0]], fill=1, width=1)

# def get_alpha_shape_html(points, im_num, alpha=5.0):
#     shape = alphashape.alphashape(points, alpha)
#     scatter_trace = go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers')
#     line_traces = []
#
#     def shape_to_traces(geom):
#         coords = np.array(geom.exterior.coords)
#         return go.Scatter(x=coords[:, 0], y=coords[:, 1], mode='lines')
#
#     if isinstance(shape, Polygon):
#         line_traces.append(shape_to_traces(shape))
#     elif isinstance(shape, MultiPolygon):
#         for poly in shape.geoms:
#             line_traces.append(shape_to_traces(poly))
#
#     fig = go.Figure(data=[scatter_trace] + line_traces)
#     pyo.plot(fig, filename=f'{FOLDER}Alpha_Shape_html/plot_cont_{im_num}.html', auto_open=False)

def main():
    print(f"{FOLDER.split('/')[1]}\nmain_Alpha_Shape")
    list_contour = np.load(f'{FOLDER}Saved/list_contour.npy')
    alpha_all = []
    for i in tqdm(range(40)):#len(list_contour)
        all_points = np.argwhere(list_contour[i] == True)
        #get_alpha_shape_html(all_points, i)
        alpha_arr = get_alpha_shape_mask(all_points, i,0.02, second_alpha=0.15)
        #get_alpha_shape_mask(all_points, i, 0.5, 0.15)
        # get_alpha_shape_mask(all_points, i, 0.5)
        alpha_all.append(np.matrix(alpha_arr))
    print(len(alpha_all))
    #np.save(f'{FOLDER}Saved/alpha_all.npy', alpha_all)

if __name__ == '__main__':
    main()
