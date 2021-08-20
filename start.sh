#!/bin/bash
stty -echoctl
if [ ! -d "venv" ]; then
  python -m venv venv
fi;
. venv/bin/activate
echo upgrading pip...
python -m pip -q install --upgrade pip
echo installing packages..
python -m pip -q install -r requirements.txt;
echo running..
if [ ! -f "config.toml" ]; then
    echo "Config doesn't exist, copying from default..."
    cp .config.toml.example config.toml
fi
python -m bot
