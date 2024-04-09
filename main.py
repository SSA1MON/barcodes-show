import tkinter as tk
from tkinter import ttk
import sys
from PIL import Image, ImageTk
from barcode import EAN13, ITF
from barcode.writer import ImageWriter


def about_help_menu():
    about_window = tk.Toplevel(padx=10, pady=10)
    about_window.focus()
    about_window.title("About Barcodes show")
    about_window.geometry("400x250")
    about_window.minsize(400, 250)
    about_window.maxsize(400, 250)

    about_label1 = ttk.Label(about_window, text="alpha-build", font=('Verdana', 12))
    about_label2 = ttk.Label(about_window, text="Github")
    about_label1.pack()
    about_label2.pack()


def exit_window_menu():
    sys.exit(0)


def identify_barcode_type(input_text, barcode_type=None):
    """ Определяет тип штрих-кода по полученному значению для дальнейшей генерации """
    if len(input_text) == 14:
        barcode_type = ITF
    elif len(input_text) == 13:
        barcode_type = EAN13
    return barcode_type


def generate_barcode(event=None):
    """
    Генерирует штрих-код на основе введенного текста и обновляет отображение.
    Args:
        event: Костыль для срабатывания функции при нажатии <Enter>
    """
    input_text = barcode_area.get()
    barcode_type = identify_barcode_type(input_text)
    if barcode_type is not None:
        my_barcode = barcode_type(input_text, writer=ImageWriter())
        if barcode_type == ITF:
            img = my_barcode.render(writer_options={'module_width': 0.18})
        else:
            img = my_barcode.render()
        img = ImageTk.PhotoImage(img)

        label.config(text=input_text)
        label_barcode_info.config(text=str(barcode_type))
        label.image = img
        label.config(image=label.image)

        barcode_area.delete(0, tk.END)
        barcode_area.focus()
    else:
        label.config(text="Неподдерживаемый формат", font=("Arial Black", 26))
        barcode_area.delete(0, tk.END)
        barcode_area.focus()


window = tk.Tk()
window.iconbitmap(default="favicon.ico")
window.title('Barcodes show')
window.geometry('650x500')
window.minsize(650, 500)

menubar = tk.Menu(window)
window_menu = tk.Menu(menubar, tearoff=0)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.winfo_geometry()

menubar.add_cascade(label="Window", menu=window_menu)
window_menu.add_command(label="Exit", command=exit_window_menu)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about_help_menu)

default_image = Image.open("img/start_barcode.png")
default_image = ImageTk.PhotoImage(default_image)
label = ttk.Label(
    image=default_image, compound="top", font=('Arial Black', 32)
)
label.pack()

frame = tk.Frame(master=window)
frame.pack(expand=True)

barcode_area = tk.Entry(frame, width=30)
barcode_area.grid(row=1, column=2)
barcode_area.bind("<Return>", generate_barcode)
barcode_area.focus()

cal_btn = ttk.Button(
    frame, text='Сгенерировать штрих-код',
    command=generate_barcode, padding=7, width=28
)
cal_btn.grid(row=2, column=2, pady=10)

label_barcode_info = ttk.Label(foreground='#D5CABD')
label_barcode_info.pack()

if __name__ == "__main__":
    window.config(menu=menubar)
    window.mainloop()
