cp relaybot/config.py relaybot/config.py.bak
git pull origin master
cp relaybot/config.py.bak relaybot/config.py
python relaybot/relaybot.py
