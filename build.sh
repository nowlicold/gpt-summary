#!/bin/bash

# 删除 build 目录
rm -r build

# 下来依赖
pip3 install -r requirements.txt -t package

zip -r recapnow.zip build/

zip -r ../recapnow.zip .

zip my-deployment-package.zip lambda_function.py