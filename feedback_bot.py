import discord
import discord.ext.commands as commands

rating_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

class FeedbackBot(commands.Bot):
	def __init__(self, config):
		intents = discord.Intents(
			guild_reactions = True,
			members         = True,
			guild_messages  = True
		)
		super().__init__(".", intents=intents)
		self.remove_command("help")
		self.config = config

	def run_bot(self):
		self.run(self.config['token'])

	async def on_message(self, message):
		if message.channel.id not in self.config['watched_channels']:
			return

		if self.is_audio_message(message):
			print(f"Adding reactions to message ID {message.id}")
			await self.add_rating_reactions(message)

	async def on_raw_reaction_add(self, payload):
		if payload.channel_id not in self.config['watched_channels'] or payload.user_id == self.user.id:
			return
		
		emoji = payload.emoji.name
		if emoji not in rating_emojis:
			return
		
		star_count = rating_emojis.index(emoji) + 1
		channel = await self.retrieve_channel(payload.channel_id)
		message = await channel.fetch_message(payload.message_id)
		if not self.is_audio_message(message):
			return
		
		guild = await self.retrieve_guild(payload.guild_id)
		user  = await self.retrieve_member(payload.user_id, guild)
		if user.bot:
			return

		print(f"User {user.nick} rated {payload.message_id} {star_count} stars")
		await self.handle_rating(message, channel, user, star_count)

	async def handle_rating(self, message, channel, user, star_count):
		stars = self.config['star_emoji'] * star_count
		embed = discord.Embed(
			title       = "Updated Rating",
			description = f"Users can vote on files and give ratings here, the file voted on is here: {message.jump_url}"
		)
		if self.has_media_link(message):
			fieldName   = "Video URL"
			fieldValue  = f"{message.content}"
		else:
			fieldName   = "File name"
			fileName    = next(attach.filename for attach in message.attachments if attach.filename.split('.')[-1] in self.config['file_exts'])
			fieldValue  = f"{fileName}"
		embed.add_field(
			name   = fieldName,
			value  = fieldValue,
			inline = True
		)
		embed.add_field(
			name   = f"{user} rated this file",
			value  = f"{stars} stars!",
			inline = True
		)
		embed.set_footer(text="Sent by FeedBack")
		await channel.send(embed=embed)

	async def on_ready(self):
		print('Member count updated')
		print("Bot in server: {}".format("Success"))
		print("Bot name: {}".format(self.user.name))
		await self.change_presence(activity=discord.Activity(
				type = discord.ActivityType.listening,
				name = "to everyone's tunes"
		))

	async def add_rating_reactions(self, message):
		for emoji in rating_emojis:
			await message.add_reaction(emoji)

	async def retrieve_guild(self, guild_id):
		guild = self.get_guild(guild_id)
		if guild is None:
			guild = await self.fetch_guild(guild_id)
		return guild

	async def retrieve_channel(self, channel_id):
		channel = self.get_channel(channel_id)
		if channel is None:
			channel = await self.fetch_channel(channel_id)
		return channel

	async def retrieve_member(self, member_id, guild):
		member = guild.get_member(member_id)
		if member is None:
			member = await guild.fetch_member(member_id)
		return member

	def is_audio_message(self, message):
		return self.has_audio_attachment(message) or self.has_media_link(message)

	def has_audio_attachment(self, message):
		return any([attach.filename.split('.')[-1] in self.config['file_exts'] for attach in message.attachments])

	def has_media_link(self, message):
		return any([url in message.content for url in self.config['media_urls']])
