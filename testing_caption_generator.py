from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.applications.xception import Xception
from keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import argparse
import tkinter as tk
from tkinter import filedialog


def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text


def upload_img():
    global img,image_data
    for img_display in frame.winfo_children():
        img_display.destroy()

    image_data = filedialog.askopenfilename(initialdir="/", title="Choose an image", 
                                        filetypes=(("all files","*.*"),("jpg files","*.jpg")))
    img = Image.open(image_data)
    img = img.resize((500, 450),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel_image = tk.Label(frame, image=img).pack()

def caption():

    max_length = 32
    tokenizer = load(open("tokenizer.p","rb"))
    model = load_model('models/model_9.h5')
    xception_model = Xception(include_top=False, pooling="avg")

    photo = extract_features(image_data, xception_model)
    img = Image.open(image_data)

    description = generate_desc(model, tokenizer, photo, max_length)
    description = description[6:-4]
    description = description.capitalize() + '.'

    table = tk.Label(frame, text="Caption: "+description, font=("Helvetica",12)).pack()

def quit_me():
    root.quit()
    root.destroy()


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", quit_me)
root.title('Image Caption Generator')
tit = tk.Label(root, text="Image Caption Generator", padx=25, pady=6, font=("",12)).pack()  
canvas = tk.Canvas(root, height=600, width=600, bg='#D1EDf2')
canvas.pack()
frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
chose_image = tk.Button(root, text='Choose Image' , padx=35, pady=10, fg="black", bg="pink", command=upload_img, activebackground="#add8e6")
chose_image.pack(side=tk.LEFT)
caption_image = tk.Button(root, text='Show Caption' , padx=35, pady=10, fg="black", bg="pink", command=caption, activebackground="#add8e6")
caption_image.pack(side=tk.RIGHT)
root.mainloop() 