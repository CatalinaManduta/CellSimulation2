# CellSimulation2
The goal of this program is to implement a cell simulation and observe how the population develops over time. The simulation's focus is to determine how environmental selective pressures such as space constraints, division limits, age limits, reproduction probabilities, and cooldown periods affect the cell population.
Project Title: Cellular Life Simulation
Description
This project simulates the life cycle of cells within a grid-based ecosystem. It sets up a grid, populates it with cells, and manages the life processes of the cells, including growth, reproduction, and death. The project tracks and reports the population statistics over time and provides visual outputs.

File Structure
cell_sim.py: Manages all the configurations for the cell population and the grid, helping the user navigate through various commands.
simulation.py: Orchestrates the simulation process including the initialization of the cell population, handling cell life cycle events (like ticking, reproduction/dividing, death), and visualization of the simulation. This module also compiles and displays statistics related to the simulation.
data.py: Manages all the data within the simulation, including the state of cells and statistics.
model.py: Contains the logic for the cell and patch models used in the simulation.
visualiser.py: Handles the visualization of the simulation's grid - Please note that the visualisation module used in this project is not included in this repository. This module was developed by our instructor and it is not publicly available. Therefore, you may encounter errors related to missing visualisation if you try to run the code as it is. You will need to supply your own visualisation functionality. 

Usage
Grid and Population Initialization: The read_grid, create_patches, and initialise_population functions help in creating a grid environment and initializing a population of cells with random resistances.
Simulation of Cell Life Cycle: The functions life, get_neighbours, and cleanup_dead are responsible for simulating a cell's life cycle, from its inception to potential death due to various reasons such as age limit, division limit, or poisoning.
Running the Simulation: The run_simulation function orchestrates the entire simulation process. It initializes the grid and population, runs the cell life cycle, visualizes the simulation (via the visualiser module), and continually checks for remaining cells. The simulation stops either when all cells are dead or when a time limit is reached.
Reporting and Visualization: The print_statistics and graph functions generate a report of the simulation statistics and visualise the data. The reported statistics include the total number of cells created, the largest generation, and causes of cell deaths. The graphical representation displays the resistance and population variations across generations.

Features
Dynamic Grid Creation: The code can read a layout from a text file and create a grid with obstacles and cell patches. This allows for customizable environments for the cells to interact in.
Cell Life Cycle Simulation: The code simulates the entire life cycle of a cell. This includes initial placement, growth and replication, death due to age, division limit, or toxicity.
Randomized Events: Elements of randomness are incorporated at various points in the code such as in initial population placement and cell division. This introduces variability in each run of the simulation.
Extensive Data Collection: The code records a wide variety of data during the simulation. This includes cell deaths (with specific causes), cell generation statistics, and resistance values of each cell.
Data Visualization: The code provides a detailed analysis of the simulation via statistics printed to the console and graphical displays. It presents generation-wise resistance (average, max, min) and population data.
Modular Design: The code is divided into distinct modules each serving a unique purpose - data handling, cell and patch modeling, visualization, and the main simulation. This makes the code easier to understand, maintain and extend.
Scalability: The grid size, initial population, and other parameters are easily adjustable, making the code flexible and scalable.

Authors
Catalina Manduta and Justin Di Giorgio.





