#!/bin/bash
#	$1 : directory name
#	$2 : index to start repetition
#	$3 : index to end repetition (include $3)
#	$4 : if exist : remove temporary files for each repetition
#	$5 : llm model
#	$6 : library name
#	$7 : option


if [ -f .env ]; then
	export $(cat .env | xargs)
fi

export OPENAI_API_KEY=$OPENAI_API_KEY



directory_name=$1
library_name=$6
llm_model=$5
option=$7

sudo rm -rf /tmp/*
rm -rf ~/.local/share/Trash/files/*


for ((var=$2; var<=$3; var++));
do
	./run_all_experiments.py\
	--model=${llm_model}\
	-y ./benchmark-sets/all/${library_name}.yaml\
	--work-dir=results/${library_name}/${directory_name}/$var\
	${option}

	python3.11 -m report.web -r results/${library_name}/${directory_name}/$var -o outputs/${library_name}/${directory_name}/$var
done

#./evaluate_output.py ${library_name} ${directory_name} $2
