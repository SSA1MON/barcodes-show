import tkinter as tk
from tkinter import ttk, S
from PIL import Image, ImageTk
from barcode import EAN13, ITF
from barcode.writer import ImageWriter
import webbrowser
import sys


def open_github_url(event):
    webbrowser.open_new(r"https://github.com/SSA1MON/barcodes-show")


def about_help_menu():
    about_window = tk.Toplevel(padx=10, pady=10)
    about_window.focus()
    about_window.title("About")
    about_window.geometry("400x250")
    about_window.minsize(400, 250)
    about_window.maxsize(400, 250)

    title_label = ttk.Label(about_window, text="Barcodes show", font=('Verdana', 14))
    url_label = ttk.Label(about_window, text="Github", foreground='#0000EE', cursor="hand2")
    version_label = ttk.Label(about_window, text="alpha-build")
    title_label.pack()
    version_label.pack()
    url_label.pack(expand=True, anchor=S)
    url_label.bind("<Button-1>", open_github_url)


def exit_window_menu():
    sys.exit(0)


def identify_barcode_type(input_text, barcode_type=None):
    """ Определяет тип штрих-кода по полученному значению для дальнейшей генерации """
    if len(input_text) == 14:
        barcode_type = ITF
    elif len(input_text) == 13:
        barcode_type = EAN13
    return barcode_type


def generate_barcode(event):
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

        error_label.pack_forget()
        label_barcode_info.pack()
        label_barcode_info.config(text="Тип: " + str(barcode_type))
        start_barcode.image = img
        start_barcode.config(image=start_barcode.image)

        barcode_area.delete(0, tk.END)
        barcode_area.focus()
    else:
        error_label.pack()
        error_label.config(
            text="Неподдерживаемый формат",
            font=("Verdana", 12), background='#d9534f', foreground='white'
        )
        barcode_area.delete(0, tk.END)
        barcode_area.focus()
        label_barcode_info.pack_forget()
        start_barcode.config(image=default_image)


window = tk.Tk()
window.iconbitmap(default="favicon.ico")
window.title('Barcodes show')
window.geometry('650x500')
window.minsize(650, 500)
window.config(background='white')

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
start_barcode = ttk.Label(
    image=default_image, compound="top", font=('Arial', 1),
    background='white'
)
start_barcode.pack()

error_label = ttk.Label(background='white')
error_label.pack()

frame = tk.Frame(master=window, background='white')
frame.pack(expand=True)

barcode_area = tk.Entry(frame, width=39)
barcode_area.grid(row=1, column=2)
barcode_area.bind("<Return>", generate_barcode)
barcode_area.focus()

gen_btn_style = ttk.Style().configure('TButton', background='white', font=('Arial', 11))
cal_btn = ttk.Button(
    frame, text='Сгенерировать',
    command=generate_barcode, padding=7, width=28, style='TButton'
)
cal_btn.grid(row=2, column=2, pady=10)

label_barcode_info = ttk.Label(foreground='#D5CABD', background='white')
label_barcode_info.pack()

if __name__ == "__main__":
    window.config(menu=menubar)
    window.mainloop()
