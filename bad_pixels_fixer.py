import os
import pathlib

import cv2
import piexif
import datetime
import time

from PIL import Image

import utils as u
import bad_pixels_mask as bpm

REPLACE_MODE = False

path_to_input_bpf_dir = "./_input/"
path_to_output_bpf_dir = "./_output/"


def start(replace_mode=False):
    global REPLACE_MODE
    REPLACE_MODE = replace_mode

    file_names = u.get_files_from_dir_with_ext(path_to_input_bpf_dir, ['jpg', 'jpeg', 'png'])

    for file in file_names:
        fix_image_by_mask(file, bpm.path_to_bpm_dir + bpm.mask_file_name)


def fix_image_by_mask(img_name, mask_path):
    img = cv2.imread(path_to_input_bpf_dir + img_name)
    mask = cv2.imread(mask_path, 0)

    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    filename, file_extension = os.path.splitext(img_name)

    if not REPLACE_MODE:
        save_file_with_metadata_from_another_file(path_to_input_bpf_dir + filename + file_extension,
                                                  path_to_output_bpf_dir + filename + file_extension,
                                                  dst)
    else:
        save_file_with_metadata_from_another_file(path_to_input_bpf_dir + filename + file_extension,
                                                  path_to_input_bpf_dir + filename + file_extension,
                                                  dst)


def save_file_with_metadata_from_another_file(path_src, path_dst, img_to_save):
    # open old image (before potential overwriting)
    src_img = Image.open(path_src)

    # getting mtime from old image (before potential overwriting)
    src_img_mtime = datetime.datetime.fromtimestamp(pathlib.Path(path_src).stat().st_mtime)
    src_img_mtime_prepared = time.mktime(src_img_mtime.timetuple())

    # getting exif from old image (before potential overwriting)
    src_img_exif_dict = piexif.load(src_img.info['exif']) if 'exif' in src_img.info else None
    src_img_exif_bytes = piexif.dump(src_img_exif_dict) if src_img_exif_dict is not None else None

    # getting the image from bytes
    dst_img = Image.fromarray(img_to_save, mode="RGB")

    # saving image with exif
    if src_img_exif_dict is not None:
        dst_img.save(path_dst, exif=src_img_exif_bytes)
    else:
        dst_img.save(path_dst)

    # setting mtime and atime (after potential overwriting)
    os.utime(path_dst, (src_img_mtime_prepared, src_img_mtime_prepared))
