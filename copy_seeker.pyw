from time import sleep
from pynput import keyboard
from tkinter import Tk, Button, Label, BOTTOM, X
from threading import Thread

import os

APP_NAME = "Copy Seeker"

THREADS = []
COPY_SEEKER_TEXT_LIST = []
current_keys = set()

COPY_SEEKER_UI = ["c", "s", "u"]
COPY_SEEKER_CLEAN = ["c", "s", "t"]
COPY_SEEKER_KILL = ["c", "s", "k"]


def copy_text(text):
    root = Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()


def get_ui():
    app = Tk()
    app.title(APP_NAME)
    app.minsize(600, 200)
    app.configure(bg='grey')
    for idx, text in enumerate(COPY_SEEKER_TEXT_LIST):
        Button(app, text=text, command=lambda sendtex=text: copy_text(sendtex)).pack(fill=X)
    Button(app, text="Developed By: furkanozkaya.com", bg="black", fg="white").pack(side=BOTTOM, fill=X)
    Button(app, text="Idea Owner: sinanaktepe.com", bg="black", fg="white").pack(side=BOTTOM, fill=X)

    app.lift()
    app.attributes('-topmost', True)
    app.after_idle(app.attributes, '-topmost', False)
    app.mainloop()


def close_app():
    app = Tk()
    app.title(APP_NAME)
    app.minsize(400, 200)
    Label(app, text=f"{APP_NAME} will not listen your copied text after 3 second that this window close").pack(fill=X)
    Label(app, text=f"Made By: Furkan Ozkaya", bg="black", fg="white").pack(side=BOTTOM, fill=X)
    app.lift()
    app.attributes('-topmost', True)
    app.after_idle(app.attributes, '-topmost', False)
    app.after(3000, lambda: quit(app))
    app.mainloop()


def quit(app):
    app.destroy()
    os._exit(0)


def on_press(key):
    try:
        if type(key) == keyboard._win32.KeyCode:
            key = key.char
        else:
            key = key.name
        current_keys.add(key)
        current_key_list = list(current_keys)
        [x.lower() for x in current_key_list]
        if len(current_key_list) >= 3:
            if all(command in current_key_list for command in COPY_SEEKER_UI):
                current_keys.clear()
                Thread(target=get_ui).start()
            elif all(command in current_key_list for command in COPY_SEEKER_CLEAN):
                current_keys.clear()
                COPY_SEEKER_TEXT_LIST.clear()
            elif all(command in current_key_list for command in COPY_SEEKER_KILL):
                current_keys.clear()
                close_app()
    except:
        pass


def on_release(key):
    try:
        if type(key) == keyboard._win32.KeyCode:
            key = key.char
        else:
            key = key.name
        current_keys.remove(key)
        for c in current_keys:
            if c.startswith('\\'):
                current_keys.remove(c)
    except:
        pass


def clipboard_listener():
    app = Tk()
    while True:
        try:
            data = app.clipboard_get()
            data = data.strip()
            if data:
                if all(data.replace("\n", " ") != text.replace("\n", " ") for text in COPY_SEEKER_TEXT_LIST):
                    if len(COPY_SEEKER_TEXT_LIST) >= 5:
                        COPY_SEEKER_TEXT_LIST.pop(0)
                    COPY_SEEKER_TEXT_LIST.append(data.strip())
            sleep(0.1)
        except:
            sleep(0.2)


def main():
    clipboard = Thread(target=clipboard_listener)
    clipboard.setDaemon(True)
    clipboard.start()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()
