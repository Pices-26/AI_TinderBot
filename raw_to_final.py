import os
import face_recognition
from PIL import Image
#import cv2
from tqdm import tqdm

#extracts face from image + saves to corresponding directory
def clean_img(dir_from,dir_to, name, r_path):
    i=0
    for image in tqdm(os.listdir(dir_from)):
        image = face_recognition.load_image_file(os.path.join(r_path, image))
        get_face = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")
        if len(get_face) == 1:
            for face in get_face:
                top, right, bottom, left = face
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                pil_image.save((r'' +dir_to + name+'{}.jpg').format(i))
            i+=1

#used while making decision if model should guess based on the profile
def get_individual_face():
    img = t_img = face_recognition.load_image_file("tinder_img.jpg")
    face_locations = face_recognition.face_locations(t_img, number_of_times_to_upsample=0, model="cnn")
    if len(face_locations) == 1: #we don't want more than 1 face or less than 1 face
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = img[top:bottom, left:right]
            img = Image.fromarray(face_image)
            img.save("tinderface_img.jpg")
        dec = "1"
        return dec
    else:
        dec = "0"
        return dec