import os
import time
import random
import configparser
from colorUtil import Colors

# Multiplication Game
# A game where you quickly go through common multiplication problems with customization.
#   You can edit the timer, number of problems, highest and lowest numbers used in generation, and more.

bool_map = {"True": True, "False": False}  # Convert strings to bools.

configure_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configure.ini")
config = configparser.ConfigParser()
config.read(configure_file)


def convert_digits(list_check):
    """Convert Digits function: converts strings to ints if applicable. Only works with neutral or positive ints."""
    converted_list = []
    for index, item in enumerate(list_check):
        if item.isdigit():
            converted_list.append(int(item))
        else:
            converted_list.append(item)
    del list_check
    return converted_list


# The following adds config options into a list and converts them into integers if applicable.
options_list = []
for section in config.sections():
    for option, option_value in config.items(section):
        options_list.append(option_value)

options_list = convert_digits(options_list)
MIN, MAX, INTEGER_NUMS, PROBLEM_NUMS, TRACK_TIMER, PRINT_SETTINGS = options_list


def generate_random_ints():
    """Generate Random Integers function: generates a list of random integers and returns."""
    set_of_problems = []
    for _ in range(PROBLEM_NUMS):
        generated_ints = [random.randint(MIN, MAX) for _ in range(INTEGER_NUMS)]
        set_of_problems.append(generated_ints)
    return set_of_problems


def _print_problems_and_solve(set_of_problems):
    """Print Problems And Solve helper function: Serves to print the problems in an organized and flexible way."""
    print_spacing = 0
    num_correct = 0
    start_timer = time.time()

    for j in range(len(set_of_problems)):
        for index in range(len(set_of_problems[j])):
            if set_of_problems[j][index] < 10:  # Spacing for the prints
                print_spacing += 1

            if len(set_of_problems[j]) - 1 == index:  # Last problem
                print(f"×  {' ' * print_spacing}{set_of_problems[j][index]}")
            else:
                print(f"   {' ' * print_spacing}{set_of_problems[j][index]}")
            print_spacing = 0
        print("─────\n")

        answer = 1  # Product of all numbers in that entry.
        for index in range(len(set_of_problems[j])):
            answer *= set_of_problems[j][index]
        try:
            user_answer = input("> Answer?: ")
            if user_answer in ["quit", "exit", "q"]:  # Record num_correct and final_time up till this command input.
                print("> Force end, bringing back to menu...")
                end_timer = time.time()
                final_time = end_timer - start_timer
                return num_correct, final_time
            elif int(user_answer) == answer:
                print(f"✅ Correct | Answer: {answer}")
                num_correct += 1
                continue
            else:
                print(f"❌ Incorrect | Answer: {answer}\n")
        except ValueError:
            print(f"❌ Incorrect | Answer: {answer}\n")
    end_timer = time.time()
    final_time = end_timer - start_timer
    return num_correct, final_time


def _grade_rank(correctness_grade, correctness_amount):
    """Grade Rank helper function: Displays a different color code depending on grade number."""
    if correctness_grade >= 0.70:
        color_rank = Colors.GREEN
    elif correctness_grade >= 0.50:
        color_rank = Colors.YELLOW
    else:
        color_rank = Colors.RED

    print(f"{color_rank}{correctness_amount}/{PROBLEM_NUMS}{Colors.END} correct.\n")


def initial_file_check():
    """Initial File Check function: Checks if the file exists and if not, creates it. Also checks for stupid
       configs the user might have tried to do and corrects them. If you get an error from here then that means
       you're a stubborn bitch who tried changing the config data before startup..."""

    global MIN, MAX, INTEGER_NUMS, PROBLEM_NUMS, TRACK_TIMER, PRINT_SETTINGS

    try:
        PRINT_SETTINGS = config.getboolean('Settings', 'print_settings', fallback=False)
    except ValueError:
        print("FileError: Reverting print_settings to defaults due to invalid values.")
        config['Settings']['print_settings'] = 'False'
        PRINT_SETTINGS = False

    try:
        TRACK_TIMER = config.getboolean('Settings', 'track_timer', fallback=False)
    except ValueError:
        print("FileError: Reverting track_timer to defaults due to invalid values.")
        config['Settings']['track_timer'] = 'True'
        TRACK_TIMER = True

    if isinstance(MIN, str) or isinstance(MAX, str) or MIN > MAX:  # Error check so the program doesn't fucking kill
                                                                   # itself when generating numbers.
        print("FileError: Reverting minimum and maximum to defaults due to invalid value(s).")
        config['Settings']['min'] = '1'
        config['Settings']['max'] = '12'
        MIN = 1
        MAX = 12

    if isinstance(INTEGER_NUMS, str) or INTEGER_NUMS < 2:  # Need at least two numbers to multiply with you retard.
        print("FileError: Reverting integer_nums to defaults due to invalid values.")
        config['Settings']['integer_nums'] = '2'
        INTEGER_NUMS = 2

    if isinstance(PROBLEM_NUMS, str) or PROBLEM_NUMS < 1:  # Need at least one problem to solve you goy.
        print("FileError: Reverting problem_nums to defaults due to invalid values.")
        config['Settings']['problem_nums'] = '10'
        PROBLEM_NUMS = 10

    if PRINT_SETTINGS:  # Print settings if bool is True on startup.
        for setting_category in config.sections():
            print(f'[{setting_category}]')
            for setting_option, setting_value in config.items(section):
                print(f'{setting_option} = {setting_value}')
            print()  # Spacing

    with open(configure_file, 'w') as configfile:  # Do all the queued up changes at once.
        config.write(configfile)


def settings_menu():
    """Settings Menu function: Allows the user to configure options to his/her liking. Checks for error situations."""
    while True:
        user_input = input('> Settings? (Type "help", a command, or Enter): ').strip().split(' ')
        user_input = convert_digits(user_input)
        global MIN, MAX, INTEGER_NUMS, PROBLEM_NUMS, PRINT_SETTINGS, TRACK_TIMER

        if len(user_input) == 1 and user_input[0] == "help":
            print("─────[Help Page]─────\n"
                  "help                  : Brings up the help page.\n"
                  "min            <int>  : Alters the minimum integer that can be generated.\n"
                  "max            <int>  : Modifies the maximum integer that can be generated.\n"
                  "integer_nums   <int>  : Changes the number of integers being multiplied.\n"
                  "problem_nums   <int>  : Increase or decrease the number of problems present.\n"
                  "track_timer    <bool> : Dictate whether the program tracks time or not.\n"
                  "print_settings <bool> : Whether the settings print on startup or not.\n"
                  "─────────────────────")
        elif len(user_input) == 2 and user_input[0] == "min" and type(user_input[1]) == int:
            if user_input[1] > MAX:  # Catch min > max error before the program shits itself.
                print("Error: Minimum cannot be set above maximum.")
            else:
                print(f'min set to: {user_input[1]} from: {MIN}')
                config['Settings']['min'] = f'{user_input[1]}'
                MIN = user_input[1]
        elif len(user_input) == 2 and user_input[0] == "max" and type(user_input[1]) == int:
            if user_input[1] < MIN:
                print("Error: Maximum cannot be set below minimum.")
            else:
                print(f'max set to: {user_input[1]} from: {MAX}')
                config['Settings']['max'] = f'{user_input[1]}'
                MAX = user_input[1]
        elif len(user_input) == 2 and user_input[0] == "integer_nums" and type(user_input[1]) == int:
            if user_input[1] < 2:
                print("Error: Numbers of integers cannot be set below two.")  # Need two numbers to multiply, retard...
            else:
                print(f'integer_nums set to: {user_input[1]} from: {INTEGER_NUMS}')
                config['Settings']['integer_nums'] = f'{user_input[1]}'
                INTEGER_NUMS = user_input[1]
        elif len(user_input) == 2 and user_input[0] == "problem_nums" and type(user_input[1]) == int:
            if user_input[1] < 1:
                print("Error: You need at least one problem to solve.")
            else:
                print(f'problem_nums set to: {user_input[1]} from: {PROBLEM_NUMS}')
                config['Settings']['problem_nums'] = f'{user_input[1]}'
                PROBLEM_NUMS = user_input[1]
        elif len(user_input) == 2 and user_input[0] == "track_timer" and type(user_input[1]) == str:
            if user_input[1].capitalize() not in ["True", "False"]:
                print('Error: Booleans can only be used ("True" or "False").')
            else:
                print(f'track_timer set to: {user_input[1].capitalize()} from: {TRACK_TIMER}')
                config['Settings']['track_timer'] = f'{user_input[1].capitalize()}'
                TRACK_TIMER = bool_map[user_input[1].capitalize()]
        elif len(user_input) == 2 and user_input[0] == "print_settings":
            if user_input[1].capitalize() not in ["True", "False"]:
                print('Error: Booleans can only be used ("True" or "False").')
            else:
                print(f'print_settings set to: {user_input[1].capitalize()} from: {PRINT_SETTINGS}')
                config['Settings']['print_settings'] = f'{user_input[1].capitalize()}'
                PRINT_SETTINGS = bool_map[user_input[1].capitalize()]
        elif user_input[0] in ["", "quit", "exit", "q"]:
            print("Leaving settings menu...")
            return
        else:
            print('Invalid command. Try "help".')

        with open(configure_file, 'w') as configfile:
            config.write(configfile)


def game_logic():
    """Game Logic function: Calculates how many problems to print, displays them, grades you, and other shit."""
    while True:
        list_of_generated_ints = generate_random_ints()
        correctness_amount, final_time = _print_problems_and_solve(list_of_generated_ints)

        if TRACK_TIMER:  # Show timer if enabled.
            print(
                f"⏱️ Time took: {round(final_time, 3)} secs | Average time per question: {round(final_time / PROBLEM_NUMS, 3)} secs")
        correctness_grade = correctness_amount / PROBLEM_NUMS
        _grade_rank(correctness_grade, correctness_amount)

        continue_ask1 = input('> Continue? (Type "settings", "quit", or Enter): ')
        if continue_ask1.lower() == "settings":
            settings_menu()
        elif continue_ask1.lower() in ["y", "yes", "ye", '']:
            continue
        else:
            print("Terminating program...")
            exit()


# Play, interact, or fuck off
def main():
    while True:
        continue_ask = input('> Play? (Type "settings" or Enter): ')
        if continue_ask.lower() in ["y", "yes", "ye", '']:
            game_logic()
        elif continue_ask.lower() == "settings":
            settings_menu()
        else:
            print("Terminating program...")
            exit()


if __name__ == "__main__":
    initial_file_check()  # Check if files are fucky or not, auto-adjusts.
    main()
