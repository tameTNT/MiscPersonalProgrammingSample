import math, json  # math imported for ceil function and json for data storage capability
import tkinter as tk  # tkinter imported as tk to reduce length of function statements
from tkinter import ttk, messagebox  # ttk library used to make GUI fit with OS and messagebox library is used for error messages during validation


class Text:  # The main Text class used to store the details of each text
    def __init__(self, title, intended_reading_age, keywords, content):  # When a text class is created, this data is entered by the user and fed into the initiation statement in the program
        self.title = title.capitalize()
        self.intended_reading_age = int(intended_reading_age)
        self.unformatted_keywords = keywords  # These 'unformatted keywords' are needed for json file storage purposes later on (as each text is re-declared when data files are loaded so this stores the original 'raw' input from the user)

        self.keywords = [keyword.strip().capitalize() for keyword in self.unformatted_keywords.split(",")]
        self.keywords = ", ".join(self.keywords)  # This list comprehension and join method turn the user's string input into a nicely formatted list which can be printed and used within the program

        self.content = content.strip()  # Removes whitespace from text content

        self.character_count = len(self.content)  # Counts the number of characters in the text content

        # This section allows the program to count the number of words in the text content - even if there *aren't* spaces after full stops or commas
        self.raw_split_words = self.content.split(" ")
        for i in range(len(self.raw_split_words)):
            for to_check in [",", "."]:
                if to_check in self.raw_split_words[i] and self.raw_split_words[i][-1] != to_check:
                    self.split_word = self.raw_split_words.pop(i).split(to_check)
                    self.raw_split_words.insert(i, self.split_word[0] + to_check)
                    self.raw_split_words.insert(i + 1, self.split_word[1])

        self.word_count = len(self.raw_split_words)  # Counts the number of words in the text content

        self.sentence_count = 0
        for character_number in range(len(self.content)):
            sentence_enders = ".!?"
            if self.content[character_number] in sentence_enders and self.content[character_number-1] not in sentence_enders:  # If the previous character was also a 'sentence ender' it does not count as a new sentence (e.g. when using an elipsis '...')
                self.sentence_count += 1  # Counts the number of sentences in the text content by counting the number of sentence ending punctuation marks (i.e. '.', '!' or '?')

        if self.sentence_count == 0:  # To prevent division by zero errors in the following stage of the program, the code first checks that there is at least one sentence in the text content. If there isn't the user is presented with an error dialogue
            messagebox.showerror("No Full Sentences Detected", "Please ensure that you have used at least one full stop ('.'), question mark ('?') or exclamation mark ('!') in the Text Content entry field.")
            self.success_state = "Failed input"
        else:
            ari = math.ceil(4.71 * (self.character_count / self.word_count) + 0.5 * (self.word_count / self.sentence_count) - 21.43)  # The actual implementation ARI formula
            self.calculated_reading_age = ari
            self.success_state = "Complete"

    def return_details(self, *args):  # This method allows the program to request as many attributes as it needs from each text class using *args
        if self.success_state == "Failed input":  # These 'success states' tell the program whether all the data was entered correctly (i.e. no division by zero errors, etc.)
            return "Failed input"
        if self.success_state == "Complete":
            detail_dictionary = {"title":self.title, "printable_keywords":self.keywords, "intended_reading_age":self.intended_reading_age, "calculated_reading_age":self.calculated_reading_age, "content":self.content}  # This dictionary associates each class attribute with a more readable string name
            return_list = []
            for key in args:
                return_list.append(detail_dictionary[key])  # Each attribute the user requested is added to the return list
            return return_list

    def return_data_to_be_saved(self):  # This method is needed for data storage capability and returns just what the user originally entered into the program
        return self.title, self.intended_reading_age, self.unformatted_keywords, self.content


class MainWindow:  # This is the main window of the GUI from which all other menus and windows branch off
    def __init__(self, master):
        self.master = master
        self.master.title("ARI")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.instructions = ttk.Label(self.frame, text="Welcome to the ARI!\nPlease choose whether to enter a new text, search currently stored texts or load/save texts.", justify="center")
        self.instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=0)

        self.enter_button = ttk.Button(self.frame, text="Enter a new text", command=self.enter_new)
        self.enter_button.grid(row=1, column=0, padx=5, pady=10)

        self.enter_button = ttk.Button(self.frame, text="Search stored texts", command=self.search_existing)
        self.enter_button.grid(row=1, column=1, padx=5, pady=10)

        self.load_data_button = ttk.Button(self.frame, text="Load saved texts", command=lambda: self.load_data("stored_data.json"))
        self.load_data_button.grid(row=2, column=0, padx=5, pady=10)

        self.save_data_button = ttk.Button(self.frame, text="Save stored texts", command=lambda: self.save_data(text_objs))
        self.save_data_button.grid(row=2, column=1, padx=5, pady=10)

        self.success_text_variable = tk.StringVar()
        self.success_text = ttk.Label(self.frame, textvariable=self.success_text_variable, justify="center")  # This label is used to display the outcome of methods such as loading and saving data
        self.success_text.grid(row=3, column=0, columnspan=2, padx=5, pady=0)

        self.input_window_root = None  # These attributes are declared here to be given a value further on in the class; they are the variables for GUI windows that branch off this one
        self.input_window = None
        self.search_window_root = None
        self.search_window = None

    def enter_new(self):  # Creates a new text entry window
        self.input_window_root = tk.Toplevel(self.master)
        self.input_window = InputWindow(self.input_window_root)

    def search_existing(self):  # Creates a new search window
        self.search_window_root = tk.Toplevel(self.master)
        self.search_window = SearchWindow(self.search_window_root)

    def load_data(self, file_name):  # Loads the file with the name 'file_name' - file name parameter not necessarily needed but included for future adaptability
        try:
            with open(file_name, mode="r") as file:
                saved_data = json.load(file)
                for obj_details in saved_data:
                    text_objs.append(Text(*obj_details))  # Creates a new text object with the details loaded from the file and adds it immediately to the text_objs list for retrieval by the program

            self.success_text_variable.set("Text data in 'stored_data.json' file successfully loaded")  # The user is shown in the GUI when data has been successfully loaded

        except FileNotFoundError:  # If 'file_name' is not found in the same directory as the program an error dialogue is produced
            messagebox.showerror("Save file not found", "A file with save data was not found.\nPlease make sure a 'stored_data.json' file actually exists and is in the same directory as this program.")

    def save_data(self, data):
        to_be_saved = []
        for obj in data:
            to_be_saved.append(obj.return_data_to_be_saved())  # Adds the data returned by the 'return_data_to_be_saved' method of each text object to a list which is then ultimately saved as a .json file

        with open("stored_data.json", mode="w+") as file:
            json.dump(to_be_saved, file)

        self.success_text_variable.set("'stored_data.json' save file successfully created")  # The user is shown in the GUI when data has been successfully saved


class InputWindow:  # This GUI window is used by the user to enter the details of a new text
    def __init__(self, master):
        self.master = master
        self.master.title("Enter a new text")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.instructions = ttk.Label(self.frame, text="Please enter the details of the new text below.", justify="center")
        self.instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=0)

        self.title_label = ttk.Label(self.frame, text="Title:")
        self.title_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
        self.title_variable = tk.StringVar()
        self.title_entry = ttk.Entry(self.frame, textvariable=self.title_variable, justify="left", width="26")
        self.title_entry.grid(row=1, column=1, padx=5, pady=5, sticky="W")

        self.intended_age_label = ttk.Label(self.frame, text="Intended reading age:")
        self.intended_age_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
        self.intended_age_variable = tk.StringVar()
        self.intended_age_entry = ttk.Entry(self.frame, textvariable=self.intended_age_variable, justify="left", width="26")
        self.intended_age_entry.grid(row=2, column=1, padx=5, pady=5, sticky="W")

        self.keyword_label = ttk.Label(self.frame, text="Keywords (separated by ','):")
        self.keyword_label.grid(row=3, column=0, padx=5, pady=5, sticky="E")
        self.keyword_variable = tk.StringVar()
        self.keyword_entry = ttk.Entry(self.frame, textvariable=self.keyword_variable, justify="left", width="26")
        self.keyword_entry.grid(row=3, column=1, padx=5, pady=5, sticky="W")

        self.content_label = ttk.Label(self.frame, text="Text Content:")
        self.content_label.grid(row=4, column=0, padx=5, pady=5, sticky="E")
        self.content_entry = tk.Text(self.frame, height="4", width="23", font=["Segoeuil", 9], wrap="word")  # There is no ttk version of the Text UI element (needed as a multiline entry field). 'Segoeui' is the default font used by Windows 10. The final 'l' character simply indicates that the light variation of the font should be used
        self.content_entry.grid(row=4, column=1, padx=5, pady=5, sticky="W")

        self.enter_button = ttk.Button(self.frame, text="Enter!", command=self.enter_text)
        self.enter_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.success_text_variable = tk.StringVar()
        self.success_text = ttk.Label(self.frame, textvariable=self.success_text_variable, justify="center")  # This label is used to display the outcome of data entry (i.e. un/successful text object creation)
        self.success_text.grid(row=6, column=0, columnspan=2, padx=10, pady=0)

    def enter_text(self):
        if vcmd("presence", self.title_variable.get()) and vcmd("type", self.intended_age_variable.get()) and vcmd("presence", self.keyword_variable.get()) and vcmd("presence", self.content_entry.get("1.0", "end-1c")):  # This validates each individual piece of data entered using the validate command (vcmd) function declared later on. It returns True if the check is passed so all need to pass for the program to continue otherwise an error dialogue is displayed
            if vcmd("format", self.keyword_variable.get()):  # The format check isn't a 'right/wrong' answer response (i.e. the user may actually want to go forward with a singular long keyword string) so it has its own separate if branch
                text_objs.append(Text(self.title_variable.get(), self.intended_age_variable.get(), self.keyword_variable.get(), self.content_entry.get("1.0", "end-1c")))  # Here, the actual text object is created using the user's inputted data and immediately added to the 'text_objs' list. 'content_entry's get statement is different as it is ek.Text() field rather than an tk.Entry() field

                if text_objs[-1].return_details() != "Failed input":  # If text object creation doesn't fail (i.e. no division by zero, etc.) the program tells the user that creation was a success!
                    messagebox.showinfo("New text created successfully!", "Intended Reading Age: {}\nCalculated Reading Age: {}".format(*text_objs[-1].return_details("intended_reading_age", "calculated_reading_age")))
                    self.success_text_variable.set("New text created successfully!")
                else:
                    text_objs.pop(-1)  # If text object creation failed in some way (causing the initiation method to return 'Failed input') then the object is removed from the 'text_objs' list and the user notified that no new text was created (they will have already seen the relevant error dialogue
                    self.success_text_variable.set("No new text created.")

            else:
                self.success_text_variable.set("No new text created.")


class SearchWindow:  # This GUI window is used by the user to search texts that have already been entered and created
    def __init__(self, master):
        self.master = master
        self.master.title("Search stored texts")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.instructions = ttk.Label(self.frame, text="Select a method by which to search below.", justify="center")
        self.instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=0)

        self.search_type = tk.IntVar()
        self.search_type.set(0)
        self.radio_button1 = ttk.Radiobutton(self.frame, text="Calculated Reading Age", variable=self.search_type, value=0, command=lambda: self.search_type_selection(0))
        self.radio_button1.grid(row=2, column=0, padx=5, pady=5)
        self.radio_button2 = ttk.Radiobutton(self.frame, text="Keywords", variable=self.search_type, value=1, command=lambda: self.search_type_selection(1))  # These two search_type_selection commands enable/disable the corresponding entry boxes below the radio buttons using this class' search_type_selection method
        self.radio_button2.grid(row=2, column=1, padx=5, pady=5)

        self.age_search = tk.StringVar()
        self.age_search.set("e.g. 5")
        self.age_search_entry = ttk.Entry(self.frame, textvariable=self.age_search, width=40, justify="center", state="enabled")
        self.age_search_entry.grid(row=3, column=0, padx=5, pady=5)

        self.keyword_search = tk.StringVar()
        self.keyword_search.set("e.g. some, keywords (leave blank to show all)")
        self.keyword_search_entry = ttk.Entry(self.frame, textvariable=self.keyword_search, width=40, justify="center", state="disabled")
        self.keyword_search_entry.grid(row=3, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.frame, text="Search!", command=lambda: self.search(self.search_type.get(), self.return_search_query(), text_objs))  # For explanations of each argument see the search method below
        self.search_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.search_results_window_root = None
        self.search_results_window = None

    def search_type_selection(self, method):
        if method == 0:
            self.age_search_entry.config(state="enabled")
            self.keyword_search_entry.config(state="disabled")
        elif method == 1:
            self.age_search_entry.config(state="disabled")
            self.keyword_search_entry.config(state="enabled")

    def return_search_query(self):  # This method just returns the data from the correct entry field depending on which radio button is selected
        if self.search_type.get() == 0:
            return self.age_search.get()
        elif self.search_type.get() == 1:
            return self.keyword_search.get()

    def search(self, query_type, query, content):  # The actual search method which trawls through the stored texts (in the text_objs list) and returns them as required. The 'content' parameter is not necessarily needed but permits greater future adaptability
        return_template = "\nResult number {}|Text title: {}|Keywords: {}|Intended Reading Age: {}        Calculated Reading Age: {}|Text Content:\n{}\n"
        results = []

        if query_type == 0:  # Used if the user is searching by calculated reading age
            if not vcmd("type", query):  # Validates the user's input to check it's an integer
                return

            query = int(query)

            for obj in content:
                if query == obj.calculated_reading_age:
                    results.append(obj)

            query_type = "calculated reading age"
            query = ["{}".format(query)]  # Needs to be in list format to match with input of a keyword search

        elif query_type == 1:  # Used if the user is searching by keywords
            if not vcmd("format", query):  # Validates the user's input to check it's correctly formatted as a keyword list
                return

            query = [keyword.strip().capitalize() for keyword in query.split(",")]  # Formats the search query as the program requires

            for obj in content:
                found_result = False
                for keyword in query:
                    if keyword in obj.keywords:
                        found_result = True
                if found_result:
                    results.append(obj)

            query_type = "keyword(s)"

        final_return = ""
        for result_number in range(len(results)):
            final_return += return_template.format(result_number + 1, *results[result_number].return_details("title", "printable_keywords", "intended_reading_age", "calculated_reading_age", "content"))  # Fills in the template with the details of the text objects that meet the search criteria

        if len(results) == 0:
            final_return = "No results found"

        self.search_results_window_root = tk.Toplevel(self.master)
        self.search_results_window = ResultsWindow(self.search_results_window_root, final_return.split("|"), query_type, "{}".format(", ".join(query)))  # The results window initiation method takes numerous parameters that format the window text as required


class ResultsWindow:  # This GUI window displays the results of a text search to the user, presenting them with each text's relevant details and content
    def __init__(self, master, final_search_results, search_method, search_query):  # The initialisation method requires these arguments to display the actual results of the search and to fill in the body/explanatory text at the top of the window
        self.master = master
        self.master.title("Search Results")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.instructions = ttk.Label(self.frame, text="Results for search {}:'{}' are shown below:".format(search_method, search_query), justify="center")
        self.instructions.grid(row=0, column=0, padx=5, pady=0)

        self.search_results = ""
        for result_section in final_search_results:  # This for loop compiles all the results in the 'final_search_results' list, returned by the search function of the 'SearchWindow', into a correctly formatted string which can then be displayed in the window's main Label
            self.search_results += "{}\n".format(result_section)

        self.results_display = ttk.Label(self.frame, text="{}".format(self.search_results), justify="center", wraplength=500)
        self.results_display.grid(row=1, column=0, padx=5, pady=5)


def vcmd(method, user_input):  # This function is used throughout the program to validate the user's input. Each different if branch refers to a different validation routine.
    # If the 'user_input' is incorrect in any way (not an integer/not in the correct format/not given), the user is presented with an error dialogue and the function returns False so that the current operation within the program can be halted until the correct input is given
    if method == "type":
        try:
            int(user_input)
            return True
        except ValueError:
            messagebox.showerror("Non-integer entered", "Please enter an integer value for age.")
            return False

    elif method == "format":
        keyword_list = user_input.split(",")
        if len(keyword_list) == 1 and len(keyword_list[0]) > 8:  # If the keyword list consists of only one suspiciously long element, it's possible that the user may have incorrectly separated their keywords (i.e. not used commas) and the program cannot detect each individual keyword.
            response = messagebox.askyesno("Possibly Incorrectly Separated List", "Please note that your list may not be correctly separated using commas: ','.\nYour keyword list should look like this: 'these, are, some, keywords'\nWould you like to continue with the keyword list {}?".format(str(keyword_list).strip("[]")))
            return response  # The messagebox above will return True or False depending on whether or not the user wants to go ahead with the keyword list they entered. Their response is stored in the 'response' variable and then returned by this function
        else:
            return True

    elif method == "presence":
        if user_input == "":  # This routine simply checks whether the user has provided an input for all required entry fields (a presence check)
            messagebox.showerror("Missing Data", "Please enter data for all entry fields.")
            return False
        else:
            return True


# Storage list for all text objects. New texts are added to this list automatically
text_objs = list()

# Main tkinter GUI loop
root = tk.Tk()
app = MainWindow(root)
root.mainloop()
