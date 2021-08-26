# GroupManagerBot
This bot will help you to manage your groups and to avoid spam.

# Installation

You can run the bot on your environment or use docker.

## configuration

Copy `.config.toml.example` into `config.toml` 
and fill the relevant fields. `api_id` and `api_hash`
which you can obtain from https://my.telegram.org, and bot_token which you can get from https://t.me/botfather.
- You can also choose what Database you want to use. read pony.orm documentation and modify the entire block under bot.database with the relevant fields that pony.orm.Database requires.

## venv (linux)

```
sh start.sh
```

## Docker
> Use `:latest` for latest published version, you can specify a release or even a branch and commit.
e.g `:master-d1dc0d4`

1. Create a config directory, and create a `config.toml` inside    
    ```bash
    mkdir -p ~/group-manager-config
    cp .config.toml.example ~/group-manager-config/config.toml
    # Configure the bot
    nano ~/group-manager-config/config.toml
    ```
2. Run the docker container, add `-d` to run in the background
    ```bash
    docker run -v ~/group-manager-config:/config \
    ghcr.io/jonatan1609/group-manager-bot:latest
    ```
   
# support

You can join our [Telegram Group](https://t.me/GMB_group) to get live support with either the bot itself or related stuff.