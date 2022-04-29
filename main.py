import twitterbot
import os
import random as rd

chrome_driver_path = "C:/Selenium/chromedriver.exe"
MIN_DOWN = 181
MIN_UP = 18

TWITTER_EMAIL = os.environ["twitter_email"]
TWITTER_PASSWORD = os.environ["twitter_password"]
TWITTER_USERNAME = os.environ["twitter_username"]

bot = twitterbot.InternetSpeedTwitterBot(chrome_driver=chrome_driver_path,
                                         twitter_email=TWITTER_EMAIL,
                                         twitter_password= TWITTER_PASSWORD,
                                         twitter_username= TWITTER_USERNAME)

speed_data = bot.get_internet_speed()

# determine what the bot will write based on the internet data

if speed_data["download"] < MIN_DOWN or speed_data["upload"] < MIN_UP:
    text_to_tweet = f"Not cool... I paid for minimum {MIN_DOWN}down/{MIN_UP}up," \
                    f" what I am getting is {speed_data['download']}down/{speed_data['upload']}up"

elif speed_data["download"] > MIN_DOWN and speed_data["upload"] > MIN_UP:
    text_to_tweet = f"Cool... I paid for minimum {MIN_DOWN}down/{MIN_UP}up," \
                    f" what I am getting is even better: {speed_data['download']}down/{speed_data['upload']}up "


bot.tweet_at_provider(text_to_tweet)

