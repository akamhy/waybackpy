#!/bin/bash
python3 --V
cd ..
python3 -m venv waybackvenv
. waybackvenv/bin/activate
cd -
pip3 install --upgrade pip3
pip3 install setuptools -U
pip3 install wheel --upgrade
pip3 install twine -U
python3 setup.py sdist bdist_wheel
twine upload dist/*
