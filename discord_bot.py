import discord
import googletrans
import re


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyClient(discord.Client, metaclass=Singleton):
    comm = '!'
    translator = googletrans.Translator(service_urls=['translate.google.com'])
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    lang_dest = 'en'
    languages = {v: k for k, v in googletrans.LANGUAGES.items()}
    help_message = "**help:** Shows available commands.\n" \
                   "**languages:** Shows available languages.\n" \
                   "**lang:** Changes destination language.\n" \
                   "**uitroepteken:** Changes command symbol.\n"

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                               name=f"Command symbol {self.comm}"))
        print('Discord: Running..')

    async def on_message(self, message):
        # Don't listen to yourself.
        if message.author == self.user:
            return

        if message.content.startswith(f'{self.comm}shutdown') and str(message.author) == 'Volts#5839':
            await self._shutdown(message)
            return

        # Sends help message.
        if message.content.startswith(f'{self.comm}help'):
            await self._help(message)
            return

        # Shows available languages.
        if message.content.startswith(f'{self.comm}languages'):
            await self._show_languages(message)
            return

        # Changes language destination command in any channel.
        if message.content.startswith(f'{self.comm}lang'):
            await self._change_lang(message)
            return

        # Changes command symbol.
        if message.content.startswith(f'{self.comm}uitroepteken'):
            await self._change_symbol(message)
            return

        # Processes only source and destination channels.
        if message.channel == self.get_channel(244536836737728512) or \
                message.channel == self.get_channel(662468963510255670):
            await self._translate_message(message)
            return

    @staticmethod
    def get_client():
        return MyClient()

    async def _shutdown(self, message):
        print('Shutting down.')
        await message.channel.send('Shutting down.')
        await self.close()

    async def _help(self, message):
        await message.channel.send(
            embed=discord.Embed(description=self.help_message, title='Commands'))
        return

    async def _show_languages(self, message):
        await message.channel.send(embed=discord.Embed(
            description=', '.join(map(lambda x: x.capitalize(),
                                      {v: k for k, v in googletrans.LANGUAGES.items()}.keys())),
            title='Possible languages'))
        return

    async def _change_lang(self, message):
        if message.content == f'{self.comm}lang':
            await message.channel.send(
                f'Current channel language is {googletrans.LANGUAGES[self.lang_dest].capitalize()}')
            return
        try:
            self.lang_dest = self.languages[
                message.content[len(f'{self.comm}lang') + 1:].lower()]
        except Exception:
            await message.channel.send('Language not found.')
            return

        await message.channel.send(
            f"Language changed to {message.content[len(f'{self.comm}lang')+1:].capitalize()}.")
        return

    async def _change_symbol(self, message):
        if message.content == f'{self.comm}uitroepteken':
            await message.channel.send(f"usage: '{self.comm}uitroepteken command_symbol'")
            return

        if len(message.content[len(f'{self.comm}uitroepteken') + 1:]) > 100:
            await message.channel.send('Command symbol too long. (max 100 characters)')
            return

        if ' ' in message.content[len(f'{self.comm}uitroepteken') + 1:]:
            await message.channel.send('Command symbol cannot contain spaces.')
            return

        self.comm = message.content[len(f'{self.comm}uitroepteken') + 1:]
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name=f"Command symbol {self.comm}"))
        await message.channel.send(f"Changed command symbol to '{self.comm}'.")
        return

    async def _translate_message(self, message):
        # Set destination.
        dest = None
        if message.channel.name == 'we-no-speak-no-dutchericano':
            dest = self.get_channel(244536836737728512)
        if message.channel.name == '🧦ts_in_2k16_lul🧦':
            dest = self.get_channel(662468963510255670)

        # Send translated message.
        content = re.sub('<[^>]*>', '', message.content)
        content = re.sub(self.emoji_pattern, '', content)

        embed = discord.Embed(
            description=self.translator.translate(content, dest=self.lang_dest).text)

        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)

        if content.strip():
            await dest.send(embed=embed)


def start_discord_bot(token):
    client = MyClient()
    client.run(token)
