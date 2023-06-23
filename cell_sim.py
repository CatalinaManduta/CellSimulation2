"""
Simulation Setup Module
-----------
Authors: Catalina Manduta and Justin Di Giorgio.
-----------
This module, part of a larger cell evolution simulation project, is responsible for setting up the simulation. Users can
 configure several parameters including the grid setup (which is a representation of the cell environment imported from
 a .txt file), the time limit of the simulation, and the initial cell population.

Each setup has its own predefined preconditions that the input from users must satisfy. The module also provides a
flexible error handling system, guiding users to fix their inputs if they don't follow the preconditions, or offering
options to return to the main menu or exit the program.

The module is designed to interact with other modules in the program, such as a 'data' module (represented as 'd' in
this script) for storing simulation data, and a 'simulation' module (represented as 'c' in this script) which handles
the core logic of the simulation.
"""



import simulation as c
import data as d


def description() -> None:
    """This function wil print information about the program."""
    print("___________________________________________________________________________________________________\n"
          "\tThis program's purpose is to simulate the development of cells and their evolution over time when\n"
          " subject to selective pressure from the environment. \n"
          "___________________________________________________________________________________________________\n"
          "\tYou will be asked to set up the simulation parameters, by introducing a text file, together with \n"
          "the time limit you wish the simulation to have as well as the initial cell population.\n"
          "___________________________________________________________________________________________________")
    precondition("Please pay attention to the preconditions of each simulation setting.")


# Configuration ####

# Functions to help collect and inform the user in a more efficient way
def error_options() -> None:
    """
    This function gives extra options in case the user inserts an invalid value. The user has 3 options: Try again,
    Return to the main menu and Exit program. Depending on the choice, the function attached to the choice will be
    executed.
    """
    try:
        new_choice = int(input("___________ERROR___________\n"
                               "Please choose between:\n"
                               "1. Try again\n"
                               "2. Return to the main menu\n"
                               "3. Exit program\n"
                               "INSERT YOUR CHOICE HERE: "))
        options = [1, 2, 3]  # list with all accepted options
        if new_choice not in options:
            attention("The value must be between 1 and 3! Please try again!")
            error_options()
        elif new_choice == 1:
            pass
        elif new_choice == 2:
            main_menu()
        elif new_choice == 3:
            print("Goodbye!")
            exit()
    except ValueError:
        attention("The inserted value must be a number.Please try again!")
        error_options()


def choice_collector(input_text: str, error: str, maximum=0) -> int:
    """This function will collect the input and will check if the collected input is in accordance with the given
    preconditions. If the precondition is not respected it will return error_options() function to give further
    options.
    The arguments for this function are:
    Input: input_text = the text shown to the user requiring the input, together with the precondition;
           maximum = the maximum value is predefined to 0 but it can be modified when a maximum value is needed;
           error = the error informing the user that the value does not follow the precondition.
    Output: int
    """
    try:
        choices = int(input(input_text))
        if choices < 1:  # check if the value is minimum 1
            attention(error)
            error_options()
            simulation_setup()
        elif maximum != 0 and choices > maximum:  # check if the maximum argument was modified in order to know if
            # there is a maximum value needed for this simulation setting as well as checking if the input is higher
            # than the maximum value accepted
            attention(error)
            error_options()
            simulation_setup()
        else:
            return choices
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        return choice_collector(input_text, error, maximum)


def attention(string, prints=True) -> str:
    """
    This function prints the string, by default, as an "Attention" string.
    """
    string = "\033[1;31mATTENTION: " + string + "\033[0;0m"
    if prints:
        print(string)
    return string


def precondition(string, prints=True) -> str:
    """
    This function prints the string, by default, as a "Precondition" string.
    """
    string = "\033[1;34mPRECONDITION: " + string + "\033[0;0m"
    if prints:
        print(string)
    return string


def valid_character(string) -> bool:
    """
    The function will check if the given argument is among the list with the possible options. The function
    will return True if the string is among the accepted values and False otherwise.
    Input: str
    Output: bool
    """
    lst = ['%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if string in lst:
        return True
    else:
        return False


def display_configurations() -> None:
    """
    This function will display the parameters, by accessing the relevant values saved in the simulation instance class.
    """
    print("_____________________________")
    print("Parameters \t\t   Value")
    print("_____________________________")
    print("Grid rows            ", d.Data.get_inst().rows)
    print("Grid columns         ", d.Data.get_inst().cols)
    print("Initial population   ", d.Data.get_inst().population)
    print("Time limit           ", d.Data.get_inst().time_limit)
    print("File name            ", d.Data.get_inst().grid_file_name)
    print("______________________________")


def grid_setup() -> None:
    """Function that reads the text file, checks if the file respects the preconditions and updates
    the data.py module."""
    try:
        precondition("The only accepted files are .txt files. \n"
                     "The grid must only contain % or digits (0-9) with at list one habitable (digits from 0 to 9) "
                     "patch.\n"
                     "Also the grid must be rectangular at least 3x3, with rows delimited by the new line character"
                     "(\\n).")
        print("The current file for the grid is:", d.Data.get_inst().grid_file_name)
        d.Data.get_inst().grid_file_name = input("Please type the name of your grid file e.g. (grid.txt) here:  ")
        check_grid()  # check if the grid  contains only valid characters, is rectangular, has minimum 3 by 3
        # dimensions and the file is of the correct type
        check_obstacles()  # check if the nr. of obstacles on the grid is smaller than the nr. of total patches
        d.Data.get_inst().grid_first = True  # changing the d.Data.get_inst().grid_first to keep track of the fact
        # that the grid has been inserted
        print("Successfully changed! The new grid file is ", d.Data.get_inst().grid_file_name)
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        grid_setup()


def time() -> None:
    """Function that requires the user to input the time limit for the simulation, checks it respects the preconditions
     and updates the data.py module."""
    try:
        precondition("The value must have minimum 1!")
        print("The current value for the simulation time limit is:", d.Data.get_inst().time_limit)
        time_limit = choice_collector("Please insert the time limit you would like to have: ",
                                      "The value must be minimum 1! Please try again!")
        d.Data.get_inst().time_limit = time_limit
        print("Successfully changed! The new time limit is ", d.Data.get_inst().time_limit)
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        time()


def population_cells() -> None:
    """Function that requires the user to input the population size for the simulation, checks it respects the preconditions
         and updates the data.py module."""
    try:
        if d.Data.get_inst().grid_first:
            limit = d.Data.get_inst().habitable  # the maximum number of patches that can house cells
            precondition("The value must have minimum 1 and a maximum of" + str(limit) + "which represents the "
                                                                                         "number of patches free of obstacles.")
            print("The current value for the simulation population is:", d.Data.get_inst().population)
            population = choice_collector("Please insert the initial population you would like to have: ",
                                          "The value must be between 1 and " + str(limit) + ".Please try again.",
                                          maximum=limit)
            d.Data.get_inst().population = population  # updating the cell population
            print("Successfully changed! The new value for the initial population is:", d.Data.get_inst().population)
            simulation_setup()
        else:
            attention("Please setup first the grid setting.")
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        population_cells()


def simulation_setup() -> None:
    """This function will allow the user to insert / change the grid file, the initial size population and the time
    limit for the simulation, according to predefined preconditions. After each simulation setup the user will be sent
    back to the simulation setup menu. In case the inserted value is not accepted the error_options() function will be
    executed.
    Modifies: d.Data.get_inst().grid_file_name, d.Data.get_inst().time_limit, d.Data.get_inst().population. """
    try:
        choice = int(input("_______Simulation Setup_______\n"
                           "\t1. Grid\n"
                           "\t2. Time limit\n"
                           "\t3. Initial cell population\n"
                           "\t4. Return to the main menu\n"
                           "\t5. Exit\n"
                           "Please choose from the following configuration settings:  "))
        if choice == 1:  # grid text file setup
            grid_setup()
            simulation_setup()
        elif choice == 2:  # time limit setup
            time()
            simulation_setup()
        elif choice == 3:  # input request for initial cell population setup
            population_cells()
            simulation_setup()
        elif choice == 4:
            main_menu()
        elif choice == 5:
            print("Goodbye!")
            exit()
        else:
            attention("The inserted value is not an option. Please try again!")
            error_options()
            simulation_setup()
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        simulation_setup()


def check_grid() -> None:
    """
        The function will create the grid with the corresponding patches by reading in the text file.
    In order to do so the function will first check if all the characters in grid file are accepted, this is done by
    making use of the valid_character() function.
        The function also checks if the shape of the grid is rectangular, as well as if the number of rows and
    columns is minimum 3.
        It raises error if the file was not found in the directory or if the file is not of a correct type.
    Returns: List[List[str]]
    """
    grid = ""
    try:
        with open(d.Data.get_inst().grid_file_name, 'r') as file:
            for line in file:
                grid += line
        grid = grid.split("\n")
        grid = [list(i) for i in grid]
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not valid_character(grid[i][j]):  # string only contains % and 0-9
                    attention("Grid characters must be either % or a digit (0-9)")
                    d.Data.get_inst().grid_file_name = ""  # reset the name of the d.Data.get_inst().grid_file_name to an empty string
                    simulation_setup()
                if len(grid[i]) != len(grid[0]):  # checks if the shape is rectangular
                    attention("Grid file is not rectangular. Please input a rectangular grid!")
                    d.Data.get_inst().grid_file_name = ""  # reset the name of the d.Data.get_inst().grid_file_name to an empty string
                    simulation_setup()
                if len(grid[i]) < 3 or len(grid[0]) < 3:  # checks if the grid's dimensions is at least 3 by 3
                    attention("The rows and columns must be minimum 3. Please try again!")
                    d.Data.get_inst().grid_file_name = ""  # reset the name of the d.Data.get_inst().grid_file_name to an empty string
                    simulation_setup()
    except FileNotFoundError:  # error in the case the inserted file was not found
        attention("The file name was either not inserted or does not exist in the given directory. Please try again!")
        d.Data.get_inst().grid_file_name = ""
        error_options()
        simulation_setup()
    except (ValueError, OSError,):  # error in case the inserted file is not of a correct type (.txt) or the inserted
        # name is not accepted (OSError) e.g. (new grid)
        attention("The inserted file type was not accepted. Please try again!")
        d.Data.get_inst().grid_file_name = ""
        error_options()
        simulation_setup()
    except IndexError:
        attention("The inserted file may contain spaces. Please try again!")
        d.Data.get_inst().grid_file_name = ""
        error_options()
        simulation_setup()


def check_obstacles() -> None:
    """Function that checks how many obstacles are in the given grid file.
    In the case the file contains only obstacles without habitable patches, and error will occur and the user will be
    sent back to the simulation setup to add a new file.
    Modifies : d.Data.get_inst().habitable
    """
    obstacles = 0  # keep track of the number of obstacles on the grid
    grid = ""
    with open(d.Data.get_inst().grid_file_name, 'r') as file:
        for line in file:
            grid += line
    # string only contains % and 0-9
    grid = grid.split("\n")
    grid = [list(i) for i in grid]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "%":
                obstacles += 1  # update obstacles variable every time it encounters a "%" character
    if len(grid) * len(grid[0]) == obstacles:
        attention("The inserted file does not contain any habitable patches! Please try again!")
        d.Data.get_inst().grid_file_name = ""  # reset the name of the d.Data.get_inst().grid_file_name to an empty string
        error_options()
        simulation_setup()
    d.Data.get_inst().habitable = (len(grid) * len(grid[0])) - obstacles  # update the value with all the habitable patches


def main_menu() -> None:
    """
    The function gives the user the possibility to chose between several options.
    """
    try:
        choice = int(input('''Please select one of the following actions:\n
        \t_________Main Menu_________
        \t1. Display configuration\n
        \t2. Simulation setup\n
        \t3. Run simulation\n
        \t4. Exit\n
        \t INSERT YOUR CHOICE HERE: '''))
        if choice == 1:
            display_configurations()
            main_menu()
        elif choice == 2:
            simulation_setup()
            main_menu()
        elif choice == 3:
            if d.Data.get_inst().population == 0 or d.Data.get_inst().time_limit == 0:  # check if the values for the population and
                # the time limit have been changed from 0 to a new value.
                attention("Please setup the population and the time limit settings!")
                error_options()
                main_menu()
            else:
                # check again the grid in the case the user modifies the values directly in the data.py
                check_grid()
                check_obstacles()
                # run the simulation, print the statistics and the graph and reset the values to 0
                c.run_simulation()
                c.print_statistics()
                c.graph()
                d.Data.get_inst().reset_data()  # reset the values inside the Data class
                main_menu()
        elif choice == 4:
            print("Goodbye!")
            exit()
        else:
            attention("The value must be between 1 and 4! Please try again!")
            error_options()
            main_menu()
    except ValueError:
        attention("The inserted value must be a number. Please try again!")
        error_options()
        main_menu()


if __name__ == "__main__":
    description()
    main_menu()

