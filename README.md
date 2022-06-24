# FeedBack Bot

A simple feedback bot for the FL Studio discord server

Watches configured channels for audio files or URLs, and provides a 5-star rating system

## Installation

You will need Python 3.10 or higher, and [Poetry](https://python-poetry.org/docs/#installation)

After cloning the repository, run:
```
poetry update
```
To update all dependencies. That's it, the bot is ready to go!

## Usage

To run the bot, simply run:
```
python main.py
```
Note that you will need to set up your config file for the bot to work.  
The bot comes with a `config.example.ini` file. Simply create a copy of this file and name it `config.ini`, then add your bot token.
