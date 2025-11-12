import numpy as np

def dict_points(all_points, x_true):
    points = all_points
    points_dict = {}
    for x_i, y_i in points:
        if x_true:
            if x_i not in points_dict:
                points_dict[x_i] = [y_i]
            else:
                points_dict[x_i].append(y_i)
        else :
            if y_i not in points_dict:
                points_dict[y_i] = [x_i]
            else:
                points_dict[y_i].append(x_i)
    return points_dict


# iterate over every X and take the first and last y pixel for each x
def select_min_max_x(all_points):
    points_dict = dict_points(all_points,x_true=True)
    new_points_x = []
    for x_i in points_dict.keys():
        points_dict[x_i] = min(points_dict[x_i]), max(points_dict[x_i])
        for new_y_i in points_dict[x_i]:
            new_points_x.append((x_i, new_y_i))
    return new_points_x


# iterate over every Y and take the first and last X pixel for each Y
# this is essential to run both on x-axis and y-axis because there are some lines
# (horizontally or vertically that could be deleted)
def select_min_max_y(all_points):
    points_dict = dict_points(all_points,x_true=False)
    new_points_y = []
    for y_i in points_dict.keys():
        points_dict[y_i] = min(points_dict[y_i]), max(points_dict[y_i])
        for new_x_i in points_dict[y_i]:
            new_points_y.append((new_x_i, y_i))
    return new_points_y


# this algorithm receive a list of points, select_min_max_x/y
# union them (most points would be duplicated)
# return a list of point
def get_contour(im_array):
    all_points = np.argwhere(im_array == True)
    new_points_x = select_min_max_x(all_points)
    new_points_y = select_min_max_y(all_points)
    final_points = list(set().union(new_points_x, new_points_y))
    return final_points
