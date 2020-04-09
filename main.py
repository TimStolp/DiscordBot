# Works with Python = 3.6
import os
from dotenv import load_dotenv
from twitter_listener import start_twitter_filter
from discord_bot import start_discord_bot


if __name__ == '__main__':
    load_dotenv()
    start_twitter_filter(["1244023151580917760", "1244343874816036865"],
                         os.getenv('APP_KEY'), os.getenv('APP_SECRET'),
                         os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
    start_discord_bot(os.getenv('DISCORD_TOKEN'))
