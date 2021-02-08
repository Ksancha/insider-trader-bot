from distutils.core import setup

setup(name='insider_trader_bot',
      version='1.0',
      description='Telegram bot for insider trading',
      author='Daniil Balabanov',
      author_email='danedbalabanov@gmail.com',
      packages=['distutils',
                'distutils.command',
                "user_agent",
                "requests",
                "beautifulsoup4",
                "python-telegram-bot==13.2"
                ],
     )