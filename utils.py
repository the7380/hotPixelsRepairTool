import os


def get_files_from_dir_with_ext(path_to_bpf_dir, included_extensions):
    file_names = [fn for fn in os.listdir(path_to_bpf_dir)
                  if any(fn.lower().endswith(ext) for ext in included_extensions)]

    return file_names
