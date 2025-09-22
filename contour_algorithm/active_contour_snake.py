import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import img_as_ubyte
from PIL import Image
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import io
from tqdm import tqdm
from extreme_values_x_y import dict_points, get_contour
from globals import FOLDER, W, H, SNAKE_Y_CENTER, SNAKE_Y_RADIUS, SNAKE_X_CENTER, SNAKE_X_RADIUS, PROCESSING_DATA_PATH


def get_image(entire_shoe, im_num,list_contour):
    img = np.nan
    if entire_shoe:
        img = img_as_ubyte(Image.open(f'{FOLDER}Cleaned_Shoes/im_{im_num}.png'))
    else:
        img = img_as_ubyte(Image.fromarray(list_contour[im_num]))
    return img

def plot_active_contour(img,init, snake, im_num):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close('all')
    img = Image.open(buf)
    # img.show()
    #img.save(f'{FOLDER}Temp/im_{im_num}.png')


def save_img(img, snake, im_num):
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img, cmap=plt.cm.gray)
    #ax.plot(init[:, 1], init[:, 0], '--r', lw=3)
    ax.plot(snake[:, 1], snake[:, 0], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, img.shape[1], img.shape[0], 0])
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close('all')
    img = Image.open(buf)
    img.save(f'{FOLDER}Active_Contour/im_{im_num}.png')

def init_snake():
    s = np.linspace(0, 2 * np.pi, 400)
    y = SNAKE_Y_CENTER + SNAKE_Y_RADIUS * np.sin(s)
    x = SNAKE_X_CENTER + SNAKE_X_RADIUS * np.cos(s)
    init = np.array([y, x]).T
    return init


def extreme_values(im_arr):
    all_points = np.argwhere(im_arr == True)
    points_dict = dict_points(all_points,x_true=True)
    new_points_x = []
    #print(all_points)
    for x_i in points_dict.keys():
        max_x = max(points_dict[x_i])+1
        min_x = min(points_dict[x_i])
        diff_min_max = max_x - min_x
        if diff_min_max > 3:
            to_add = min(int(diff_min_max/2),3)
            min_x += to_add
            max_x -= to_add
        for new_y_i in range(min_x, max_x):
            new_points_x.append((x_i, new_y_i))
    new_arr = np.zeros((H, W), dtype=bool)
    new_arr[tuple(zip(*new_points_x))] = True
    new_image = Image.fromarray(new_arr)

    img_thresholded = new_image.point(lambda x: 255 if x ==0 else 0)
    return img_thresholded


def get_snake_image(snake):
    # create a blank image of the same size as the input image
    output = np.zeros((W,H), dtype=np.uint8)
    # draw the initial contour in red and the snake in blue on the output image
    #cv2.polylines(output, [np.int32(init)], False, (0, 0, 255), thickness=3)
    cv2.polylines(output, [np.int32(snake)], False, 255, thickness=3)

    # convert the output image to PNG format
    png_bytes = cv2.imencode('.png', output)[1].tobytes()
    img = cv2.imdecode(np.frombuffer(png_bytes, np.uint8), cv2.IMREAD_UNCHANGED)
    img = cv2.transpose(img)
    return Image.fromarray(img.astype(bool))


def combined_snake_arr(snake, original_img):
    snake_img = get_snake_image(snake)
    snake_arr = np.array(snake_img, dtype=bool)
    first_snake_contour_arr = extreme_values(snake_arr)
    snake_arr = np.array(snake_img, dtype=bool)
    """Get the part of the shoe that is out of the first_snake"""
    out_first_snake_arr = np.bitwise_and(first_snake_contour_arr, np.array(original_img, dtype=bool))
    """Get a new image with extreme values of out_first_snake_arr and the original images

    Add out_first_snake_arr and first_snake_arr. Then we will calculate the extremes values"""
    new_first_comb_arr = np.add(out_first_snake_arr, snake_arr)
    comb_coordinates = get_contour(new_first_comb_arr)
    comb_arr = np.zeros((H, W), dtype=bool)
    comb_arr[tuple(zip(*comb_coordinates))] = True
    comb_extremes_img = Image.fromarray(comb_arr)
    return comb_extremes_img

#essayer de garder la grnde figure mais de faire un border content et comme ca on bloque
def active_contour_shoe(list_contour, plot_img,save_img_bool, im_num):
    """Get Img (entire or only contour)"""
    original_img = get_image(True, im_num, list_contour)
    """First active-contour : beta=10"""
    init = init_snake()
    first_snake = active_contour(gaussian(original_img, 3, preserve_range=False), init, alpha=0.015, beta=10, gamma=0.001)
    if plot_img: plot_active_contour(original_img, init, first_snake,im_num)
    """Get a new image with extreme values of out_first_snake_arr and the original images
        Add out_first_snake_arr and first_snake_arr. Then we will calculate the extremes values"""
    comb_extremes_img = combined_snake_arr(first_snake, original_img)
    """Do second snake on comb_extremes_img"""
    second_snake = active_contour(gaussian(img_as_ubyte(comb_extremes_img), 3, preserve_range=False), init, alpha=0.015, beta=0.10, gamma=0.001)

    if save_img_bool: save_img(original_img, second_snake, im_num)
    if plot_img: plot_active_contour(img_as_ubyte(comb_extremes_img), init,second_snake, im_num)
    if plot_img: plot_active_contour(original_img,init,  second_snake, im_num)
    snake_img = get_snake_image(second_snake)
    snake_arr = np.array(snake_img, dtype=bool)
    comb_coordinates = get_contour(snake_arr)
    comb_arr = np.zeros((H, W), dtype=bool)
    comb_arr[tuple(zip(*comb_coordinates))] = True
    return comb_arr


def active_contour_on_prototype():
    """Create cleaned prototype image using dual-stage active contour"""
    print("Creating cleaned prototype image...")

    original_img = img_as_ubyte(Image.open(f'{PROCESSING_DATA_PATH}old_freq_min_18.png'))
    init = init_snake()

    # First snake with beta=10 for rough boundary detection
    first_snake = active_contour(gaussian(original_img, 3, preserve_range=False), init,
                                alpha=0.015, beta=10, gamma=0.001)

    # Create combined extremes image for second stage
    comb_extremes_img = combined_snake_arr(first_snake, original_img)

    # Second snake with beta=0.10 for refined boundary
    second_snake = active_contour(gaussian(img_as_ubyte(comb_extremes_img), 3, preserve_range=False), init,
                                 alpha=0.015, beta=0.10, gamma=0.001)

    # Create final cleaned image
    snake_img = get_snake_image(second_snake)
    snake_arr = np.array(snake_img, dtype=bool)
    final_arr = ~np.array(extreme_values(snake_arr), dtype=bool)

    # Save cleaned prototype
    final_img = Image.fromarray(final_arr.astype(np.uint8) * 255)
    final_img.save(f'{PROCESSING_DATA_PATH}freq_min_18.png')
    np.save(f'{PROCESSING_DATA_PATH}freq_min_18.npy', final_arr)

    print("Cleaned prototype image created successfully")
    return final_arr

def main():
    print(f"active_contour_snake")

    # Create Active-contour directory for cleaned images
    import os
    os.makedirs(f'{FOLDER}Active_Contour', exist_ok=True)

    list_contour = np.load(f'{PROCESSING_DATA_PATH}list_contour.npy')
    snake_all = []
    for i in tqdm(range(len(list_contour))):#len(list_contour))
        snake_arr = active_contour_shoe(list_contour, plot_img=False, save_img_bool=True, im_num=i)
        snake_all.append(snake_arr)
    np.save(f'{PROCESSING_DATA_PATH}active_contour_all.npy', snake_all)
    print("Active contour processing complete - cleaned images saved to Active-contour folder")

if __name__ == '__main__':
    main()
    snake_all = []
    list_contour = np.load(f'{PROCESSING_DATA_PATH}list_contour.npy')
   #snake_arr = active_contour_shoe(list_contour, plot_img=True, save_img_bool=True, im_num=555)
   #Image.fromarray(snake_arr).save(PROCESSING_DATA_PATH + 'test_135.png')
