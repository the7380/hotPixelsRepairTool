import cv2
import numpy

import utils as u

path_to_bpm_dir = "./_detect/"
mask_file_name = "bad_pixels_mask.png"


def start():
    file_names = u.get_files_from_dir_with_ext(path_to_bpm_dir, ['jpg', 'jpeg', 'png'])
    make_bad_pixels_mask(path_to_bpm_dir + file_names[0])


def calc_avg_color(img):
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color


def search_bad_pixels_in_img(img):
    avg_color = calc_avg_color(img)
    ar, ag, ab = avg_color

    rows, cols, depth = img.shape

    result = []

    for i in range(rows):
        for j in range(cols):
            r, g, b = img[i, j]

            if r > ar or g > ag or b > ab:
                result.append([i, j])

    return result


def make_mask(arr_bad_pixels, rows, cols):
    image = numpy.zeros((rows, cols, 3), numpy.uint8)  # creating blank image

    for i in range(rows):
        for j in range(cols):
            if [i, j] in arr_bad_pixels:
                image[i, j] = [255, 255, 255]

    cv2.imwrite(path_to_bpm_dir + mask_file_name, image)


def make_bad_pixels_mask(bad_pixels_img_path):
    img = cv2.imread(bad_pixels_img_path)

    arr_bad_pixels = search_bad_pixels_in_img(img)

    rows, cols, depth = img.shape
    make_mask(arr_bad_pixels, rows, cols)
