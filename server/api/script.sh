#!/bin/bash

# Register conda PATH
export PATH=/home/pkr7098/miniconda3/bin:$PATH

export NOTION_TOKEN=secret_MqjmE6xA5ynMXGtAfyu9BA6s9DTZQRAhMnqxbUaRAJ6
export NOTION_DATABASE_SERVER_API_ID=eec8cad7dc044af6a64035e8fe813ffe

# Activate conda virtual environment
conda activate notion-api

# Activate monitoring program
python /home/pkr7098/project/notion/server/api/main.py --loop True > log.out 2> err.out

