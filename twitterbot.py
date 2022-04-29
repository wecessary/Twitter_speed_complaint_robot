from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

SPEED_TEST_URL = "https://www.speedtest.net/"
TWITTER_URL = "https://twitter.com/"

class GotEmptySpeedValue(Exception):
    '''If the bot wrote down the speed before the website had finished loading'''
    pass


class InternetSpeedTwitterBot:
    def __init__(self, chrome_driver, twitter_email, twitter_password, twitter_username):
        self.driver = webdriver.Chrome(service=Service(chrome_driver))
        self.up = 0
        self.down = 0
        self.login = twitter_email
        self.password = twitter_password
        self.username = twitter_username

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST_URL)
        time.sleep(1.5)  # let it load
        accept_cookie = self.driver.find_element(By.CSS_SELECTOR, "#_evidon-banner-acceptbutton")  # accept cookies
        accept_cookie.click()

        time.sleep(1)
        go_button = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")  # start speed test button
        go_button.click()

        time.sleep(30)  # let it run the speed test

        while True:
            try:
                download = self.driver.find_element(By.CSS_SELECTOR,
                                                    ".result-data.u-align-left span.download-speed").text
                upload = self.driver.find_element(By.CSS_SELECTOR,
                                                  ".result-data.u-align-left span.upload-speed").text
                if download == " " or upload == " ":
                    raise GotEmptySpeedValue

            except NoSuchElementException:
                print("Exception 1 is triggered")
                time.sleep(5)

            except GotEmptySpeedValue:
                print("Exception 2 is triggered")
                time.sleep(5)

            except ElementClickInterceptedException:
                print("Exception 2 is triggered")
                close_ad = self.driver.find_element(By.CSS_SELECTOR,".notification-dismiss.close-btn")
                close_ad.click()
            else:

                speed_data = {}
                speed_data["download"] = float(download)
                speed_data["upload"] = float(upload)
                # self.driver.close()
                return speed_data

                break



    def tweet_at_provider(self, tweet):
        self.driver.get(TWITTER_URL)
        time.sleep(1)

        accept_cookies = self.driver.find_element(By.XPATH,
                                                  '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div/span/span')
        accept_cookies.click()

        login_button = self.driver.find_element(By.CSS_SELECTOR, "a[data-testid='loginButton']")
        login_button.click()

        time.sleep(1)
        email = self.driver.find_element(By.NAME, "text")
        email.send_keys(self.login)  # enter email

        next_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
        next_button.click()  # click next

        time.sleep(0.5)
        while True:
            try:
                password = self.driver.find_element(By.NAME, "password")
                password.send_keys(self.password)
                password.send_keys(Keys.ENTER)

            except NoSuchElementException:
                username = self.driver.find_element(By.NAME, "text")
                username.send_keys(self.username)
                username.send_keys(Keys.ENTER)
                time.sleep(1)

            else:
                break

        time.sleep(1)
        tweet_field = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
        # tweet_field.click()
        tweet_field.send_keys(tweet)

        tweet_button = self.driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']")
        tweet_button.click()