import time

name = input("Please enter your name:")
postcode = input("Please enter your postcode:")
expiry_date = input("Please enter your expiry date (eg. 02/03/18):")
original_number = input("Please enter the 8 digit number on your card (eg. 4676 4833):")
number_list = []
number_total = 0
invalid_date = False
date = time.strftime("%d%m%Y")

new_expiry_date = expiry_date[:2] + expiry_date[3:5] + expiry_date[6:]

if int(date[-2:]) >= int(new_expiry_date[-2:]):

    if int(date[-4:-2]) >= int(new_expiry_date[-4:-2]):

        if int(date[:2]) > int(new_expiry_date[:2]):
            print("INVALID EXPIRY DATE")
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
    print("====================")
    print("CARD IS VALID")
    print("{}\nat postcode {}\nwith expiry date {}\nwith card number {}\nis valid for a 10% discount".format(name, postcode, expiry_date, original_number))
    print("====================")

else:
    print("====================")
    print("CARD IS INVALID")
    print("{}\nat postcode {}\nwith expiry date {}\nwith card number {}\nis NOT valid for a 10% discount".format(name, postcode, expiry_date, original_number))
    print("====================")
            
