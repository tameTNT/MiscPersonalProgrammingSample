# imports the main tkinter module needed for the GUI
from tkinter import *
# imports the ttk library for standardized GUIs across OSs
from tkinter import ttk
# tkinter.messagebox is used for confirmations in the program
from tkinter import messagebox

# Stores all the customer objects under the customer's name. This is used to check if a customer has made a booking before
customer_dict = {}

# The discount type dictates what operations are done to the price later in the program
discount_type = 0  # Key: 0=no discount; 1=half price; 2=free


# The customer class stores the customer's name (self.name),  their bookings (self.bookings) and how many bookings they have made (self.booking_count)
class Customer:
    def __init__(self, name):
        self.bookings = {}
        self.name = name
        self.booking_count = 0

    # The self.booking() method creates a booking storing the date and group size for the customer, adding it it the self.booking dictionary to reference later
    def booking(self, date, people):
        self.bookings[str(date)] = int(people)


# The checks function goes through
def checks():
    global discount_type  # Discount type is changed in this function depending on a customer's previous bookings

    discount_type = 0

    customer_name_var.set(customer_name_var.get().capitalize())  # Capitalizes the customer's name to prevent the program not recognising the customer in later bookings due to a 'different' name

    # Checks if all the Entry Fields are actually filled to prevent errors later
    if customer_name_var.get() == "":
        errors.set("A required field(s) was left blank.")
        return
    if date_var.get() == "":
        errors.set("A required field(s) was left blank.")
        return
    if people_var.get() == "":
        errors.set("A required field(s) was left blank.")
        return

    # Checks that the value for people and date are entered correctly
    try:
        int(people_var.get())  # The people tkinter variable should be able to be converted into an integer
    except ValueError:
        errors.set("You have not entered an Integer for 'People'")
        return

    if date_var.get()[2] != "/":  # Checks that the forward slashes are in the correct place
        errors.set("Date not in format DD/MM/YYYY")
        return
    if date_var.get()[5] != "/":
        errors.set("Date not in format DD/MM/YYYY")
        return
    if len(date_var.get()) != 10:  # Checks if the length of the date string is correct
        errors.set("Date not in format DD/MM/YYYY")
        return

    # TODO:Check if the date is actually numbers not just "DD/MM/YYYY"

    # Resets the error Label if function gets this far
    errors.set("")

    # Checks if the customer_name_var is an existing customer or not (validation)
    if customer_name_var.get() not in customer_dict:

        # Creates another TopLevel window just to confirm that the user wants to make a new user 'account'
        verify = messagebox.askyesno(title="New Customer Confirmation", message="{} is not an existing customer.\nDo you want to create a new customer?".format(customer_name_var.get()))  # This returns True or False depending on user response

        if verify:
            customer_dict[customer_name_var.get()] = Customer(customer_name_var.get())
            current_customer = customer_dict[customer_name_var.get()]

        else:
            errors.set("No new customer created")
            return
    else:
        current_customer = customer_dict[customer_name_var.get()]

        if current_customer.booking_count == 3:
            discount_type = 1
            reverse_group_history = []

            for group_size in current_customer.bookings.values():
                reverse_group_history.insert(0, group_size)

            if reverse_group_history[0] == 6 and reverse_group_history[1] == 6 and reverse_group_history[2] == 6:
                discount_type = 2

            current_customer.booking_count = -1

    current_customer.booking_count += 1
    booking_window()


# This is the final main window where the prices, etc. are displayed
def booking_window():
    current_customer = customer_dict[customer_name_var.get()]
    current_customer.booking(date_var.get(), people_var.get())

    type_number = type_select_var.get()[0]
    type_cost = 0

    if type_number == "1":
        type_cost = 40
    elif type_number == "2":
        type_cost = 25

    total_cost = type_cost * int(people_var.get())

    if discount_type == 1:
        total_cost /= 2
    elif discount_type == 2:
        total_cost = 0

    current_booking = Tk()
    current_booking.title("{} - {} Booking".format(customer_name_var.get(), date_var.get()))

    booking_window_title = ttk.Label(current_booking, text="Rafting Cymru", justify="center")
    booking_window_title.grid(row=0, column=0, padx=10, pady=5)

    booking_title = ttk.Label(current_booking, text="{} - {}".format(customer_name_var.get(), date_var.get()), justify="center")
    booking_title.grid(row=1, column=0, padx=10, pady=5)

    full_details_frame = ttk.LabelFrame(current_booking, text="Full Booking Details")
    full_details_frame.grid(row=2, column=0, padx=10, pady=5)

    final_date_label = ttk.Label(full_details_frame, text="Date: ")
    final_date_label.grid(row=0, column=0, pady=5, sticky="E")

    final_date = ttk.Label(full_details_frame, text="{}".format(date_var.get()))
    final_date.grid(row=0, column=1, pady=5, sticky="W")

    final_people_label = ttk.Label(full_details_frame, text="Group Size: ")
    final_people_label.grid(row=1, column=0, pady=5, sticky="E")

    final_people = ttk.Label(full_details_frame, text="{}".format(people_var.get()))
    final_people.grid(row=1, column=1, pady=5, sticky="W")

    final_type_label = ttk.Label(full_details_frame, text="Type: ")
    final_type_label.grid(row=2, column=0, pady=5, sticky="E")

    final_type = ttk.Label(full_details_frame, text="{}".format(type_select_var.get()[2:]))
    final_type.grid(row=2, column=1, pady=5, sticky="W")

    final_time_label = ttk.Label(full_details_frame, text="Time: ")
    final_time_label.grid(row=3, column=0, pady=5, sticky="E")

    final_time = ttk.Label(full_details_frame, text="{}".format(time_select_var.get()[2:]))
    final_time.grid(row=3, column=1, pady=5, sticky="W")

    price_label = ttk.Label(full_details_frame, text="Final Price:\n£{:.2f}".format(total_cost), justify="center")
    price_label.grid(row=1, column=2, rowspan=2, padx=10, pady=5)

    # TODO: Create a window to view a customer's past bookings


# Creates the main window
root = Tk()

# Gives the window a title
root.title("Rafting Cymru Booking Platform")

# Creates the main label/heading for the window
main_title = ttk.Label(root, text="Rafting Cymru", justify="center")  # Optional font size increase, font=("Segoe UI", 20))
main_title.grid(row=0, column=0, padx=10, pady=5)

# Creates the LabelFrame to house the customer details input section
customer_details = ttk.LabelFrame(root, text="Customer Details")
customer_details.grid(row=1, column=0, padx=10, pady=5)

# Label for the customer_name Entry Field
customer_name_label = ttk.Label(customer_details, text="Name:")
customer_name_label.grid(row=0, column=0, pady=5, sticky="E")

# Creates a tkinter string variable for the customer_name Entry Field
customer_name_var = StringVar()
customer_name_var.set("")
# Creates the entry field for the customer's name
customer_name_entry = ttk.Entry(customer_details, textvariable=customer_name_var, width="45")
customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

# Creates the booking_details LabelFrame
booking_details = ttk.LabelFrame(root, text="Booking Details")
booking_details.grid(row=2, column=0, padx=10, pady=5)

# A Label for the date_entry Entry box
date_label = ttk.Label(booking_details, text="Date:")
date_label.grid(row=0, column=0, pady=5, sticky="E")

# Creates a tkinter String Variable for the date
date_var = StringVar()
# Sets the date_var to the current date using the date object created earlier
date_var.set("DD/MM/YYYY")
# Entry field for booking date
date_entry = ttk.Entry(booking_details, textvariable=date_var, width="45")
date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="W")

# A Label for the people_entry Entry box
people_label = ttk.Label(booking_details, text="People:")
people_label.grid(row=1, column=0, pady=5, sticky="E")

# Creates a tkinter String Variable for the amount of people which will be converted to an integer later
people_var = StringVar()
people_var.set("")
# Entry field for amount of people
people_entry = ttk.Entry(booking_details, textvariable=people_var, width="45")
people_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

type_label = ttk.Label(booking_details, text="Type:")
type_label.grid(row=2, column=0, pady=5, sticky="E")

type_select_var = StringVar()
type_options = ["1-White Water Rafting - £40pp (12+yrs)", "2-Family White Water Rafting - £25pp (6+yrs)"]
type_select = ttk.OptionMenu(booking_details, type_select_var, type_options[0], *type_options)
type_select.grid(row=2, column=1, padx=5, pady=5, sticky="W")

time_label = ttk.Label(booking_details, text="Time:")
time_label.grid(row=3, column=0, pady=5, sticky="E")

time_select_var = StringVar()
time_options = ["1-Wednesday Evening", "2-Sunday Morning"]
time_select = ttk.OptionMenu(booking_details, time_select_var, time_options[0], *time_options)
time_select.grid(row=3, column=1, padx=5, pady=5, sticky="W")

# Creates 'Book' Button for actual program
book_button = ttk.Button(root, text="Book", command=checks)
book_button.grid(row=3, column=0, padx=10, pady=5)

# Creates a, to begin with, blank error display text area
errors = StringVar()
errors.set("")
error_display = ttk.Label(root, textvariable=errors)
error_display.grid(row=4, column=0)

# Runs the main window loop
root.mainloop()
