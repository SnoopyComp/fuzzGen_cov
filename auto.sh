#!/bin/bash
#	$1 : library name
#	$2 : gpt model name

if [ -f .env ]; then
	export $(cat .env | xargs)
fi

export OPENAI_API_KEY=$OPENAI_API_KEY

library_name=$1
model_name=$2

no_example=no-example
default=default
lv1=lv1
lv2=lv2

#	no example section
bash clear_and_run.sh ${no_example} 1 10 nothing ${model_name} ${library_name} --${no_example}
bash make_example.sh ${library_name} ${no_example} 10

#	default section
bash clear_and_run.sh ${default} 1 10 nothing ${model_name} ${library_name} --${default}
bash make_example.sh ${library_name} ${default} 10

#	lv1 section
bash clear_and_run.sh ${lv1} 1 10 nothing ${model_name} ${library_name} --${lv1}
bash make_example.sh ${library_name} ${lv1} 10

#	lv2 section
bash clear_and_run.sh ${lv2} 1 10 nothing ${model_name} ${library_name} --${lv2}
bash make_example.sh ${library_name} ${lv2} 10
