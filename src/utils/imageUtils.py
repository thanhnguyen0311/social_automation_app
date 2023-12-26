import tkinter as tk
from PIL import ImageTk, Image
import base64


def RBGAImage(path):
    return Image.open(path).convert("RGBA")


def resize_image(img, width, height, canvas, canvas_image):
    image = img.resize((width, height))
    tk_image = ImageTk.PhotoImage(image)
    canvas.itemconfig(canvas_image, image=tk_image)
    canvas.image = tk_image


def show_image(frame, path, width, height):
    im = RBGAImage(path)
    tk_image = ImageTk.PhotoImage(im)
    canvas = tk.Canvas(frame, bg="lightblue", highlightthickness=0, width=width, height=height)
    canvas.pack(fill=tk.BOTH)
    canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    canvas.bind("<Configure>", resize_image(im, width, height, canvas, canvas_image))
    return canvas


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode("utf-8")


def find_image_from_image():
    return