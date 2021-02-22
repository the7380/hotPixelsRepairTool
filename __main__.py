import sys

import bad_pixels_mask as bpm
import bad_pixels_fixer as bpf
import bad_pixels_emulator as bme

if __name__ == '__main__':
    cli_params = sys.argv[1:]

    if "detect" in cli_params:
        params = dict()

        if "--highlight" in cli_params:
            params['highlight'] = True

        if "--threshold" in cli_params:
            index = cli_params.index("--threshold")
            if index + 1 < len(cli_params):
                params['threshold'] = int(cli_params[index + 1])
            else:
                raise Exception("The threshold value is not set")

        bpm.start(**params)

    if "fix" in cli_params:
        params = dict()

        if "--replace" in cli_params:
            params['replace_mode'] = True

        if "--algorithm" in cli_params:
            index = cli_params.index("--algorithm")
            if index + 1 < len(cli_params):
                params['algorithm'] = cli_params[index + 1].upper()
            else:
                raise Exception("The algorithm type is not set")

        bpf.start(**params)

    if "emulation" in cli_params:
        bme.start()
