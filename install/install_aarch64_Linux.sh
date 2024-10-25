#!/bin/bash
echo "[ Info ] installing dependencies..."
curl -sSL https://install.python-poetry.org | python3 -
pkg install x11-repo firefox geckodriver xorg-server-xvfb
