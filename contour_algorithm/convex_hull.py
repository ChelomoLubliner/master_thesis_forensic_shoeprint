import plotly.graph_objs as go
import plotly.offline as pyo
from tqdm import tqdm
from scipy.spatial import ConvexHull
from globals import FOLDER, W, H
import numpy as np
from PIL import Image, ImageDraw


def get_convex_plotly(points, im_num):
    hull = ConvexHull(points)
    image = Image.new('1', (W, H), color=0)
    draw = ImageDraw.Draw(image)
    for simplex in hull.simplices:
        draw.line([(points[simplex[0]][1], points[simplex[0]][0]),(points[simplex[1]][1], points[simplex[1]][0])], fill=True)
    convex_arr = list(np.argwhere(np.array(image, dtype=bool) == True))
    shoe_arr = list(points)
    new_points = shoe_arr +convex_arr
    final_arr = np.zeros((H, W), dtype=bool)
    final_arr[tuple(zip(*new_points))] = True
    final_img = Image.fromarray(final_arr)
    final_img.save(f'{FOLDER}Convex_Hull/im_{im_num}.png')
    return (np.array(image, dtype=bool) == True)

def get_convex_plotly_html(points, im_num):
    hull = ConvexHull(points)
    scatter_trace = go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers')
    line_traces = []
    for simplex in hull.simplices:
        x = points[simplex, 0]
        y = points[simplex, 1]
        line_trace = go.Scatter(x=x, y=y, mode='lines')
        line_traces.append(line_trace)

    fig = go.Figure(data= line_traces)
    pyo.plot(fig, filename=f'{FOLDER}Convex_Hull_html/plot_cont_{im_num}.html',auto_open=False)


def main():
    print(f"{FOLDER.split('/')[1]}\nmain_convex_hull")
    list_contour = np.load(f'{FOLDER}Saved/list_contour.npy')
    convex_all = []
    for i in tqdm(range(len(list_contour))):
        all_points = np.argwhere(list_contour[i] == True)
        get_convex_plotly_html(all_points, i)
        convex_arr = get_convex_plotly(all_points, i)
        convex_all.append(np.matrix(convex_arr))
    print(len(convex_all))
    np.save(f'{FOLDER}Saved/convex_all.npy', convex_all)

if __name__ == '__main__':
    main()
