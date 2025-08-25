#!/usr/bin/env bash

ENVIRONMENT_NAME="dqn_env"

source "$(conda info --base)/etc/profile.d/conda.sh"

# Create conda environment with required dependencies
conda env list | grep -q "^$ENVIRONMENT_NAME\s" || conda create --name $ENVIRONMENT_NAME python=3.12 -y
conda activate $ENVIRONMENT_NAME

if [ -f "requirements.txt" ]; then
    conda install -c conda-forge --file requirements.txt -y
fi

# Install local package
pip install -e .