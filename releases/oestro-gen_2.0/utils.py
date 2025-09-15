from tkinter import Frame, Label
from PIL import Image, ImageTk

def error_handler(root, message):
    frame_error = Frame(root, width=500, height=60, bg="red")
    frame_error.place(x=0, y=0)
    frame_error.lift()

    label_error = Label(frame_error, text=message, background="red", foreground="white", font=("Khmer", 15))
    label_error.place(x=10, y=5)

    root.after(5000, frame_error.place_forget)

def change_validate(root, message):
    frame_validate = Frame(root, width=500, height=60, bg="green")
    frame_validate.place(x=0, y=0)
    frame_validate.lift()

    label_validate = Label(frame_validate, text=message, background="green", foreground="white", font=("Khmer", 15))
    label_validate.place(x=10, y=5)

    root.after(5000, frame_validate.place_forget)

def resize_image(image_path, width, height):
    """Resize the image to fit the specified dimensions."""
    img = Image.open(image_path)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)