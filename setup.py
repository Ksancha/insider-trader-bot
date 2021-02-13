from setuptools import setup, find_packages

setup(name='insider_trader_bot',
      version='1.0',
      description='Telegram bot for insider trading',
      author='Daniil Balabanov',
      author_email='danedbalabanov@gmail.com',
      packages=find_packages(exclude=['env', 'tests']),
      install_requirements=[
                "user_agent",
                "requests",
                "sqlalchemy",
                "beautifulsoup4",
                "python-telegram-bot==13.2"
                ]
     )