import cv2
import numpy

import utils as u

path_to_bpm_dir = "./_detect/"
mask_file_name = "bad_pixels_mask.png"

DETECT_THRESHOLD = 10

def start():
    file_names = u.get_files_from_dir_with_ext(path_to_bpm_dir, ['jpg', 'jpeg', 'png'])
    make_bad_pixels_mask(path_to_bpm_dir, file_names)


def calc_avg_color(img):
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color


def search_bad_pixels_in_img(img, set_of_bad_pixels):
    avg_color = calc_avg_color(img)
    ar, ag, ab = avg_color

    rows, cols, depth = img.shape

    for i in range(rows):
        for j in range(cols):
            r, g, b = img[i, j]

            if abs(r - ar) > DETECT_THRESHOLD or abs(g > ag) > DETECT_THRESHOLD or abs(b > ab) > DETECT_THRESHOLD:
                set_of_bad_pixels.add((i, j))



def make_mask(set_of_bad_pixels, rows, cols):
    image = numpy.zeros((rows, cols, 3), numpy.uint8)  # creating blank image

    for i in range(rows):
        for j in range(cols):
            if (i, j) in arr_bad_pixels:
                image[i, j] = [255, 255, 255]

    cv2.imwrite(path_to_bpm_dir + mask_file_name, image)


def make_bad_pixels_mask(base_dir, bad_pixels_image_names):
    set_of_bad_pixels = set()

    tmp_img = cv2.imread(base_dir + bad_pixels_image_names[0])
    first_img_rows, first_img_cols, depth = tmp_img.shape

    for img_name in bad_pixels_image_names:
        if img_name == mask_file_name:
            continue

        img = cv2.imread(base_dir + img_name)
        rows, cols, depth = img.shape

        if rows != first_img_rows or first_img_cols != first_img_cols:
            raise Exception('The dimensions of the images in detect directory are different')

        search_bad_pixels_in_img(img, set_of_bad_pixels)

    make_mask(set_of_bad_pixels, first_img_rows, first_img_cols)
