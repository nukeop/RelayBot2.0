# ![RelayBot2.0](https://nukeop.github.io/RelayBot2.0/)
[![Build Status](https://travis-ci.org/nukeop/RelayBot2.0.svg?branch=master)](https://travis-ci.org/nukeop/RelayBot2.0) [![Code Health](https://landscape.io/github/nukeop/RelayBot2.0/master/landscape.svg?style=flat)](https://landscape.io/github/nukeop/RelayBot2.0/master) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/82440b8ba7c64ad2912e57f1680ed1e0)](https://www.codacy.com/app/alsw/RelayBot2-0?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nukeop/RelayBot2.0&amp;utm_campaign=Badge_Grade) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/0dbd87e771ad485da35be8621c4edbfe/badge.svg)](https://www.quantifiedcode.com/app/project/0dbd87e771ad485da35be8621c4edbfe) 


New incarnation of Relay Bot™

## How to run

Clone the repo:

`$ git clone https://github.com/nukeop/RelayBot2.0.git`

Create a virtual environment and install dependencies:

```
$ cd RelayBot2.0
$ mkdir venv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Edit the config file and plug in the username, password, and possibly other keys as required by plugins (if you want those plugins to work). You can also add users to "ignored" and "authorized" lists:

`$ nano relaybot/config.json`

Start the program:

`$ python relaybot/relaybot.py`

If your account has 2FA or steam Guard enabled you will be prompted to enter the code once, then the program will save a sentry file named `relaybot_sentry.bin` so you don't have to do it again. It will also create a local sqlite database named `relaybot.db` if it does not exist.

For a list of all available commands, open the chat window on Steam, and send `!help` to the bot, it will reply with all commands you can use. `!plugins` will display a list of all plugins and short descriptions (even of plugins that are not callable). `!plugins <name>` will display detailed info about a plugin.
