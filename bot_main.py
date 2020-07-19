from PyBot import PyBot
import time
import face_recognition
from PIL import Image
import os
from raw_to_final import clean_img, get_individual_face
import shutil
from CnnModel import *
import numpy as np
import random
from tqdm import tqdm
import cv2

EMAIL = PUT FB EMAIL HERE
PASSWORD = PUT FB PASSWORD HERE

#used to login with fb (google had a bot prevention, possible next project)
def login():
    bot.driver.switch_to.window(login_page)  # switching to login window
    bot.driver.find_elements_by_xpath("//*[@id='email']")[0].send_keys(bot.email)  # inputing email
    bot.driver.find_elements_by_xpath("//*[@id='pass']")[0].send_keys(bot.password)  # inputing email
    time.sleep(1)
    bot.driver.find_elements_by_xpath("//*[@id='u_0_0']")[0].click()  # loging into fb
    time.sleep(2)
    bot.driver.switch_to.window(main_page)  # switching to main page

#used to read the current image that was downloaded
def get_image():
    t_img = face_recognition.load_image_file("tinder_img.jpg")
    pil_img = Image.fromarray(t_img)
    #pil_img.show() #used for debugging
    return pil_img

#used to save images while gathering data (it would save liked images to like_raw and dislike images to dislike_raw)
def save_image(image, dir, name, number):
    image.save((r'' + dir + name).format(number+1))

#making it possible to retrain the model without having duplicates
def final_folder_refactor():
    isYes = os.path.isdir("like")
    if isYes:
        shutil.rmtree("like")
    os.mkdir("like")

    isNo = os.path.isdir("dislike")
    if isNo:
        shutil.rmtree("dislike")
    os.mkdir("dislike")

#used to gather data from within the app
def gather_data():
    choice = ""

    dir_like = "like_raw/"
    name_like = "like{}.jpg"

    dir_dislike = "dislike_raw/"
    name_dislike = "dislike{}.jpg"

    while choice != "q":
        #house keeping variables
        DISLIKE_RAW_NUM = len(os.listdir('dislike_raw/'))
        LIKE_RAW_NUM = len(os.listdir('like_raw'))

        bot.download_image()

        image = get_image()

        choice = input("q:quit \n1:like \n2:dislike\n")
        if choice == "1":
            #add image to like
            save_image(image, dir_like, name_like, LIKE_RAW_NUM)
            #click like
            bot.like()

        elif choice == "2":
            # add image to dislike
            save_image(image, dir_dislike, name_dislike, DISLIKE_RAW_NUM)
            # click dislike
            bot.dislike()
        else:
            pass

#gets an img from raw folders, finds face and adds that face to like or dislike folder. We classify based on faces
def reload_data():
    final_folder_refactor()
    r_path_like = r'like_raw/'
    r_path_dislike = r'dislike_raw/'

    dir_like = "like_raw/"
    dir_like_final = "like/"
    name_like = "like"

    dir_dislike = "dislike_raw/"
    dir_dislike_final = "dislike/"
    name_dislike = "dislike"

    time.sleep(2)
    clean_img(dir_like, dir_like_final, name_like, r_path_like)  # for like
    clean_img(dir_dislike, dir_dislike_final, name_dislike, r_path_dislike)  # for dislike


################################# Main AI usability (option 3 of bot at the bottom of this file)#########################################

### those variables cna be changed
BATCH_SIZE = 4
EPOCH = 8
IMG_SIZE = 400
###

CATEGORIES = ["like", "dislike"]
training_data = []

def main_bot():
    train_data_prep()
    # print(len(training_data))
    random.shuffle(training_data)

    # appending data to X and y and reshaping
    X = []
    y = []
    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape((-1, IMG_SIZE, IMG_SIZE, 3))
    # resize_image = tf.reshape(image, [-1, 224, 224, 3])

    X = np.array(X / 255.0)
    y = np.array(y)

    # getting model from our model class

    model = CnnModel(X, y, BATCH_SIZE, EPOCH)
    model.model_structure()
    model.model_comp()
    model.model_fit()

    choice = ""
    while choice != 'q':
        i = 0
        choice = input("q:quit\n1:run bot on 3 people\n")
        if choice == '1':
            for i in range(3): # range can be changed to how many people should bot swipe in a row while running
                #get face from current image
                bot.download_image()
                dec = get_individual_face()
                if dec == '1':
                    #img = prep_img_for_prediction()
                    #get decision (possibly need to change img so it can be evaluated
                    prediction = model.prediction([prep_img_for_prediction()])
                    print(CATEGORIES[int(prediction[0][0])])
                    d = CATEGORIES[int(prediction[0][0])]
                    # make decision
                    if d == "like":
                        #like here
                        bot.like()
                    elif d == "dislike":
                        #dislike here
                        bot.dislike()
                    else: # used for debugging
                        print("problem")
                else:
                    print("\ntoo many faces, skipping to the next one\n")
                    #dislike here
                    bot.dislike()

#used to read and prep image to be used for prediction
def prep_img_for_prediction():
    img = Image.open("tinderface_img.jpg")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img.show()
    img = np.array(img)
    return img.reshape((-1, IMG_SIZE, IMG_SIZE, 3))

#
def train_data_prep():
    for category in CATEGORIES:
        class_num = CATEGORIES.index(category)
        path = category

        for img in tqdm(os.listdir(path)):
            try:
                img_array = face_recognition.load_image_file(os.path.join(path, img))  # convert to array
                img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
                img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE)) # img size conversion
                #cv2.imshow("", img_array) #used for troubleshooting
                #cv2.waitKey() #used for troubleshooting
                training_data.append([img_array, class_num])
            except Exception as e:
                pass #for troubleshooting if needed

###############################################################################################################


if __name__ == "__main__":
    bot = PyBot(EMAIL, PASSWORD) #init bot + login

    time.sleep(3)  # waiting for pop up
    bot.click_login()

    main_page = bot.driver.current_window_handle # getting current window as main window (needed for pop up window interaction)
    time.sleep(2)

    # handling for switching website
    for handle in bot.driver.window_handles:
        if handle != main_page:
            login_page = handle

    login()
    time.sleep(3)
    bot.close_starting_pop_up()
    time.sleep(3)

    choice = ""
    data_choice = ""
    #main choice block
    while choice != "q":
        choice = input("1: Gather Data \n2: Build data from own import \n3:run bot \nq:quit\n")

        if choice == "1":
            gather_data()
        elif choice == "2":
            reload_data()
            print("finished building")
        elif choice == "3":
            main_bot()
        else:
            pass

    bot.finish()
    print("\nall done\n")