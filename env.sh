#! /bin/bash
project_path=$(dirname "$(realpath $0)")
export PYTHONPATH=$project_path/scripts
export PATH=$PATH:$project_path
export | grep PYTHONPATH
