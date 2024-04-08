import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from barcode import Code39
from barcode.writer import ImageWriter


# TODO: rework
BARCODE_TYPE = Code39


# def about_help_menu():
#     about_window = tk.Toplevel(padx=10, pady=10)
#     about_window.focus()
#     about_window.title("About Barcodes show")
#     about_window.geometry("400x250")
#     about_window.minsize(400, 250)
#     about_window.maxsize(400, 250)
#
#     about_label1 = ttk.Label(about_window, text="alpha-build", font=('Verdana', 12))
#     about_label2 = ttk.Label(about_window, text="Github")
#     about_label1.pack()
#     about_label2.pack()


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

# menubar = tk.Menu(window)
# help_menu = tk.Menu(menubar, tearoff=0)
# help_menu.winfo_geometry()
# help_menu.add_command(label="About", command=about_help_menu)
# menubar.add_cascade(label="Help", menu=help_menu)

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

if __name__ == "__main__":
    # window.config(menu=menubar)
    window.mainloop()
