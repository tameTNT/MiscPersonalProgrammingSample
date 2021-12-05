import random
from tkinter import *

# The dictionary used by the program to convert numerals into words
english_numbers = {"1": "one",
                   "2": "two",
                   "3": "three",
                   "4": "four",
                   "5": "five",
                   "6": "six",
                   "7": "seven",
                   "8": "eight",
                   "9": "nine",
                   "10": "ten",
                   "11": "eleven",
                   "12": "twelve",
                   "13": "thirteen",
                   "14": "fourteen",
                   "15": "fifteen",
                   "16": "sixteen",
                   "17": "seventeen",
                   "18": "eighteen",
                   "19": "nineteen",
                   "20": "twenty",
                   "30": "thirty",
                   "40": "forty",
                   "50": "fifty",
                   "60": "sixty",
                   "70": "seventy",
                   "80": "eighty",
                   "90": "ninety"}

correctly_answered = []
incorrectly_answered = []
pupils = []
not_ask = []
to_ask = []
results = []
current_question = 0


# -------------MAIN NAME FOR NUMBER CODE-------------
# The main function for converting a number to a name. utilises dictionary created earlier
def name_for_number(integer):
    english = ""
    str_number = str(integer)
    length = len(str_number)

    # TODO: compact this code somehow
    if integer <= 20:  # numbers less than 20 are simply taken from the dictionary
        english = english_numbers[str_number]

    elif length == 2:  # 2 digit numbers consist of the first digit (the ten) which is looked up in the dictionary followed by the units (if it isn't 0)
        english = "{}".format(english_numbers[str_number[0] + "0"])
        if str_number[1] != "0":
            english += " {}".format(english_numbers[str_number[1]])

    # 3 and 4 digit numbers are slightly more awkward and each digit has to be checked after the first to see if it's 0
    elif length == 3:
        english = "{} hundred".format(english_numbers[str_number[0]])

        last_two_digits = int(str_number[1:])
        if 1 <= last_two_digits <= 20:
            english += " and {}".format(english_numbers[str(last_two_digits)])

        else:
            if str_number[1] != "0":
                english += " and {}".format(english_numbers[str_number[1] + "0"])
            if str_number[2] != "0":
                english += " {}".format(english_numbers[str_number[2]])

    elif length == 4:
        english = "{} thousand".format(english_numbers[str_number[0]])
        if str_number[1] != "0":
            english += ", {} hundred".format(english_numbers[str_number[1]])

        last_two_digits = int(str_number[2:])
        if 1 <= last_two_digits <= 20:
            english += " and {}".format(english_numbers[str(last_two_digits)])

        else:
            if str_number[2] != "0":
                english += " and {}".format(english_numbers[str_number[2] + "0"])
            if str_number[3] != "0":
                english += " {}".format(english_numbers[str_number[3]])

    return english.title()  # Just makes the question look nicer with an all capitalised number


# TODO: GUI class
# TODO: move main code below to GUI or separate function each
# -------------LOGGING IN A PUPIL CODE------------- opening storage, checking past results, etc.
with open("pupils.txt", "r") as pupil_names:  # NB: Change this directory address based on usage
        for line in pupil_names:  # Adds each pupil name in the file to a list
            pupils.append(line.strip())  # .strip() gets rid of newline character

current_pupil = input("What's your name?").lower().strip()
storage_file_name = "storage-{}.txt".format(current_pupil)  # NB: Change this directory address based on usage

if current_pupil not in pupils:  # Checks if the student is new, if they are then they're added to the pupil names file for storage
    with open("pupils.txt", "a") as pupil_names:
        pupil_names.write("{}\n".format(current_pupil))

else:
    with open(storage_file_name, "r") as storage:  # Opens the storage file to check questions to ask, not to ask, etc.
        stored_values = []
        for line in storage:
            if line == "-incorrect-\n" or line == "-results-\n":  # -incorrect- and -results- are the dividers used by the program to separate the three lists
                stored_values.append(line.strip())
            else:
                stored_values.append(int(line.strip()))

        split_point = stored_values.index("-incorrect-")
        results_point = stored_values.index("-results-")
        # Creates the three different lists for the program to use by splitting the big stored_values list by the 'split points' of -incorrect' and 'results'
        not_ask = stored_values[:split_point]
        to_ask = stored_values[split_point+1:results_point]
        results = stored_values[results_point+1:]

# -------------ACTUAL QUESTIONS CODE-------------
for question in range(10):  # Generates 10 questions
    current_question = random.randrange(1, 10000)  # Generates a random number
    if question < len(to_ask):
        current_question = to_ask[question]  # If there are certain questions remaining that were answered incorrectly last time, these are asked instead
    else:
        while current_question in not_ask:  # Prevents questions from being repeated by regenerating a random number
            current_question = random.randrange(1, 10000)

    print(name_for_number(current_question))  # Prints the name for the current number
    not_ask.append(current_question)  # Adds question to not_ask list so that it is not repeated

    while True:  # This makes sure the pupil has entered a number
        try:
            response = int(input("What is that number in numerals? "))  # Asks the actual question
            break
        except ValueError:  # i.e. if the entered value is an integer
            print("That is not a number. Please input an integer.")

    if response == current_question:  # Checks if the question was answered correctly and adds it to the corresponding list
        correctly_answered.append(current_question)
    else:
        incorrectly_answered.append(current_question)

score = len(correctly_answered)  # A pupil's score will simply be how many they answered correctly
print("Thank you, {}. You scored {}/10".format(current_pupil.title(), score))  # Prints the pupil's name and their score
results.append(score)

if len(results) % 3 == 0:  # Every three tests the program will output a mean
    mean = (results[-3] + results[-2] + results[-1]) / 3  # Calculates the mean
    print("You mean score over the last three tests is {}".format(round(mean)))  # Rounds the mean to the nearest integer and prints it

with open(storage_file_name, "w+") as storage:  # Stores final results and correctly and incorrectly answered questions
    for number in correctly_answered:
        storage.write(str(number) + "\n")

    storage.write("-incorrect-\n")  # This splits the storage file so the program can later use it to generate the two lists
    for number in incorrectly_answered:
        storage.write(str(number) + "\n")

    storage.write("-results-\n")  # This splits the storage file again so the program can later use it to generate a results list
    for result in results:
        storage.write(str(result) + "\n")
