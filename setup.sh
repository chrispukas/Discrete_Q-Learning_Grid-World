#!/usr/bin/env bash

ENVIRONMENT_NAME="dqn_env"


# Create conda environment with required dependencies
conda create --name $ENVIRONMENT_NAME
conda activate $ENVIRONMENT_NAME

if [ -f "requirements.txt" ]; then
    conda install -c conda-forge --file requirements.txt -y
fi

# Install local package
pip install -e .