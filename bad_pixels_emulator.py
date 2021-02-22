import cv2

import utils as u
import bad_pixels_fixer as bpf
import bad_pixels_mask as bpm
import constants as cns

path_to_input_emulated_dir = cns.PATH_TO_EMULATOR_DIR
path_to_input_bpf_dir = cns.PATH_TO_INPUT_DIR


def start():
    file_names = u.get_files_from_dir_with_ext(path_to_input_bpf_dir, ('jpg', 'jpeg', 'png'))

    mask_coordinates = get_mask_coordinates_from_file(bpm.path_to_bpm_dir + cns.PATH_TO_HOTPIXELS_FILE)

    for file in file_names:
        spoil_image(file, path_to_input_bpf_dir, file, path_to_input_emulated_dir, mask_coordinates)


def get_mask_coordinates_from_file(file_path):
    with open(file_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()
        mask_coordinates = []

        for line in lines:
            line = line.replace("\n", "")
            i, j = line.split(" ")
            mask_coordinates.append((int(i), int(j)))

    return mask_coordinates


def spoil_image(src_img_name, src_base_dir, dst_img_name, dst_base_dir, mask_coordinates):
    img = cv2.imread(src_base_dir + src_img_name)

    for coords in mask_coordinates:
        i, j = coords
        img[i, j] = [255, 255, 0]

    cv2.imwrite(dst_base_dir + dst_img_name, img)
