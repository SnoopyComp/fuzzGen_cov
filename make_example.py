#!/usr/bin/env python3.11

#######     arg1 : project name
#######     arg2 : folder name that you want to create
#######     arg3 : repetition number of folder

#######     Best output will be saved at 'result/{library name}/{folder name}/best_outputs
#######                              and 'prompts/example/{folder name}

import os
import re
import sys


def main():
    project_name = sys.argv[1]
    folder_name = sys.argv[2]
    recur_count = sys.argv[3]

    project_path = os.path.join("./results", project_name)
    folder_path = os.path.join(project_path, folder_name)
    signature_path = os.path.join(folder_path, "benchmarks.txt")
    example_path = os.path.join("./prompts", "example", folder_name)
    print(project_path)
    print(folder_path)

    # Record signatures
    os.makedirs(folder_path, exist_ok=True) 
    with open(signature_path, 'w') as fs:
        signature_list = os.listdir(os.path.join(folder_path, str(1)))
        for s in signature_list:
            if os.path.isdir(os.path.join(folder_path, str(1), s)):
                fs.write(f"{s}\n")

    # Load signature list
    with open(signature_path, 'r') as fs:
        signature_list = fs.readlines()

    sig_idx = 1
    for s in signature_list:
        s = s.strip()
        max_cov_output = [0, 0, 0, 0.0, []]  # repetition, subtask, coverage, cov_diff, src code
        result_str = ""
        for count in range(1, int(recur_count) + 1):
            for i in range(1, 3):
                cov_path = os.path.join(folder_path, str(count), s, "status", f'0{i}', "result.json")
                try:
                    with open(cov_path, 'r') as fs:
                        result = fs.readlines()
                except FileNotFoundError:
                    continue  # Skip if file does not exist

                # Parse coverage and coverage_diff
                covs = [0.0, 0.0]
                for idx, line in enumerate(result):
                    match = re.search(r'\d+\.\d+', line)
                    if match:
                        covs[idx] = float(match.group(0))
                    if idx >= 1:
                        break

                coverage, coverage_diff = covs
                if max_cov_output[2] < coverage:  # Compare with max coverage
                    max_cov_output = [count, i, coverage, coverage_diff, []]
                    target_path = os.path.join(folder_path, str(count), s, "fixed_targets", f'0{i}.cc')
                    try:
                        with open(target_path, 'r') as target:
                            max_cov_output[4] = target.readlines()
                    except FileNotFoundError:
                        pass

                result_str += f"{s} - {i}, {count}\t coverage: {coverage}\t cov_diff: {coverage_diff}\n"
                print(f"{s} - {count}, {i}\t coverage: {coverage}\t cov_diff: {coverage_diff}\n")

        # Define output paths and write outputs
        output_folder_path = os.path.join(folder_path, "best_outputs", s)
        os.makedirs(output_folder_path, exist_ok=True)

        # Write best coverage output file
        example_sig_path = os.path.join(example_path, str(sig_idx))
        os.makedirs(example_sig_path, exist_ok=True)

        with open(os.path.join(example_sig_path, "output.cc"), 'w') as fw:
            fw.writelines(max_cov_output[4])

        with open(os.path.join(example_sig_path, "info.txt"), 'w') as fw:
            info_str = (
                f"repetition num: {max_cov_output[0]}, "
                f"subtask num: {max_cov_output[1]}, "
                f"max_coverage: {max_cov_output[2]}, "
                f"coverage_diff: {max_cov_output[3]}"
            )
            fw.write(info_str)

        with open(os.path.join(output_folder_path, 'output.cc'), 'w') as ofp:
            ofp.writelines(max_cov_output[4])

        with open(os.path.join(output_folder_path, 'best_info.txt'), 'w') as ofp:
            ofp.write(info_str)

        with open(os.path.join(output_folder_path, 'total_info.txt'), 'w') as ofp:
            ofp.write(result_str)

        sig_idx += 1


if __name__ == '__main__':
    main()
