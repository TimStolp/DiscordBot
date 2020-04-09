import tweepy as tw
import asyncio
import json
from discord_bot import MyClient


class MyStreamListener(tw.StreamListener):
    def on_connect(self):
        print("Twitter: Running..")

    def on_data(self, data_raw):
        data = json.loads(data_raw)
        print(data)
        href = f"{data['user']['name']} was wakker op {data['created_at']} " \
               f"https://twitter.com/{data['user']['screen_name']}/status/{data['id_str']}"
        client = MyClient.get_client()
        channel = client.get_channel(693921819555659876)
        asyncio.run_coroutine_threadsafe(channel.send(href), client.loop)

    def on_error(self, status_code):
        print(status_code)


def start_twitter_filter(ids, app_key, app_secret, access_token, access_token_secret):
    auth = tw.OAuthHandler(app_key, app_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)

    listener = MyStreamListener()
    stream = tw.Stream(auth=api.auth, listener=listener)

    stream.filter(follow=ids, is_async=True)
