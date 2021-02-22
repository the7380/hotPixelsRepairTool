import cv2
import numpy

import utils as u

path_to_bpm_dir = "./_detect/"
mask_file_name = "bad_pixels_mask.png"
highlight_file_prefix = "highlight_"

DETECT_THRESHOLD = 10
DETECT_HIGHLIGHT = False


def start(highlight=False, threshold=10):
    global DETECT_HIGHLIGHT
    DETECT_HIGHLIGHT = highlight

    global DETECT_THRESHOLD
    DETECT_THRESHOLD = threshold

    file_names = u.get_files_from_dir_with_ext(path_to_bpm_dir, ('jpg', 'jpeg', 'png'))
    make_bad_pixels_mask(path_to_bpm_dir, file_names)


def calc_avg_color(img):
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color


def search_bad_pixels_in_img(img):
    avg_color = calc_avg_color(img)
    ar, ag, ab = avg_color
    set_of_bad_pixels = set()

    rows, cols, depth = img.shape

    for i in range(rows):
        for j in range(cols):
            r, g, b = img[i, j]

            if abs(r - ar) > DETECT_THRESHOLD or abs(g > ag) > DETECT_THRESHOLD or abs(b > ab) > DETECT_THRESHOLD:
                set_of_bad_pixels.add((i, j))

    return set_of_bad_pixels


def make_mask(set_of_bad_pixels, rows, cols):
    image = numpy.zeros((rows, cols, 3), numpy.uint8)  # creating blank image

    for el in set_of_bad_pixels:
        i, j = el
        image[i, j] = (255, 255, 255)

    cv2.imwrite(path_to_bpm_dir + mask_file_name, image)


def make_bad_pixels_mask(base_dir, bad_pixels_image_names):
    set_of_bad_pixels = set()

    tmp_img = cv2.imread(base_dir + bad_pixels_image_names[0])
    first_img_rows, first_img_cols, depth = tmp_img.shape

    for img_name in bad_pixels_image_names:
        if img_name == mask_file_name or img_name.startswith(highlight_file_prefix):
            continue

        img = cv2.imread(base_dir + img_name)
        rows, cols, depth = img.shape

        if rows != first_img_rows or first_img_cols != first_img_cols:
            raise Exception('The dimensions of the images in detect directory are different')

        current_set_of_bad_pixels = search_bad_pixels_in_img(img)
        set_of_bad_pixels.update(current_set_of_bad_pixels)

        if DETECT_HIGHLIGHT:
            highlight_pixels(img, img_name, path_to_bpm_dir, current_set_of_bad_pixels)

    make_mask(set_of_bad_pixels, first_img_rows, first_img_cols)


def highlight_pixels(img, img_name, base_dir, pixels_coords):
    for el in pixels_coords:
        i, j = el
        safe_painting(img, (i + 4, j))
        safe_painting(img, (i + 5, j))

        safe_painting(img, (i - 4, j))
        safe_painting(img, (i - 5, j))

        safe_painting(img, (i, j + 4))
        safe_painting(img, (i, j + 5))

        safe_painting(img, (i, j - 4))
        safe_painting(img, (i, j - 5))

    cv2.imwrite(base_dir + highlight_file_prefix + img_name, img)


def safe_painting(img, pixel_coords, color=(255, 255, 0)):
    i, j = pixel_coords
    max_i, max_j, depth = img.shape
    if 0 <= i < max_i and 0 <= j <= max_j:
        img[i, j] = color
