from tkinter import *

root = Tk()

input_entry = Entry(root, font=("Arial", 18), width=30, border=0, justify="right")
input_entry.grid(row=0, column=0, columnspan=3)


def button_clear():
    input_entry.delete(0, END)


def click(number):
    current = input_entry.get()
    input_entry.delete(0, END)
    input_entry.insert(0, str(current) + str(number))


def add():
    num1 = input_entry.get()
    global add_num
    add_num = int(num1)
    input_entry.delete(0, END)

def subtract():
    num1 = input_entry.get()
    global sub_num
    sub_num = int(num1)
    input_entry.delete(0, END)


def equal():
    num2 = input_entry.get()
    input_entry.delete(0, END)
    number1 = int(add_num)
    number2 = int(num2)
    input_entry.insert(0, number1 + number2)


button1 = Button(root, text=1, width=10, height=3, border=0, command=lambda: click(1))
button2 = Button(root, text=2, width=10, height=3, border=0, command=lambda: click(2))
button3 = Button(root, text=3, width=10, height=3, border=0, command=lambda: click(3))
button4 = Button(root, text=4, width=10, height=3, border=0, command=lambda: click(4))
button5 = Button(root, text=5, width=10, height=3, border=0, command=lambda: click(5))
button6 = Button(root, text=6, width=10, height=3, border=0, command=lambda: click(6))
button7 = Button(root, text=7, width=10, height=3, border=0, command=lambda: click(7))
button8 = Button(root, text=8, width=10, height=3, border=0, command=lambda: click(8))
button9 = Button(root, text=9, width=10, height=3, border=0, command=lambda: click(9))
button0 = Button(root, text=0, width=10, height=3, border=0, command=lambda: click(0))

clear = Button(root, text="C", width=10, height=3, border=0, command=lambda: button_clear())
button_dot = Button(root, text=".", width=10, height=3, border=0)
button_plus = Button(root, text="+", width=10, height=3, border=0, command=add)
button_minus = Button(root, text="-", width=10, height=3, border=0)
button_divide = Button(root, text="/", width=10, height=3, border=0)
button_multiply = Button(root, text="*", width=10, height=3, border=0)
button_equal = Button(root, text="=", width=10, height=3, border=0, command=equal)

button7.grid(row=1, column=0)
button8.grid(row=1, column=1)
button9.grid(row=1, column=2)

button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)

button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)

button0.grid(row=4, column=0, )
button_dot.grid(row=4, column=1)
button_equal.grid(row=4, column=2)

clear.grid(row=0, column=3)
button_plus.grid(row=1, column=3)
button_minus.grid(row=2, column=3)
button_multiply.grid(row=3, column=3)
button_divide.grid(row=4, column=3)

root.mainloop()
