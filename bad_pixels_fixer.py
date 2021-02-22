import os
import pathlib

import cv2
import piexif
import datetime
import time

from multiprocessing import Process, cpu_count
from PIL import Image

import utils as u
import bad_pixels_mask as bpm

REPLACE_MODE = False
ALGORITHM = "TELEA"

path_to_input_bpf_dir = "./_input/"
path_to_output_bpf_dir = "./_output/"


def start(replace_mode=False, algorithm="TELEA"):
    global REPLACE_MODE
    REPLACE_MODE = replace_mode

    global ALGORITHM
    ALGORITHM = algorithm

    file_names = u.get_files_from_dir_with_ext(path_to_input_bpf_dir, ('jpg', 'jpeg', 'png'))

    multiprocessing_start(file_names)


def multiprocessing_start(file_names):
    processes = []
    cpu_number = cpu_count()
    task_per_cpu = len(file_names) // cpu_number

    cpu_tasks = []
    if task_per_cpu > 0:
        for x in range(cpu_number):
            cpu_tasks.append([])
            cpu_tasks[x].extend(file_names[x * task_per_cpu:(x + 1) * task_per_cpu])
        cpu_tasks[cpu_number - 1].extend(file_names[task_per_cpu * cpu_number - 1:len(file_names) - 1])
    else:
        cpu_tasks.append([])
        cpu_tasks[0].extend(file_names)

    for tasks in cpu_tasks:
        proc = Process(target=fix_image_by_mask_caller, args=(tasks, bpm.path_to_bpm_dir + bpm.mask_file_name))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()


def fix_image_by_mask_caller(tasks, mask_path):
    for el in tasks:
        fix_image_by_mask(el, mask_path)


def fix_image_by_mask(img_name, mask_path):
    print("Fixing " + img_name)

    img = cv2.imread(path_to_input_bpf_dir + img_name)[..., ::-1]  # RGB, not BGR
    mask = cv2.imread(mask_path, 0)

    if ALGORITHM == "TELEA":
        dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    elif ALGORITHM == "NS":
        dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_NS)
    else:
        raise Exception("Incorrect inpainting algorithm")

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
