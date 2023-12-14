import tkinter as tk
from itertools import cycle


def update_label(new_text):
    blinking_label.config(text=new_text)


def blink():
    if next(blink_iter):
        blinking_label.config(fg='black')
    else:
        blinking_label.config(fg='white')
    root.after(500, blink)


root = tk.Tk()
root.title("Blinking Label App")

blinking_label = tk.Label(root, text="Click a button", font=('Helvetica', 16))
blinking_label.pack(pady=20)

button1 = tk.Button(root, text="Button 1", command=lambda: update_label("Text for Button 1"))
button1.pack(side=tk.LEFT, padx=10)

button2 = tk.Button(root, text="Button 2", command=lambda: update_label("Text for Button 2"))
button2.pack(side=tk.RIGHT, padx=10)

blink_iter = cycle([True, False])
blink()

root.mainloop()
