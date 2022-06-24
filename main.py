from feedback_bot import FeedbackBot
from configparser import ConfigParser

def read_config(config):
	if 'bot' not in config:
		print("Could not read config file!")
		exit(1)
	try:
		token = config['bot']['token']
		star_emoji = config['bot']['star_emoji']
		file_exts = [ext.strip() for ext in config['bot']['audio_file_exts'].split(',')]
		media_urls = [url.strip() for url in config['bot']['media_urls'].split(',')]
		watched_channel_ids = [channel.strip() for channel in config['bot']['watched_channels'].split(',')]
		if any(not id.isnumeric() for id in watched_channel_ids):
			print("Invalid channel ID found in watched_channels!")
			exit(1)
		watched_channels = [int(id) for id in watched_channel_ids]
	except KeyError as err:
		print(f"Could not find {err} in config file!")
		exit(1)
	
	return {
		'token'           : token,
		'star_emoji'      : star_emoji,
		'file_exts'       : file_exts,
		'media_urls'      : media_urls,
		'watched_channels': watched_channels
	}


#run token
if __name__ == "__main__":
	config = ConfigParser()
	config.read('config.ini')
	bot_config = read_config(config)
	#[706699759456354366]
	bot = FeedbackBot(bot_config)
	bot.run_bot()
else:
	print(f"Run as main! '{__name__}'")