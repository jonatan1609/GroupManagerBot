from . import __version__, client
from .set_bot_commands import main
from loguru import logger

logger.info('GroupManagerBot is running.. version {}'.format(__version__))

client.loop.run_until_complete(main())
client.run()
