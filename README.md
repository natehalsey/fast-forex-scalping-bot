# python-trading-bot

Python trading bot using IBKR.

# Getting started

First ensure `docker, docker-compose` and all dependencies are installed.

```
git clone https://github.com/natehalsey/python-trading-bot
```

Then you'll need to get your IBKR information from IBKR and set it in a `.env` file in the root of the project.

```
# .env

TWS_USERID=""
TWS_PASSWORD=""
TRADING_MODE=""

```

Afterward, simply run:

```
make docker.start
```



# Local Dev

Install:

```
- pyenv
- virtualenv
```

Then simply `. .script/bootstrap` to bootstrap the environment and begin developing.
# fast-forex-scalping-bot
