#!/bin/sh
if ! command -v pip &> /dev/null
then
    echo "Installing pip"
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user
fi

python -m pip install --user wand
python -m pip install --user svgpathtools
python -m pip install --user requests
python -m pip install --user pyobjc
python -m pip install --user numpy
python -m pip install --user reportlab
python -m pip install --user svglib