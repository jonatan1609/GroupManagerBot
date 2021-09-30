#!/bin/bash
stty -echoctl
if [ ! -d "venv" ]; then
    python -m venv venv
fi;
. venv/bin/activate
if [[ ! ($1 == "-s" || $1 == "--skip") ]]; then
    echo upgrading pip...
    python -m pip -q install --upgrade pip
    echo installing packages..
    python -m pip -q install -r requirements.txt;
fi;
echo running..
if [ ! -f "config.toml" ]; then
    echo "Config doesn't exist, copying from default..."
    cp .config.toml.example config.toml
fi
python -m bot
