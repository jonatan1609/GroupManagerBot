#!/bin/bash

CONFIG_FILE="/config/config.toml"
if [ ! -f "$CONFIG_FILE" ]; then
    cp /opt/bot/.config.toml.example $CONFIG_FILE
fi

python -m bot
