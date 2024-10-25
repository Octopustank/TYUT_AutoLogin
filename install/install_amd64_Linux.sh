#!/bin/bash
cp ./geckodriver/geckodriver_amd64_Linux /usr/bin/geckodriver
echo "[ Info ] geckodriver was copied to /usr/bin/"

echo "[ Info ] installing dependencies..."
curl -sSL https://install.python-poetry.org | python3 -
apt install python3-selenium python3-pyvirtualdisplay

