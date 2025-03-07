
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Haken\Downloads\Tkinter-Designer-master\Tkinter-Designer-master\Dossier3\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1920x1080")

window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 1080,
    width = 1920,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1920.0,
    1080.0,
    fill="#D9D9D9",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    960.0,
    540.0,
    image=image_image_1
)

canvas.create_rectangle(
    516.0,
    73.0,
    1440.0,
    258.0,
    fill="#1A0350",
    outline="")

canvas.create_text(
    681.0,
    84.0,
    anchor="nw",
    text="ŒSTRO-GEN",
    fill="#FFFFFF",
    font=("Khmer", 96 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=666.0,
    y=430.0,
    width=623.0,
    height=112.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=726.0,
    y=556.0,
    width=503.0,
    height=115.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1627.0,
    677.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    429.0,
    903.0,
    image=image_image_3
)

canvas.create_rectangle(
    109.0,
    278.0,
    379.0,
    530.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    294.0,
    339.0,
    anchor="nw",
    text="L",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    125.0,
    339.0,
    anchor="nw",
    text="Aymeric",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    125.0,
    384.0,
    anchor="nw",
    text="Yann",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    125.0,
    432.0,
    anchor="nw",
    text="Damien",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    125.0,
    476.0,
    anchor="nw",
    text="Nathan",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    294.0,
    384.0,
    anchor="nw",
    text="G",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    294.0,
    432.0,
    anchor="nw",
    text="B",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    294.0,
    476.0,
    anchor="nw",
    text="R",
    fill="#000000",
    font=("RobotoSlab Black", 36 * -1)
)

canvas.create_text(
    125.0,
    294.0,
    anchor="nw",
    text="Made by  :",
    fill="#000000",
    font=("RobotoSlab Bold", 36 * -1)
)
window.resizable(True, True)
window.mainloop()