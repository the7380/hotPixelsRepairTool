import cv2
import numpy

import utils as u
import constants as cns


def start(highlight=False, threshold=10):
    file_names = u.get_files_from_dir_with_ext(cns.PATH_TO_DETECT_DIR, ('jpg', 'jpeg', 'png'))
    make_bad_pixels_mask(cns.PATH_TO_DETECT_DIR, file_names, highlight, threshold)


def calc_avg_color(img):
    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color


def search_bad_pixels_in_img(img, threshold):
    avg_color = calc_avg_color(img)
    ar, ag, ab = avg_color
    set_of_bad_pixels = set()

    rows, cols, depth = img.shape

    for i in range(rows):
        for j in range(cols):
            r, g, b = img[i, j]

            if abs(r - ar) > threshold or abs(g > ag) > threshold or abs(b > ab) > threshold:
                set_of_bad_pixels.add((i, j))

    return set_of_bad_pixels


def make_mask(set_of_bad_pixels, rows, cols):
    image = numpy.zeros((rows, cols, 3), numpy.uint8)  # creating blank image

    for el in set_of_bad_pixels:
        i, j = el
        image[i, j] = (255, 255, 255)

    cv2.imwrite(cns.PATH_TO_DETECT_DIR + cns.PATH_TO_MASK_FILE, image)


def make_bad_pixels_mask(base_dir, bad_pixels_image_names, highlight, threshold):
    set_of_bad_pixels = set()

    tmp_img = cv2.imread(base_dir + bad_pixels_image_names[0])
    first_img_rows, first_img_cols, depth = tmp_img.shape

    for img_name in bad_pixels_image_names:
        if img_name == cns.PATH_TO_MASK_FILE or img_name.startswith(cns.HIGHLIGHT_FILE_PREFIX):
            continue

        img = cv2.imread(base_dir + img_name)
        rows, cols, depth = img.shape

        if rows != first_img_rows or first_img_cols != first_img_cols:
            raise Exception('The dimensions of the images in detect directory are different')

        current_set_of_bad_pixels = search_bad_pixels_in_img(img, threshold)
        set_of_bad_pixels.update(current_set_of_bad_pixels)

        if highlight:
            highlight_pixels(img, img_name, cns.PATH_TO_DETECT_DIR, current_set_of_bad_pixels)

    make_mask(set_of_bad_pixels, first_img_rows, first_img_cols)
    with open(base_dir + cns.PATH_TO_HOTPIXELS_FILE, "w", encoding="UTF-8") as file:
        for el in set_of_bad_pixels:
            x, y = el
            file.writelines(str(x) + " " + str(y) + "\n")


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

    cv2.imwrite(base_dir + cns.HIGHLIGHT_FILE_PREFIX + img_name, img)


def safe_painting(img, pixel_coords, color=(255, 255, 0)):
    i, j = pixel_coords
    max_i, max_j, depth = img.shape
    if 0 <= i < max_i and 0 <= j <= max_j:
        img[i, j] = color
