from . import __version__, client
from .set_bot_commands import main

print('\u001b[38;5;208m\033[1mGroupManagerBot is running.. version %s\033[0m' % __version__)

client.loop.run_until_complete(main())
client.run()
