import sys

import bad_pixels_mask as bpm
import bad_pixels_fixer as bpf

if __name__ == '__main__':
    cli_params = sys.argv[1:]

    if "detect" in cli_params:
        params = dict()

        if "--highlight" in cli_params:
            params['highlight'] = True

        bpm.start(**params)

    if "fix" in cli_params:
        params = dict()

        if "--replace" in cli_params:
            params['replace_mode'] = True

        bpf.start(**params)
