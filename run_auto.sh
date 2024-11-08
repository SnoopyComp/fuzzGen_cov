#!/bin/bash

#	$1 : directory name
#	$2 : number of times to repite

############ Use this when you set the best outputs of LV.0 at 'prompts/example/auto/ 1~5 folders.
############ You should set output.txt(banchmarks info file) for each target functions.

############ Result directory name will be {directory name}_LV1, {directory name}_LV2

if [ -f .env ]; then
	export $(cat .env | xargs)
fi

export OPENAI_API_KEY=$OPENAI_API_KEY



directory_name_input=$1
library_name=xpdf

for ((cnt=1; cnt<=2; cnt++));
do
	directory_name=${directory_name_input}_LV${cnt}

	for ((var=1; var<=$2; var++));
	do
		./run_all_experiments.py\
		--model='gpt-4o-mini'\
		-y ./benchmark-sets/all/${library_name}.yaml\
		--work-dir=results/${library_name}/${directory_name}/$var

		python3.11 -m report.web -r results/${library_name}/${directory_name}/$var -o outputs/${library_name}/${directory_name}/$var
	#	python3.11 -m http.server 2222 -d outputs/${library_name}/${directory_name}$var
	done

	./make_example_auto.py ${library_name} ${directory_name} $2
done