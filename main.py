from feedback_bot import FeedbackBot

#run token
if __name__ == "__main__":
	token = 'OTg5NTk4MjM5MDMwNDAzMDgy.Ggy-Pq.LTw8QzFBRr34S6zq3ki5Rfc5Tc91P9VWhfufj8'
	token = 'NzA2NjgxOTQ5NTk4NTE1MjYx.GBBkgE.BJ2q10rab0UTdh59hDg94oOaZF2ypdJmcfdOrg'
	bot = FeedbackBot([706699759456354366])
	bot.run(token)
else:
	print(f"Run as main! '{__name__}'")