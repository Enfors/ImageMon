#!/usr/bin/env python3

"""
ImageMon by Christer Enfors 2021. Released under GPL version 3.

Run this program while playing Minecraft Java Edition. If you make a
screenshot from inside Minecraft with the F2 key, this program will
display that screenshot in a separate window.
"""

from os import listdir
from os.path import isfile, join, expanduser
import time
import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError


def main():
    root = tk.Tk()

    # Get the path to the directory where Minecraft stores screenshots.
    # In Linux, it's ~/.minecraft/screenshots, and in Windows it's
    # %appdata%\.minecraft\screenshots.
    # Using expanduser("~"), we get the first part - the home directory.
    # Using join, we can then concatenate that with the remaining parts
    # of the path to get the full path in a portable way.

    path = join(expanduser("~"), ".minecraft", "screenshots")

    old_list = get_screenshot_list(path)
    old_img = None

    try:
        while True:
            time.sleep(.1)
            new_list = get_screenshot_list(path)

            new_files = [f for f in new_list if f not in old_list]

            if new_files:
                old_img = show_image(join(path, new_files[0]), old_img)

            old_list = new_list.copy()

            try:
                root.update()
            except tk.TclError:
                # The user has probably closed the window. Just exit.
                return

    except KeyboardInterrupt:
        return


def get_screenshot_list(path: str):
    files = [f for f in listdir(path) if isfile(join(path, f)) and
             f.endswith(".png")]
    return files


def show_image(img_path: str, old_img: tk.Label):

    if old_img:
        old_img.pack_forget()

    image_loaded = False

    while image_loaded is not True:
        try:
            image = Image.open(img_path)
            image_loaded = True
        except UnidentifiedImageError:
            # We just noticed that the file is there, but loading it
            # fails. Why? Probably because it is still in the process
            # of being created, which could take a second. So, let's
            # give it exactly that - a second, then try again.
            time.sleep(1)

    # Change 'width' to make the window a suitable size for your
    # particular screen resolution.
    width = 1670

    resized_image = image.resize((width, width*9//16))

    img = ImageTk.PhotoImage(resized_image)

    label1 = tk.Label(image=img)
    label1.image = img
    label1.pack()

    return label1


if __name__ == "__main__":
    main()
