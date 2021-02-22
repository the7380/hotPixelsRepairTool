import sys

import bad_pixels_mask as bpm
import bad_pixels_fixer as bpf
import bad_pixels_emulator as bme
import constants as cns

if __name__ == '__main__':
    cli_params = sys.argv[1:]

    if cns.CLI_DETECT_WORD in cli_params:
        params = dict()

        if cns.CLI_DETECT_HIGHLIGHT_PARAMETER in cli_params:
            params[cns.CLI_DETECT_HIGHLIGHT_WORD] = True

        if cns.CLI_DETECT_THRESHOLD_PARAMETER in cli_params:
            index = cli_params.index(cns.CLI_DETECT_THRESHOLD_PARAMETER)
            if index + 1 < len(cli_params):
                params[cns.CLI_DETECT_THRESHOLD_WORD] = int(cli_params[index + 1])
            else:
                raise Exception("The threshold value is not set")

        bpm.start(**params)

    if cns.CLI_FIX_WORD in cli_params:
        params = dict()

        if cns.CLI_FIX_REPLACE_PARAMETER in cli_params:
            params[cns.CLI_FIX_REPLACE_WORD] = True

        if cns.CLI_FIX_ALGORITHM_PARAMETER in cli_params:
            index = cli_params.index(cns.CLI_FIX_ALGORITHM_PARAMETER)
            if index + 1 < len(cli_params):
                params[cns.CLI_FIX_ALGORITHM_WORD] = cli_params[index + 1].upper()
            else:
                raise Exception("The algorithm type is not set")

        bpf.start(**params)

    if cns.CLI_EMULATION_WORD in cli_params:
        bme.start()
