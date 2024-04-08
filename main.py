import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from barcode import Code39
from barcode.writer import ImageWriter


# TODO: rework
BARCODE_TYPE = Code39


def generate_barcode(event=None):
    """
    Генерирует штрих-код на основе введенного текста и обновляет отображение.
    Args:
        event: Костыль для срабатывания функции при нажатии <Enter>
    """
    input_text = barcode_area.get()
    my_barcode = BARCODE_TYPE(input_text, writer=ImageWriter())
    img = my_barcode.render()
    img = ImageTk.PhotoImage(img)

    label.config(text=input_text)
    label.image = img
    label.config(image=label.image)

    barcode_area.delete(0, tk.END)
    barcode_area.focus()


window = tk.Tk()
window.iconbitmap(default="favicon.ico")
window.title('Barcodes show')
window.geometry('650x500')
window.minsize(650, 500)

default_image = Image.open("img/start_barcode.png")
default_image = ImageTk.PhotoImage(default_image)
label = ttk.Label(
    image=default_image, text="BARCODE NUMBER",
    compound="top", font=('Arial Black', 32)
)
label.pack()

frame = tk.Frame(master=window)
frame.pack(expand=True)

barcode_area = tk.Entry(frame, width=30)
barcode_area.grid(row=1, column=2)
barcode_area.bind("<Return>", generate_barcode)
barcode_area.focus()

cal_btn = ttk.Button(frame, text='Generate barcode', command=generate_barcode, padding=7, width=28)
cal_btn.grid(row=2, column=2, pady=10)

window.mainloop()
