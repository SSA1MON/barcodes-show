from tkinter import *
from tkinter import ttk
from io import BytesIO
from barcode import Code39
from barcode.writer import ImageWriter
from io import BytesIO


MY_CODE = Code39


def generate_barcode():
    """
    Временное описание:
    Берет строку из поля ввода, генерирует штрих-код, сохраняет его как файл,
    изменяет label на данные из строки, обновляет переменную с изображением,
    удаляет текст из поля ввода и фокусирует курсор на нем.
    """
    global python_logo
    input_barcode = barcode_area.get()
    my_barcode = MY_CODE(input_barcode, writer=ImageWriter())
    my_barcode.save(f'img/{input_barcode}_barcode')

    fp = BytesIO()
    my_barcode.write(fp)

    with open(f"img/{input_barcode}_barcode.png", "wb") as f:
        my_barcode.write(f)

    label["text"] = input_barcode

    barcode_img = PhotoImage(file=f"img/{input_barcode}_barcode.png", width=650)
    label.image = barcode_img
    label['image'] = label.image

    barcode_area.delete(0, END)
    barcode_area.focus()


window = Tk()
window.title('Barcodes show')
window.geometry('650x500')

python_logo = PhotoImage(file="img/start_barcode.png")
label = ttk.Label(image=python_logo, text="YOUR BARCODE IS HERE", compound="top", font=('Arial Black', 32))
label.pack()

frame = Frame(master=window, relief=SUNKEN, borderwidth=2)
frame.pack(expand=True)

barcode_area = Entry(frame, width=90)
barcode_area.grid(row=1, column=2)
barcode_area.focus()


cal_btn = ttk.Button(frame, text='Generate barcode', command=generate_barcode)
cal_btn.grid(row=2, column=2, pady=10)

label2 = ttk.Label(frame, text="213312321", compound="top")
label2.grid(row=3, column=2)

if __name__ == '__main__':
    window.mainloop()
