from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import requests
import random
import webbrowser
import time


def generate():
    # Makes variables from tkinter window and ther functions accesible
    global path_list_text
    global origin
    global target
    global copy_1
    global copy_2

    # This list will store the path the program takes
    path = []

    # Sets the original random page or custom start page depending on the users choice in the GUI
    if origin_page_var.get() == 1:
        divert = "/wiki/Special:Random"
    elif origin_page_var.get() == 2:
        divert = custom_divert_var.get()

    # Specifies length of click path
    try:
        if path_length_choice.get() == 1:  # These if/elif branches check which radiobutton the user has selcted in the GUI
            length = int(path_length_var.get())
        elif path_length_choice.get() == 2:
            length = random.randrange(2,
                                      11)  # Paths longer than 10 take quite some time to generate and are very difficult
    except ValueError:
        error_window("number")
        return  # Placing return here stops the funciton from continuing

    # Function used to check the valitidy of links
    def link_check():
        global target
        # This massive if branch checks if the link is a valid link for the game to use
        if "/wiki/" in divert:  # This makes sure the game stays on the wikipedia domain
            if "Category:" not in divert:  # Category, File, etc. are all wikipedia admin pages so are useless
                if "File:" not in divert:
                    if "Wikipedia:" not in divert:
                        if "Template:" not in divert:
                            if "Special:" not in divert:
                                if "Help:" not in divert:
                                    if "#" not in divert:  # '#'s are just links to within the page so these are useless anyway
                                        if "ISBN" not in links[
                                            choice].get_text():  # There are often many ISBN links in a well written Wiki page so this stops the program jumping to the ISBN page all the time
                                            if not i == length - 1:  # This is the branch that normally happens
                                                # This makes sure that the link ISN'T in a navbox at the bottom or in the references
                                                if str(links[choice]) in str(
                                                        links[choice].find_parents(class_="navbox")) or str(
                                                        links[choice]) in str(
                                                        links[choice].find_parents(class_="references")):
                                                    return False
                                                else:
                                                    # If the link passes the tests it is added to the path list and the program continues
                                                    path.append("{} - {}".format(links[choice].get_text(), divert))
                                                    return True
                                            # On the last link the program simply ends
                                            else:
                                                target = page.url  # This else branch is onlky carried out in the last round and simply stores the current page as the target and then ends
                                                return True

        # If a link is invalid it is removed from the list
        links.pop(choice)
        return False

    # MAIN PROGRAM LOOP
    for i in range(length):
        try:
            if i == 0:  # If this is the origin page (the first iteration of the loop) this branch is executed
                done = False
                # This loop checks if the starting page is valid and keeps going to a random page until it is
                while not done:
                    # Gets page data from a random wiki page using the, helpfully supplied by Wikipedia themselves, 'Special:Random' link
                    page = requests.get("https://en.wikipedia.org{}".format(divert))
                    if "/wiki/" in page.url:
                        if "Category:" not in page.url:
                            if "File:" not in page.url:
                                if "Template" not in page.url:
                                    if "Wikipedia:" not in page.url:
                                        origin = page.url
                                        done = True
            else:  # This just happens normally using the divert chosen on the previous page
                page = requests.get("https://en.wikipedia.org{}".format(divert))

        except:
            error_window("divertl")

        # Creates the navigatable HTML version of the current page
        content = BeautifulSoup(page.content, "html.parser")
        # breakpoint()  TODO: broken!!!
        # This creates a variable with the contents of the wiki page (including all the hyperlinks)
        # content = list(soup)[2].find(id="content")

        # This narrows it down just to the links
        links = list(content.find_all("a"))

        # This loop choses a random link on the wiki page and continues doing so until it finds a valid one
        done = False
        while not done:
            # This choses a random link on the page
            choice = random.randrange(1, len(links))
            # Try and except is here as the program sometimes runs into an error here. This stops the program outright crashing. Cause of error unknown
            try:
                divert = links[choice]["href"]
            except KeyError:
                error_window("key")
            done = link_check()  # As the link_check() function return either True or False, this can be used to break from this while loop

    # These two statements set the chosen start and end urls as text in the tkinter window
    o_text.set("Begin at {}".format(origin))
    t_text.set("And get to {}".format(target))

    # If the use has opted for the windows to be automatically opened, the program checks and does that here
    if win_create_var.get() == 1:
        webbrowser.open_new_tab(origin)
        time.sleep(2)  # This time is to prevent windows opening in the wrong order
        webbrowser.open_new_tab(target)

    # Sets path list in tkinter window
    path_list_text.set("Possible Click Path:\n(On page text - Wikipedia link)\n{}".format("\n".join(path)))

    # Makes 'Copy to Clipboard' buttons usable
    copy_1.config(state="normal")
    copy_2.config(state="normal")


# Opens a new window displaying the computer's 'click path'
def show_path():
    global path_list_text
    path_view = Toplevel(base)
    path_text = ttk.Label(path_view, textvariable=path_list_text, justify="center")
    path_text.grid(row=0, column=0, padx=5, pady=5)


# These two functions copy their respective urls to the clipboard
def clipboard_1():
    base.clipboard_clear()
    base.clipboard_append(origin)
    base.update()


def clipboard_2():
    base.clipboard_clear()
    base.clipboard_append(target)
    base.update()


# Changes the entry field to enabled or disabled depending on which radio button is currently selected
def radio_change_1():
    if origin_page_var.get() == 1:
        custom_divert_entry.config(state="disabled")
    elif origin_page_var.get() == 2:
        custom_divert_entry.config(state="normal")


def radio_change_2():
    if path_length_choice.get() == 1:
        path_length_entry.config(state="normal")
    elif path_length_choice.get() == 2:
        path_length_entry.config(state="disabled")


# This validate function makes sure that you can only enter integers into the Entry field by just setting the contents to 4 if you try entering anything else
def vcmd():  # vcmd stands for validate command
    try:
        if path_length_var.get() == "":
            return True
        else:
            int(path_length_var.get())
            return True
    except ValueError:
        path_length_var.set("")
        return False


# Used throughout the program in the case of an error to display and error window
def error_window(type_):
    error = Toplevel(base)
    # There is different text displayed depending on the location of the error
    if type_ == "divertl":
        error_message_text = StringVar()
        error_message_text.set(
            "There was a problem with the Wiki URL you entered.\nPlease try another one or fix any mis-types, etc. with the current one.")
    elif type_ == "key":
        error_message_text = StringVar()
        error_message_text.set(
            "The program ran into an error processing a Wiki page.\nPlease restart it and try again.")
    elif type_ == "number":
        error_message_text = StringVar()
        error_message_text.set("You've entered an invalid number\n for the click path length.")
    error_message = ttk.Label(error, textvariable=error_message_text, justify="center")
    error_message.grid(row=0, column=0, padx=5, pady=5)
    error_message.mainloop()


# Creates the main window
base = Tk()
base.title("The Python Wiki-Game")

# This variable is needed across commands/functions so is put out here for convenience
path_list_text = StringVar()
path_list_text.set("Possible Click Path:\n\nYou haven't pressed the Generate button yet!\n\n")

# Main game explanation section
text_frame = ttk.LabelFrame(base, text="The Wiki-Game (in Python 3.6 using BS)")
text_frame.grid(row=0, column=0, padx=5, pady=5)
warning_label = ttk.Label(text_frame,
                          text="WARNING:\nThis version of the wikigame is much harder than normal as the program will use almost every possible link on a page to progress.\nLuckily, this does NOT include collapsed 'drawers' and footnote/reference links.\nThe program is restricted to staying on the English Wikipedia domain so at least there's some hope!\nIt is also prevented from going on stupid Wikipedia admin and moderating pages such as 'Help' and 'Template'",
                          justify="center")
warning_label.grid(row=0, column=0, padx=5, pady=5)
explanation_label = ttk.Label(text_frame,
                              text="HOW TO PLAY:\nMake your way from the first Wikipedia URL to the second one,\nusing only the hyperlinks on the pages to navigate the complex web that is Wikipedia.\nIt's that simple!",
                              justify="center")
explanation_label.grid(row=1, column=0, padx=5, pady=5)

# Creation of main game components
game_frame = ttk.LabelFrame(base, text="Game & Options")
game_frame.grid(row=1, column=0, padx=5, pady=5)
generate_button = ttk.Button(game_frame, text="Start a Game!", command=generate)
generate_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# Two text variables to display start and end urls
o_text = StringVar()
o_text.set("Origin/Start Page will display here")
path_details_1 = ttk.Label(game_frame, textvariable=o_text, justify="right")
path_details_1.grid(row=1, column=0, padx=5, pady=5, sticky="E")
t_text = StringVar()
t_text.set("Destination/End Page will display here")
path_details_2 = ttk.Label(game_frame, textvariable=t_text, justify="right")
path_details_2.grid(row=2, column=0, padx=5, pady=5, sticky="E")

# Copy to clipboard buttons
copy_1 = ttk.Button(game_frame, text="Copy to Clipboard", state="disabled", command=clipboard_1)
copy_1.grid(row=1, column=1, padx=5, pady=5, sticky="W")
copy_2 = ttk.Button(game_frame, text="Copy to Clipboard", state="disabled", command=clipboard_2)
copy_2.grid(row=2, column=1, padx=5, pady=5, sticky="W")

# Button to open new window with computer's 'click path'
show_path_button = ttk.Button(game_frame, text="Show Path (opens in new window)", command=show_path)
show_path_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Option to turn automatic window creation on and off
win_create_var = IntVar()
win_create_var.set(0)
win_create_option = ttk.Checkbutton(game_frame, text="Automatically open start and end pages in default browser?",
                                    variable=win_create_var)
win_create_option.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Option to start on another selected wiki page
origin_page_var = IntVar()
origin_page_var.set(1)
random_radio = ttk.Radiobutton(game_frame, text="Start on a Random Wikipedia page", variable=origin_page_var, value=1,
                               command=radio_change_1)
random_radio.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
select_radio = ttk.Radiobutton(game_frame, text="Enter a Custom Wikipedia start page:", variable=origin_page_var,
                               value=2, command=radio_change_1)
select_radio.grid(row=6, column=0, padx=5, pady=5, sticky="E")

# This entry field is disabled unless you select the custom radiobutton
custom_divert_var = StringVar()
custom_divert_var.set("Please enter a Custom Wikipedia Page in the format '/wiki/Spam'")
custom_divert_entry = ttk.Entry(game_frame, textvariable=custom_divert_var, width="60", justify="center",
                                state="disabled")
custom_divert_entry.grid(row=6, column=1, padx=5, pady=5)

path_length_choice = IntVar()
path_length_choice.set(1)
# This allows the user to speicfy the length of the 'click path' or random
path_length_label = ttk.Radiobutton(game_frame, text="Enter an integer for the length of the 'Click Path':",
                                    variable=path_length_choice, value=1, command=radio_change_2)
path_length_label.grid(row=7, column=0, padx=5, pady=5, sticky="E")
# The default length for the 'click path' is 6
path_length_var = StringVar()
path_length_var.set("6")
# This entry field is validated with an above funciton to make sure only numerical values can be entered
path_length_entry = ttk.Entry(game_frame, textvariable=path_length_var, width="20", validate="key",
                              validatecommand=vcmd)
path_length_entry.grid(row=7, column=1, padx=5, pady=5, sticky="WE")
path_length_label = ttk.Radiobutton(game_frame, text="Random 'Click Path' Length (max. 10)",
                                    variable=path_length_choice, value=2, command=radio_change_2)
path_length_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

base.mainloop()
