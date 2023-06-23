"""
Module: Cellular Life Simulation
--------------------------------
Authors: Catalina Manduta and Justin Di Giorgio.
--------------------------------
This module, part of the Cellular Life Simulation package, governs the simulation of life of cells within a grid-based
ecosystem. The code sets up the grid, populates it with cells, regulates the life processes of the cells (including
growth, reproduction, and death), and tracks and reports the population statistics over time.

Key functions include grid setup and population, neighborhood determination for cellular interaction, simulation running
 with life cycle management, and reporting through printing of final statistics and generation of graphical displays.
"""

import model as m
import random as r
import visualiser as v
import matplotlib.pyplot as plt
import data as d


# Simulation #######################################################
def read_grid() -> list:
    """
    The function will create the grid with the corresponding patches by reading in the text file.
    Output: list.
    """
    grid = ""
    with open(d.Data.get_inst().grid_file_name, 'r') as file:
        for line in file:
            grid += line
    grid = grid.split("\n")
    grid = [list(i) for i in grid]
    return grid


def create_patches(grid) -> None:
    """
    This function is passed a 2D list and then modifies patches to create either obstacle or cell patches depending
    on the values in grid.
    Input: a grid containing obstacles or habitable patches
    Modifies: d.Data.get_inst().patches
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '%':  # create an obstacle patch
                grid[i][j] = m.ObstaclePatch(i, j)
            else:  # create an habitable patch
                grid[i][j] = m.CellPatch(i, j, int(grid[i][j]))
            d.Data.get_inst().patches(grid[i][j])
            print(d.Data.get_inst().patches(return_value=True))


def get_cell_patches() -> list:
    """
    This function checks which of the patches are an instance of the CellPatch, and returns a list containing them.
    Output: list
    """
    return [x for x in d.Data.get_inst().patches(return_value=True) if x.can_host_cell()]


def initialise_population() -> None:
    """
    The function will insert the cells from the initial population at random positions on the grid.
    Modifies: d.Data.get_inst().patches, d.Data.get_inst().generation_pop, d.Data.get_inst().cells.
    """
    # make sure take min between number of CellPatches and default population
    population = min(d.Data.get_inst().population, len([x for x in d.Data.get_inst().patches(return_value=True) if x.can_host_cell()]))
    d.Data.get_inst().increase_cell(d.Data.get_inst().population)   # counting the initial population to the
    # choose random positions on the grid
    extract_random_patches = r.sample([x for x in d.Data.get_inst().patches(return_value=True) if x.can_host_cell()],
                                      k=population)
    for i in extract_random_patches:
        cell = m.Cell(i, r.choice(range(10)))  # create new cell with random resistance from 0-9
        i.put_cell(cell)  # insert the cell on the patch
    first_cells = [x.cell() for x in get_cell_patches() if x.has_cell()]
    first_cells = [i.resistance() for i in first_cells]
    for i in range(len(first_cells)):
        d.Data.get_inst().generations(value=first_cells[i])


# Functions related to patches management
def get_neighbours(patch) -> list:
    """
    Takes a patch and returns a list of its neighbours
    Input: Patch
    Output: List(Patch)
    """
    width = d.Data.get_inst().cols
    height = d.Data.get_inst().rows
    nearby = []
    col = patch.col()
    row = patch.row()
    for i in range(3):  # i = 0,1,2
        for j in range(3):  # j = 0,1,2
            if i == j == 1:  # don't add the patch to the list of neighbours
                continue
            new_row = (row + i - 1) % height  # we take the modulo so that the row is not negative or over the width
            new_col = (col + j - 1) % width  # we take the modulo so that the col is not negative or over the height
            index = new_row * width + new_col  # index of the patch in patches
            # needs the -1 because range(2) is 0,1,2. So we subtract 1 to get -1, 0, 1 for the rows and columns.
            # we want -1, 0, 1 so the index looks left (-1) centre (0) and right(1) for the column.
            nearby.append(d.Data.get_inst().patches(return_value=True)[index])  # add the patch to the list
    return nearby


def life() -> None:
    """
    This function iterates over all CellPatches. It first ticks them then attempts to divide any live cells that have
    an empty neighbour. It updates the statistics for total cells accordingly.
    Input: None
    Output: None
    Modifies: d.Data.get_inst().patches(), d.Data.get_inst().generations()
    """
    cell_patches = get_cell_patches()  # [CellPatch(row = 1, col = 0, toxicity = 0, has_cell = None),
    # CellPatch(row = 1, col = 1, toxicity = 0, has_cell = None), etc]
    cell_patches = [x for x in cell_patches if x.has_cell()]
    cell_patches = r.sample(cell_patches, len(cell_patches))
    # Tick every alive cell
    for patch in cell_patches:
        patch.cell().tick()
        # Death Statistics
    # Check reproduction for every alive cell after we tick
    for patch in cell_patches:
        # Cell must be alive. Cell could have died from ticking
        if patch.has_cell() and patch.cell().is_alive():
            # Reproduction
            neighbours = get_neighbours(
                patch)  # [ObstaclePatch(row = 0, col = 12), ObstaclePatch(row = 0, col = 13),
            # ObstaclePatch(row = 0, col = 14), CellPatch(row = 1, col = 12, toxicity = 0,
            neighbours = [x for x in neighbours if x.can_host_cell()]
            neighbours = [x for x in neighbours if not x.has_cell()]
            if len(neighbours) == 0:  # if list is empty, no place where the cell can divide
                pass
            else:
                # attempt division

                # list to the d.Data.get_inst().generation_pop
                new_patch = r.choice(neighbours)
                cell = patch.cell()
                # if division occurred
                if cell.divide(patch=new_patch):
                    d.Data.get_inst().increase_cell(1)  # update the number of total cells in this simulation
                    d.Data.get_inst().generations(value=new_patch.cell().resistance(), index=new_patch.cell().generation())


def cleanup_dead():
    """
    This function will iterate over all CellPatches and checks if they have a dead cell. If True, it will update the
    statistics for total deaths and causes of death.
    Modifies: d.Data.get_inst().deaths, d.Data.get_inst().deaths_age, d.Data.get_inst().deaths_poisoning, d.Data.get_inst().deaths_division.
    """
    cell_patches = get_cell_patches()
    for i in cell_patches:
        if i.has_cell() and not i.cell().is_alive():
            cell = i.cell()
            d.Data.get_inst().increase_deaths(1)
            if cell.died_by_age_limit():
                d.Data.get_inst().increase_deaths_age(1)
            if cell.died_by_poisoning():
                d.Data.get_inst().increase_deaths_poisoning(1)
            if cell.died_by_division_limit():
                d.Data.get_inst().increase_deaths_div(1)
            i.remove_cell()


# Functions to run the simulation
def check_any_cell() -> bool:
    """
    The function checks if there is a cell on the grid.
    Returns: bool
    """
    cell_patches = get_cell_patches()
    for patch in cell_patches:
        if patch.has_cell():
            return True


def run_simulation() -> None:
    """
    This function helps visualize and update the grid as long as the time is below the limit and the grid is not empty.
    modifies: simulation
    """
    grid = read_grid()
    d.Data.get_inst().rows = len(grid)  # set up the number of rows read from the file
    d.Data.get_inst().cols = len(grid[0])  # set up the number of columns read from the file
    create_patches(grid)
    initialise_population()
    vis = v.Visualiser(d.Data.get_inst().patches(return_value=True), d.Data.get_inst().rows, d.Data.get_inst().cols)
    while d.Data.get_inst().increase_time(0) < d.Data.get_inst().time_limit:
        any_cell = check_any_cell()  # check if any cell is left on the grid
        if any_cell:
            # ticks, reproduction/dividing, count generations, resistances, population
            life()
            # remove dead cells, counts total deaths and deaths from specific causes
            cleanup_dead()
            vis.update()  # updates visualiser
            d.Data.get_inst().increase_time(1)  # update the time in order to know when to stop the simulation
        else:
            break
    vis.close()


# Reporting #########################################################
def print_statistics() -> None:
    """
    This function will display the final statistics by printing the relevant stored class attributes.
    """
    generation_pop = [x for x in d.Data.get_inst().generations(return_value=True) if x != []]
    # delete all the empty lists
    for i in range(len(generation_pop)):
        print("Generation",  i, ":", generation_pop[i])
    largest_pop = max([len(i) for i in generation_pop])  # check which generation had the largest population
    # check which is the oldest generation
    largest_gen = [i for i in range(len(generation_pop)) if len(generation_pop[i]) == largest_pop]
    # Print different statistics
    print("         ------------- Statistics -------------")
    print("Time covered by the simulation (ticks):", d.Data.get_inst().increase_time(0))
    print("Total cells created during the simulation:", d.Data.get_inst().increase_cell(0))
    print("Largest Generation(s):", largest_gen, "with a population of", largest_pop)
    print("Number of Generations", len(generation_pop))
    print("Breakdown of Deaths")
    print("\t Total deaths", d.Data.get_inst().increase_deaths(0))
    print("\t\t Age Limit deaths", d.Data.get_inst().increase_deaths_age(0))
    print("\t\t Division Limit deaths", d.Data.get_inst().increase_deaths_div(0))
    print("\t\t Poisoning deaths", d.Data.get_inst().increase_deaths_poisoning(0))
    return None


def graph():
    """
    This function uses d.Data.get_inst().generation_pop to look at the lengths and resistance of cell populations and create
    a graphic display for the user.
    """
    lst = [x for x in d.Data.get_inst().generations(return_value=True) if x != []]
    gens = len(lst)  # the number of generations
    averages = [sum(x) / len(x) for x in lst]  # average resistence per generation
    maxes = [max(x) for x in lst]  # max resistence per generation
    mins = [min(x) for x in lst]  # min resistence per generation
    pops = [len(x) for x in lst]  # lengths of each generation

    # Plotting avg, min, max resistance by generation
    figure, axis = plt.subplots(2, 1)
    axis[0].plot(range(gens), averages, label='avg')
    axis[0].plot(range(gens), maxes, label='max')
    axis[0].plot(range(gens), mins, label='min')
    axis[0].set_ylabel("Resistance")
    axis[0].set_xlabel("Generation")
    axis[0].grid(True)

    #  Plotting population by generation
    axis[1].plot(range(gens), pops)
    axis[1].set_ylabel("Population")
    axis[1].set_xlabel("Generation")
    axis[1].grid(True)

    axis[0].legend()
    figure.tight_layout()

    plt.show()
