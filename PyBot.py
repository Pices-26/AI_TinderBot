from selenium import webdriver
from PIL import Image
import cv2
from io import BytesIO
import requests
import numpy as np

class PyBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get('https://tinder.com/')

    #for liking profile
    def like(self):
        self.driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')[0].click()

    #for disliking profile
    def dislike(self):
        self.driver.find_elements_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')[0].click()

    #for closing a pop up at the start
    def close_starting_pop_up(self):
        self.driver.find_elements_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/button[1]/span")[0].click()  # closing pop up
        self.driver.find_elements_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/button[1]")[0].click()  # closing pop up

    #for closing session with a webdriver
    def finish(self):
        self.driver.close()

    #for clicking the login button
    def click_login(self):
        self.driver.find_elements_by_xpath("//*[@id='modal-manager']/div/div/div/div/div[3]/span/div[2]/button")[0].click()  # clicing login button

    #for downloading main image
    def download_image(self):
        img = self.driver.find_elements_by_xpath("//*[@id='content']/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div")[0]  # getting path to img
        image_url = img.value_of_css_property("background-image")
        raw_url = image_url.replace('url("', '').replace('")', '')
        resp = requests.get(raw_url)
        # convert raw url to image
        image = Image.open(BytesIO(resp.content)).convert("RGB")
        # converting to numpy array so it works with open cv
        image = np.array(image)
        # converting to proper rgb
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("tinder_img.jpg", image)