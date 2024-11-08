#!/usr/bin/env python3.11

import os
import re
import sys


def main():
    project_name = sys.argv[1]
    folder_name = sys.argv[2]
    recur_count = sys.argv[3]

    project_path = os.path.join("./results", project_name)
    folder_path = os.path.join(project_path, folder_name)
    signature_path = os.path.join(folder_path,"benchmarks.txt")
    print(project_path)
    print(folder_path)

    #record signatures
    with open(signature_path,'w') as fs:
        signature_list = os.listdir(os.path.join(folder_path,str(1)))
        for s in signature_list:
            if os.path.isdir(os.path.join(folder_path,str(1),s)):
                fs.write(f"{s}\n")



    # signature_list 경로 설정
    signature_list = list()
    with open(signature_path,'r') as fs:
        signature_list = fs.readlines()
    
    for s in signature_list:
        s = s.split('\n')[0]
        max_scored_output = [0,0, 0, 0, [""], 0,0]  #validation, output, recur_number, 1 or 2, coverage, avg_rate
        for count in range(1,int(recur_count)+1):
            log_dir = os.path.join(folder_path, str(count), s, "logs", "run")
            for i in range(1, 3):
                result_path = os.path.join(folder_path, str(count), s, f"0{i}_result.txt")
                with open(result_path, 'w') as fw:

                    for j in range(6, -1, -1):
                        log_file_name = f"0{i}.cc-F{j}.log"
                        log_file_path = os.path.join(log_dir, log_file_name)
                        if not os.path.isfile(log_file_path):
                            continue

                        print(s +  "-> " + str(count) + "  in  " + str(i) + ".cc  :  " + str(j))

                        total_rate_sum = 0.0
                        timestamp_count = 0

                        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as fs:
                            lines = fs.readlines()
                            for line in lines:
                                if "Target runtime" in line and "Function runtime" in line:
                                    timestamp_count += 1
                                    numbers = re.findall(r'\d+', line)

                                    target_runtime = int(numbers[0])
                                    function_runtime = int(numbers[1])
                                    if target_runtime == 0:
                                        continue
                                    time_rate = function_runtime / target_runtime
                                    total_rate_sum += time_rate

                        if timestamp_count != 0:
                            avg_rate = total_rate_sum / timestamp_count
                            fw.write(f"{avg_rate}\n")
                        
                        if timestamp_count != 0 and time_rate != 0:
                            cov_path = os.path.join(folder_path, str(count), s, "status", f'0{i}', "result.json")
                            with open(cov_path, 'r') as fc:
                                covs = fc.readlines()
                            for c in covs:
                                cov_tmp = re.search(r'\d+\.\d+', c)
                                if(cov_tmp):
                                    break
                            coverage = float(cov_tmp.group(0))
                            validation = coverage * avg_rate
                            print("validaton: " + str(validation) + ", avg_rate : " + str(avg_rate) + ", coverage : " + str(coverage))
                            if validation > max_scored_output[0]:
                                max_scored_output[0] = validation
                                max_scored_output[1] = count
                                max_scored_output[2] = i
                                max_scored_output[4] = coverage
                                max_scored_output[5] = avg_rate
                                with open(os.path.join(folder_path, str(count), s, "fixed_targets",f'0{i}.cc')) as target:
                                    max_scored_output[3] = target.readlines()

        output_folder_path = os.path.join(folder_path, "best_outputs",s)
        os.makedirs(output_folder_path, exist_ok=True)
        with open(os.path.join(output_folder_path, 'output.cc'), 'w') as ofp:
            for output_text in max_scored_output[3]:
                if ("#include <chrono>" in output_text) or ("std::cout" in output_text) or ("std::chrono" in output_text) or ("#include <iostream>" in output_text):
                    continue
                if ("//erase" in output_text):
                    continue
                ofp.write(f"{output_text}")
        with open(os.path.join(output_folder_path, 'info.txt'), 'w') as ofp:
            info_str = "max_validation : " + str(max_scored_output[0]) + "\nfrom "+ str(max_scored_output[1]) + "st -> 0" + str(max_scored_output[2]) + ".cc\n"
            info_str += "coverage : " + str(max_scored_output[4]) + ", avg_rate : " + str(max_scored_output[5])
            ofp.write(info_str)


if __name__ == '__main__':
    main()
