"""
Data Module
-----------
Authors: Catalina Manduta and Justin Di Giorgio.
-----------
This module defines the `Data` class, which is implemented as a Singleton. The class is designed to encapsulate and
manage all the necessary variables and data related to a simulation, providing a central repository for statistics and
information about the state of the system. The `Data` class manages data about the simulation's population, time limit,
grid dimensions, number of habitable patches, and whether a grid file has been loaded. It keeps track of the list of
patches for the simulation, the number of cells involved, along with various statistics about cell death causes and the
number of ticks that have passed in the simulation. Class methods include getter and setter methods for appending to and
retrieving data from the patches and generations lists, methods for incrementing the number of cells, the number of deaths,
deaths by various causes, and the time elapsed in the simulation. A `reset_data` method is also provided to reset all the
class attributes, effectively resetting the state of the simulation.
"""


class Data:
    """
    Represents a simulation. Saves all the values needed for simulation to proceed.
    Parameters: population: int, time_limit:int and grid_file: str.

    Other attributes contained by this class are:
        patches: the list of patches for the simulation;
        generation_pop: list of generations and cellular resistance;
        rows: the number of rows read in the grid file;
        cols: the number of columns read in the grid file;
        habitable: the number of patches that can be inhabited by cells;

        cells: number of cells int the simulation;
        deaths_age: the number of cells that died duo to exceeding the age limit;
        deaths_division: the number of cells that died duo to exceeding the division limit;
        deaths_poisoning: the number of cells that died duo to poisoning;
        deaths: total deaths;
        time: the time that has passed so far in the simulation;
        grid_first: True if the grid file was inserted, False otherwise;"""
    _instance = None
    # So the main difference between _variable and __variable is that the first one is a convention indicating that the
    # variable is intended for internal use within the class and should not be accessed directly from outside the class,
    # but it still can be accessed. The second one is an implementation detail, which the interpreter uses to avoid
    # naming conflicts between class variables and instance variables, and it is not intended to be accessed directly
    # from outside the class.

    @classmethod
    def get_inst(cls):
        """ Class method through which returns the class instance. """
        if cls._instance is None:
            cls()
        return cls._instance

    # Statistics Global Variable
    def __init__(self, population=5, time_limit=50, grid_file_name="grid_3.txt"):
        # External class attributes which are gone be accessed by the user
        if Data._instance is not None:
            raise Exception("This class is a singleton!")  # ensure that there is just one instance of the Data class
        else:
            Data._instance = self
        self.population = population  # saves the population input from the user
        self.time_limit = time_limit  # saves the time limit input from the user
        self.grid_file_name = grid_file_name  # saves the file name from the user
        self.rows = 0  # saves the number of rows read from the grid file
        self.cols = 0  # saves the number of columns read from the grid file
        self.habitable = 0  # save the number of habitable patches on the grid
        self.grid_first = False  # checks if the grid file has been introduced or not

        # Internal class attributed only accessed by the program
        # Lists
        self._patches = []  # List(Patch): the list of patches for the simulation
        self._generations = []

        # Integers
        self._cells = 0  # the number of cells involved in the simulation
        self._deaths_age = 0  # the number of cells that died duo to exceeding the age limit
        self._deaths_division = 0  # the number of cells that died duo to exceeding the division limit
        self._deaths_poisoning = 0  # the number of cells that died duo to poisoning
        self._deaths = 0  # total deaths
        self._time = 0  # the number of ticks passed

    # Methods
    def patches(self, value=0, return_value=False) -> list:
        """Class method that either appends a value to the _patches class attribute or returns the list.
         Input: value = the value that need to be appended;
                return_value = if the list should be returned.
        Output: list[patches] = a list of patches.
        """
        if not return_value:
            self._patches.append(value)
        elif return_value:
            return self._patches

    def generations(self, value=0, index=0, return_value=False) -> list:
        """Class method that either appends a value to the _generations class attribute or returns the list.
         Input:
                value [list] = the value that need to be appended;
                index [int] = the index where the value must be inserted;
                return_value = if the list should be returned.
        Output:
                list[list[int]] = a list which index represents the generation and the integers represents the cell's
                resistance.
            """
        if not return_value:
            self._generations.append([])  # add a new list in order to avoid out of index error when slicing it
            self._generations[index].append(value)
        elif return_value:
            return self._generations

    def increase_cell(self, value) -> int:
        """Method that increases the number of cells by the value introduced as parameter and returns self._cells.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
        """
        self._cells += value
        return self._cells

    def increase_deaths(self, value) -> int:
        """Method that increases the number of death cells by the value introduced as parameter and
        returns self._deaths.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
        """
        self._deaths += value
        return self._deaths

    def increase_deaths_age(self, value) -> int:
        """Method that increases the number of death cells that died duo to age by the value introduced as parameter
        and returns self._deaths_age.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
        """
        self._deaths_age += value
        return self._deaths_age

    def increase_deaths_poisoning(self, value) -> int:
        """Method that increases the number of death cells that died duo to poisoning by the value introduced as
        parameter and returns self._deaths_poisoning.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
        """
        self._deaths_poisoning += value
        return self._deaths_poisoning

    def increase_deaths_div(self, value) -> int:
        """Method that increases the number of death cells that died duo to division limit by the value introduced as
        parameter and returns self._deaths_poisoning.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
        """
        self._deaths_division += value
        return self._deaths_division

    def increase_time(self, value) -> int:
        """Method that increases the time passed by the value introduced as parameter and returns self._time.
        Input:
            value: the value with which the class attribute should be increased;
        Output:
            return the class attribute.
                """
        self._time += value
        return self._time

    def reset_data(self) -> None:
        """
        Method that restarts all the class attributes. The attributes represented by integers are restarted to 0, the
        attributes represented by lists are restarted to empty lists and the attributes represented by boolean to False.
        """
        self.population = 0  # saves the population input from the user
        self.time_limit = 0  # saves the time limit input from the user
        self.grid_file_name = ""  # saves the file name from the user
        self.rows = 0  # saves the number of rows read from the grid file
        self.cols = 0  # saves the number of columns read from the grid file
        self.habitable = 0  # save the number of habitable patches on the grid
        self.grid_first = False

        self._patches = []  # List(Patch): the list of patches for the simulation
        self._generations = []

        self._cells = 0  # the number of cells involved in the simulation
        self._deaths_age = 0  # the number of cells that died duo to exceeding the age limit
        self._deaths_division = 0  # the number of cells that died duo to exceeding the division limit
        self._deaths_poisoning = 0  # the number of cells that died duo to poisoning
        self._deaths = 0  # total deaths
        self._time = 0  # the number of ticks passed
        self._instance = 0



