"""
Cellular Automaton Simulation Module
------------------------------------
Authors: Catalina Manduta and Justin Di Giorgio
------------------------------------
This module defines the classes necessary for a cellular automaton simulation, where a grid of patches hosts
single-celled organisms. The grid consists of habitable patches (CellPatch) or obstacles (ObstaclePatch).

The Cell class represents an organism in the simulation, which can age, divide, and die due to various causes such as
toxicity, old age, or overdivision. The probability of cell division is influenced by individual resistance and
simulation parameters.

The BasePatch class and its subclasses, CellPatch and ObstaclePatch, represent points on the simulation grid.
CellPatch can host a cell and contains a toxicity level, while ObstaclePatch acts as an obstacle in the simulation
grid.
"""


import random as r


class BasePatch:
    """Represents a 'patch' at the intersection of the given row and column of the simulation grid.

    Parameters row, col: int

    The index of the row and column containing this patch.

    Subclasses: CellPatch, ObstaclePatch"""

    def __init__(self, row: int, col: int):
        """
        Parameters
        ----------
        row, col: int
          The index of the row and column containing this patch.
        """
        self._col = col
        self._row = row

    def can_host_cell(self):
        """Returns whether this patch can be inhabited by cells."""
        if isinstance(self, CellPatch):
            return True
        else:
            return False

    def col(self):
        """Returns the index of the column containing this patch."""
        return self._col

    def row(self):
        """Returns the index of the row containing this patch."""
        return self._row


class CellPatch(BasePatch):
    """Represents a patch at the intersection of the given row and column of the simulation grid that a cell can
    inhabit.
    Parameters row, col :int

    The index of the row and column containing this patch.
    poison :int

    The level of poison found in this patch.

    Ancestors: BasePatch."""
    def __init__(self, row, col, toxicity):
        super().__init__(row, col)
        self._toxicity = toxicity
        self._cell = None

    def __repr__(self):
        string = "CellPatch(row = " + str(self._row) + \
                 ", col = " + str(self._col) + \
                 ", toxicity = " + str(self._toxicity) + \
                 ", has_cell = " + str(self._cell) + ")"
        return string

    def cell(self):
        """Returns the cell currently on this patch, if any."""
        return self._cell

    def has_cell(self) -> bool:
        """Checks if the patch holds a cell."""
        if self._cell is not None:
            return True

    def put_cell(self, cell) -> None:
        """
        Puts a cell on this patch.

        Preconditions: there is no cell on this patch and the cell is not on another patch"""
        assert not self.has_cell(), "This patch has a cell."
        assert (cell.patch() is self), "The cell is on this patch."
        self._cell = cell

    def remove_cell(self) -> None:
        """ Removes any cell currently on this patch."""
        self._cell = None

    def toxicity(self) -> int:
        """Returns the toxicity level of this patch."""
        return self._toxicity


class ObstaclePatch(BasePatch):
    """Represents an obstacle (a patch that cannot have a cell) at the intersection of the given row and column of the
    simulation grid.

        Parameters: row, col: int

        The index of the row and column containing this patch.

        Ancestors BasePatch
        Inherited members: BasePatch: can_host_cell col row.

        """
    def __init__(self, row, col):
        super().__init__(row, col)

    def __repr__(self):
        string = "ObstaclePatch(row = " + str(self._row) + \
                 ", col = " + str(self._col) + ")"
        return string


class Cell:
    """Represents a cell in the simulation."""
    age_limit = 10
    division_limit = 3
    division_probability = 0.6
    division_cooldown = 1

    def __init__(self, patch, resistance, generation=0, parent=None):
        # class attributes
        # should a cell be able to have no patches?
        self._patch = patch
        self._age = 0
        self._divisions = 0
        self._last_division = 0
        self._alive = True
        self._died_by_poisoning = False
        self._died_by_age_limit = False
        self._died_by_division_limit = False
        self._resistance = resistance
        self._generation = generation
        self._parent = parent

    def __repr__(self):
        string = "Cell(age = " + str(self._age) + \
                 ", divisions = " + str(self._divisions) + \
                 ", resistance = " + str(self._resistance) + \
                 ", generation = " + str(self._generation) + "\n" + \
                 "\t\talive = " + str(self._alive) + \
                 ", poisoned = " + str(self._died_by_poisoning) + \
                 ", old age = " + str(self._died_by_age_limit) + \
                 ", overdivided = " + str(self._died_by_division_limit) + ")"
        return string

# Static method
    @staticmethod
    def resistance_inheritance(res, minimum=0, maximum=9) -> list:
        """Function that returns a list with the resistance values that can be inherited by a cell."""
        lst = [i for i in range(res - 2, res + 3)]
        lst = [i for i in lst if (minimum <= i <= maximum)]
        return lst

# Class methods
    def age(self) -> int:
        """Returns the age in ticks of this cell or the age at the time of death if the cell is dead."""
        return self._age

    def divisions(self) -> int:
        """Returns number of division performed by this cell."""
        return self._divisions

    def generation(self) -> int:
        """Returns the generation of this cell (generations are counted starting from 0)."""
        return self._generation

    def is_alive(self) -> bool:
        """Returns whether this cell is alive."""
        return self._alive

    def died_by_poisoning(self) -> bool:
        """Checks if this cell died because of the toxicity in its patch."""
        return self._died_by_poisoning

    def died_by_age_limit(self) -> bool:
        """Checks if this cell died because it exceeded the age limit."""
        return self._died_by_age_limit

    def died_by_division_limit(self) -> bool:
        """Checks if this cell died because it exceeded the division limit."""
        return self._died_by_division_limit

    def divide(self, patch) -> bool:
        """This cell attempts to divide using the given patch for the new cell.
        Returns True if the division is successful, False otherwise.

        Precondition: the cell is alive.

        pass resistance onto child from parent

        # The new cell should have the parent as the cell that divided
            new_cell.parent = old_cell
        """
        assert self.is_alive()  # "the cell must be alive."
        assert not patch.has_cell()  # "patch has to be free"
        p = Cell.division_probability - self._resistance / 20
        divides = r.choices([1, 0], weights=[p, 1-p], k=1)
        # 1 is divides with probability of p
        # 0 is does not divide with probability 1-p
        if divides[0]:  # if divides[0] == 1, then division happens
            # parent_resistance = 7
            # randomly select equally probable from [5,6,7,8,9]
            # parent_resistance = 0
            # uniformly random from [0,1,2] or [0,0,0,1,2]
            res = r.choice(Cell.resistance_inheritance(self._resistance))
            new_cell = Cell(patch, resistance=res, generation=self._generation + 1, parent=self)
            patch._cell = new_cell
            patch._has_cell = True
            self._last_division = 0  # reset the counter from the last division
            self._divisions = self._divisions + 1  # updates the division count
            return True
        return False

    def parent(self):
        """Returns the parent of this cell, None this cell belongs to the initial generation."""
        return self._parent

    def patch(self):
        """Returns the patch of this cell. If the cell is dead, it returns the patch where the cell died."""
        return self._patch

    def resistance(self) -> int:
        """Returns the resistance level of this cell."""
        return self._resistance

    def tick(self) -> None:
        """Register with this cell that a tick in the simulation happened making the cell age and die
        (age or division limit, or poisoning).

        Precondition: the cell is alive.

        # DOES NOT remove dead cells
        """
        assert self.is_alive(), "the cell must be alive."
        self._age += 1
        self._last_division += 1
        if self._age >= Cell.age_limit:
            # print("death by age limit")
            self._alive = False
            self._died_by_age_limit = True
        if self._divisions >= Cell.division_limit:
            # print("death by division")
            self._alive = False
            self._died_by_division_limit = True
        patch_toxicity = self.patch().toxicity()
        p = (patch_toxicity - self._resistance) / 10
        p = max(p, 0)  # if p < 0, probability will go to 0
        dies = r.choices([1, 0], weights=[p, 1-p], k=1)
        # 1 is dying with probability p
        # 0 is not dying with probability 1-p
        if dies[0] == 1:
            # print("death by poisoning")
            self._alive = False
            self._died_by_poisoning = True


if __name__ == '__main__':
    pass
