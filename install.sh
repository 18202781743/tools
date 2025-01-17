#!/bin/bash

set -e

sudo apt install python3-venv

python -m venv ~/.venv

source ~/.venv/bin/activate

pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip install -r requirements.txt

deactivate

chmod +x ./crp
sudo cp ./crp /usr/bin/crp

sudo mkdir -p /usr/share/tools/
sudo install ./package-crp.py /usr/share/tools/

echo "##################### 安装完成 #####################"
echo ""
echo "################# 执行 crp --help #####################"

/usr/bin/crp --help
