# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import cv2
# from tqdm import tqdm
# import random
# from CnnModel import *
# import tensorflow as tf
# from bot_main import *
# from raw_to_final import *
# import face_recognition
# from bot_main import bot
#
# BATCH_SIZE = 2
# EPOCH = 5
# IMG_SIZE = 400
# CATEGORIES = ["like", "dislike"]
# training_data = []
#
# def main_bot():
#     train_data_prep()
#     # print(len(training_data))
#     random.shuffle(training_data)
#
#     # appending data to X and y and reshaping
#     X = []
#     y = []
#     for features, label in training_data:
#         X.append(features)
#         y.append(label)
#
#     X = np.array(X).reshape((-1, IMG_SIZE, IMG_SIZE, 3))
#     # resize_image = tf.reshape(image, [-1, 224, 224, 3])
#
#     X = np.array(X / 255.0)
#     y = np.array(y)
#
#     # getting model from our model class
#
#     model = CnnModel(X, y, BATCH_SIZE, EPOCH)
#     model.model_structure()
#     model.model_comp()
#     model.model_fit()
#
#     choice = ""
#     while choice != 'q':
#         i = 0
#         choice = input("q:quit\n1:run bot on 3 people\n")
#         if choice == '1':
#             for i in range(3):
#                 #get face from current image
#                 dec = get_individual_face()
#                 if dec == '1':
#                     #img = prep_img_for_prediction()
#                     #get decision (possibly need to change img so it can be evaluated
#                     prediction = model.prediction([prep_img_for_prediction()])
#                     print(CATEGORIES[int(prediction[0][0])])
#                     d = CATEGORIES[int(prediction[0][0])]
#                     # make decision
#                     if d == "like":
#                         #like here
#                         bot.like()
#                     else:
#                         #dislike here
#                         bot.dislike()
#                 else:
#                     print("\ntoo many faces, skipping to the next one\n")
#                     #dislike here
#                     bot.dislike()
#
# def prep_img_for_prediction():
#     img = Image.open("tinderface_img.jpg")
#     #img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
#     #img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
#     img = img.resize((IMG_SIZE, IMG_SIZE))
#     img.show()
#     #print(img.reshape((-1, IMG_SIZE, IMG_SIZE, 3)))
#     img = np.array(img)
#     return img.reshape((-1, IMG_SIZE, IMG_SIZE, 3))
#
#
#
# def train_data_prep():
#     for category in CATEGORIES:
#         class_num = CATEGORIES.index(category)
#         path = category
#
#         for img in tqdm(os.listdir(path)):
#             try:
#                 img_array = face_recognition.load_image_file(os.path.join(path, img))  # convert to array
#                 img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
#                 img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE)) # img size conversion
#                 #cv2.imshow("", img_array)
#                 #cv2.waitKey()
#                 #img_array = tf.reshape(img_array, [-1,IMG_SIZE,IMG_SIZE,3])
#
#                 training_data.append([img_array, class_num])
#             except Exception as e:
#                 pass #for troubleshooting if needed
