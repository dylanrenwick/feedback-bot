from feedback_bot import FeedbackBot
from configparser import ConfigParser

#run token
if __name__ == "__main__":
	config = ConfigParser()
	config.read('config.ini')
	if 'bot' not in config or 'token' not in config['bot']:
		print("Could not read config file!")
		exit(1)
	token = config['bot']['token']
	bot = FeedbackBot([706699759456354366])
	bot.run(token)
else:
	print(f"Run as main! '{__name__}'")