import hashlib
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np


def get_sha_key(key):
    sha_key = hashlib.sha256(key.encode()).hexdigest()
    return sha_key


def process_image():
    key = get_sha_key(key_entry.get())
    operation = var.get()
    if image_path and key:
        img = Image.open(image_path)
        img_array = np.array(img)
        print(img_array)
        flat_img_array = img_array.flatten()
        print(flat_img_array)
        np.random.seed(sum(map(ord, key)))
        print(np.random.seed(sum(map(ord, key))))
        perm = np.random.permutation(len(flat_img_array))
        print(perm)
        np.random.seed()
        if operation == 'Encode':
            scrambled_array = flat_img_array[perm]
        else:
            scrambled_array = flat_img_array[np.argsort(perm)]
        new_img_array = scrambled_array.reshape(img_array.shape)
        new_img = Image.fromarray(new_img_array.astype('uint8'))
        new_img.save(image_path)
        img_label.config(text="Process Completed: " +
                         operation + " Using Key: " + key)
        # Update the result image label
        new_img.thumbnail((200, 200))

        result_img = ImageTk.PhotoImage(new_img)
        result_img_label.config(image=result_img)
        result_img_label.image = result_img
        process_btn.config(state='disabled')


def upload_image():
    global image_path
    image_path = filedialog.askopenfilename()
    if image_path:
        img_label.config(text="Image Loaded: " + image_path.split('/')[-1])
        # Load the image and display it in a Label widget
        img = Image.open(image_path)
        img.thumbnail((200, 200))
        result_img = ImageTk.PhotoImage(img)
        result_img_label.config(image=result_img)
        result_img_label.image = result_img
        process_btn.config(state='normal')


root = tk.Tk()
root.title("Image Scrambler")
root.configure(bg='white')
style = {'font': ('Helvetica', 12), 'bg': 'white'}

key_label = tk.Label(root, text="Enter Key:", **style)
key_label.pack(pady=5)

key_entry = tk.Entry(root, **style)
key_entry.pack(pady=5)

var = tk.StringVar(value='Encode')

operation_label = tk.Label(root, text="Select Operation:", **style)
operation_label.pack(pady=5)

encode_radio = tk.Radiobutton(
    root, text="Encode", variable=var, value='Encode', **style)
encode_radio.pack()
decode_radio = tk.Radiobutton(
    root, text="Decode", variable=var, value='Decode', **style)
decode_radio.pack()

upload_btn = tk.Button(root, text="Upload Image",
                       command=upload_image, **style)
upload_btn.pack(pady=10)

process_btn = tk.Button(root, text="Process Image",
                        command=process_image, **style, state='disabled')
process_btn.pack(pady=10)

img_label = tk.Label(root, text="No Image Loaded", wraplength=200, **style)
img_label.pack(pady=10)

# Add a new label widget for the result image
result_img_label = tk.Label(root, **style)
result_img_label.pack(pady=10)

root.mainloop()
