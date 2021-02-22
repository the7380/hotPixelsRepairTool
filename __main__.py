import sys

import bad_pixels_mask as bpm
import bad_pixels_fixer as bpf

if __name__ == '__main__':
    cli_params = sys.argv[1:]

    if "detect" in cli_params:
        params = dict()

        index = cli_params.index("detect")
        if index + 1 < len(cli_params) and cli_params[index + 1] == "--highlight":
            params['highlight'] = True

        bpm.start(**params)

    if "fix" in cli_params:
        params = dict()

        index = cli_params.index("fix")
        if index + 1 < len(cli_params) and cli_params[index + 1] == "--replace":
            params['replace_mode'] = True

        bpf.start(**params)
