# Work with Python 3.6
import discord
from googletrans import Translator
import re
from iso639 import languages


class MyClient(discord.Client):
    channel_a = None
    channel_b = None
    translator = Translator(service_urls=['translate.google.com'])
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    lang_dest = 'en'

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # Don't listen to yourself.
        if message.author == client.user:
            return

        # Change language destination command in any channel
        if message.content.startswith('!lang'):
            try:
                lang = languages.get(name=message.content[6:].capitalize())
            except Exception:
                await message.channel.send('Language not found.')
                return

            self.lang_dest = lang.alpha2
            await message.channel.send('Language changed.')
            return

        # Process only source and destination channels
        if message.channel.name != '🧦ts_in_2k16_lul🧦' and message.channel.name != 'we-no-speak-no-dutchericano':
            return

        # Get channels
        if not self.channel_a or not self.channel_b:
            self.channel_b = next(filter(lambda c: c.name == 'we-no-speak-no-dutchericano',
                                       message.guild.channels))
            self.channel_a = next(filter(lambda c: c.name == '🧦ts_in_2k16_lul🧦',
                                       message.guild.channels))

        # Set destination
        dest = None
        if message.channel.name == 'we-no-speak-no-dutchericano':
            dest = self.channel_a
        if message.channel.name == '🧦ts_in_2k16_lul🧦':
            dest = self.channel_b

        # Send translated message
        if dest:
            content = re.sub('<[^>]*>', '', message.content)
            content = re.sub(self.emoji_pattern, '', content)

            embed = discord.Embed(description=self.translator.translate(content, dest=self.lang_dest).text)

            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)

            if content.strip():
                await dest.send(embed=embed)
        else:
            print('channel not found.')


client = MyClient()
client.run('NjYyNDQ4Nzk3NjE5NTg1MDY0.Xg6POQ.nyq0BJkdd9RLQaBcfQEMNoNxapQ')
