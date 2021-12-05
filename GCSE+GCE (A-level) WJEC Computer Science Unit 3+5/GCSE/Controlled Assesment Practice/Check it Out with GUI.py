from tkinter import *
from tkinter import ttk
import time


def check():
    name = name_fieldvar.get()
    postcode = post_fieldvar.get()
    expiry_date = date_fieldvar.get()
    original_number = num_fieldvar.get()
    number_list = []
    number_total = 0
    invalid_date = False
    date = time.strftime("%d%m%Y")
    valid = ""

    new_expiry_date = expiry_date[:2] + expiry_date[3:5] + expiry_date[6:]

    if int(date[-4:]) >= int(new_expiry_date[-4:]):

        if int(date[-6:-4]) >= int(new_expiry_date[-6:-4]):

            if int(date[:2]) > int(new_expiry_date[:2]):
                invalid_date = True

    number = original_number[:4] + original_number[5:]
        
    check_digit = int(number[7])

    number = number[:7]
    number = number[::-1]

    for i in range(7):
        number_list.append(int(number[i]))

    for i in range(7):
        if (i + 1) % 2 == 1:
            number_list[i] *= 2
            if number_list[i] > 9:
                number_list[i] -= 9

    for digit in number_list:
        number_total += digit

    number_total += check_digit

    if number_total % 10 == 0 and invalid_date == False:
        valid = "VALID"

    else:
        valid = "INVALID"

    result.set("{}\n{} - {} - {} - {}".format(valid, name, postcode, expiry_date, original_number))


root = Tk()
root.geometry("350x225")
root.title("Main Window")

name_label = ttk.Label(root, text="Enter name:", justify="center")
name_label.pack()

name_fieldvar = StringVar()
name_field = ttk.Entry(root, textvariable=name_fieldvar, width=50, justify="center")
name_field.pack()

post_label = ttk.Label(root, text="Enter postcode:", justify="center")
post_label.pack()

post_fieldvar = StringVar()
post_field = ttk.Entry(root, textvariable=post_fieldvar, width=50, justify="center")
post_field.pack()

date_label = ttk.Label(root, text="Enter date (eg. 23/09/2017):", justify="center")
date_label.pack()

date_fieldvar = StringVar()
date_field = ttk.Entry(root, textvariable=date_fieldvar, width=50, justify="center")
date_field.pack()

num_label = ttk.Label(root, text="Enter 8-digit code (eg. 1234 5678):", justify="center")
num_label.pack()

num_fieldvar = StringVar()
num_field = ttk.Entry(root, textvariable=num_fieldvar, width=50, justify="center")
num_field.pack()

result = StringVar()
result.set("Press Enter\nwhen complete")
result_label = ttk.Label(root, textvariable=result, justify="center")
result_label.pack()

submit_button = ttk.Button(root, text="Enter", command=check)
submit_button.pack()

root.mainloop()    
