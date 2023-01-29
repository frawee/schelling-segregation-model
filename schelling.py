import os
import random
import math
import platform
import matplotlib.pyplot as plt
from typing import Tuple, List
from colors import Colors


def clear_output():
    """
    Clear the former output to not spam the console
    """
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class SchellingModel:
    def __init__(
        self,
        grid_size: Tuple[int, int],
        n_agents: int,
        share_a: float,
        stay_threshold: float,
    ):
        """
        calculates a schelling segregation simulation show the emergence of segregation
        even in the absence of strict preferences for a segregated society.
        For more info, see https://en.wikipedia.org/wiki/Schelling%27s_model_of_segregation
        For this purpose, agents of type A and B are randomly placed in a
        grid of the size x_size * y_size. In each step, one agent evaluates his neighbors
        and moves if the fraction of equal neighbors is less than T.
        :param grid_size: The width and height of the grid
        :param n_agents: number of total agents (A and B)
        :param share_a: share of type a agents
        :param stay_threshold: fraction of equal neighbors to not move
        :return: the schelling grid
        """

        self.x_size = int(grid_size[0])
        self.y_size = int(grid_size[1])
        self.n_agents = int(n_agents)
        self.share_a = float(share_a)
        self.stay_threshold = float(stay_threshold)

        # the grid in which agents are located (will be initialized later)
        self.grid = None
        # the share of agents with more than stay_threshold * 100 percent neighbors of the same letter
        self.segregation_shares = []
        # how often a random agent decided whether to move or not
        self.steps_run = 0

        # check whether inputs were valid
        self.__check_inputs()
        # initialize the grid and fill with agents
        self.__initialize_grid()

    def __check_inputs(self):
        """
        Ensure there are valid inputs for the Schelling model only
        """
        # grid is at least 2 by 2
        assert (
            self.x_size > 1 and self.y_size > 1
        ), "Both x size and y size must be integers larger than 1."
        # There have to be more cells than agents
        assert (
            self.x_size * self.y_size > self.n_agents
        ), "There are too many agents for the chosen grid size!"
        # there is more than one agent
        assert self.n_agents > 1, "There are not enough agents, choose at least two."
        # the share of agents of letter A is a valid share
        assert (
            0.0 <= self.share_a <= 1.0
        ), "The share of agents of type A must be between zero and one"
        # the neighbor share threshold for staying is a valid share
        assert (
            0.0 <= self.stay_threshold <= 1.0
        ), "The stay threshold must be between zero and one"

    def __initialize_grid(self):
        """
        Create a grid of the size given in init and
        randomly fill it with agents of type a and b
        """

        # initialize two-dimensional grid
        self.grid = [self.y_size * [None] for x in range(self.x_size)]

        # randomly place 50% A-agents and 50% B-agents in grid
        for i in range(math.floor(self.n_agents / 2)):
            new_pos = self.__find_empty_cell()
            self.grid[new_pos[0]][new_pos[1]] = "A"
        for j in range(math.ceil(self.n_agents)):
            new_pos = self.__find_empty_cell()
            self.grid[new_pos[0]][new_pos[1]] = "B"

    def run(self, steps: int = 1000, print_at_end: bool = True, print_every: int = 0):
        """
        Model the Schelling segregation process for a given number of steps.
        :param steps: How many agents consecutively decide whether to move or not
        :param print_at_end: Whether to print the final state of the grid
        :param: print_every: after how many steps to print the update.
            To not print an update, set to -1 or larger than steps
        """

        for step in range(steps):
            # let one agent decide whether to move or not and update the grid
            self.__run_one_step()
            # update step counter
            self.steps_run += 1
            # track current state of separation
            self.segregation_shares.append(self.get_segregation())

            # check whether it is time to print an update and do so
            if self.steps_run % print_every == 0:
                clear_output()
                self.print_schelling()

        # check whether to print the final state and do so
        if print_at_end:
            clear_output()
            self.print_schelling()

    def __run_one_step(self):
        """
        Run one step of the Schelling segregation model,
        i.e., choose one agent and have it move if
        its neighbor share is below the stay threshold
        """
        # randomly select an agent
        chosen_agent = self.__find_full_cell()
        # calculate share of equal neighbors
        equals = self.__get_neighbor_relation(chosen_agent)

        # move to random new position if share is smaller than threshold.
        if equals < self.stay_threshold:
            new_pos = self.__find_empty_cell()
            self.grid[new_pos[0]][new_pos[1]] = self.grid[chosen_agent[0]][
                chosen_agent[1]
            ]
            self.grid[chosen_agent[0]][chosen_agent[1]] = None

    def __find_empty_cell(self) -> Tuple[int, int]:
        """
        finds an empty cell in the schelling grid and returns its location.
        :return: a tuple of x and y location of the cell
        """

        # randomly pick position
        new_x_pos = random.randint(0, len(self.grid) - 1)
        new_y_pos = random.randint(0, len(self.grid[0]) - 1)

        # if cell is occupied, retry until it is not
        while self.grid[new_x_pos][new_y_pos]:
            new_x_pos = random.randint(0, len(self.grid) - 1)
            new_y_pos = random.randint(0, len(self.grid[0]) - 1)

        # return position of empty cell
        return new_x_pos, new_y_pos

    def __find_full_cell(self) -> Tuple[int, int]:
        """
        finds a full cell in the schelling grid and returns its location.
        :return: a tuple of x and y location of the cell
        """

        # randomly pick position
        full_cell = False

        # if cell is empty, retry until it is not
        while not full_cell:
            new_x_pos = random.randint(0, self.x_size - 1)
            new_y_pos = random.randint(0, self.y_size - 1)
            if self.grid[new_x_pos][new_y_pos]:
                full_cell = True

        # return position of occupied cell
        return new_x_pos, new_y_pos

    def __get_neighbor_relation(self, position) -> float:
        """
        calculates the share of equal direct neighbors of an agent in the
        schelling grid at a given position
        :param position: a tuple of x and y location of the agent
        :return: the share of neighbors of the same letter
        """
        a_count, b_count = self.__count_neighbors(position=position)

        # return the share of equal neighbors given the value of the agent
        if self.grid[position[0]][position[1]] == "A":
            if b_count == 0:
                neighbor_relation = 1
            else:
                neighbor_relation = a_count / b_count
        elif self.grid[position[0]][position[1]] == "B":
            if a_count == 0:
                neighbor_relation = 1
            else:
                neighbor_relation = b_count / a_count
        # no neighbors: stay
        else:
            return 1.0

        return neighbor_relation

    def __get_neighbor_positions(
        self, position: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """
        Get a list of all neighbor tuple locations
        to avoid index errors or empty cells
        :param position: the location of the agent whose neighbors are wanted
        :return: a list with all neighbor tuple locations
        """
        # start a list of neighbors
        neighbors = []

        # check all positions in the three by three grid surrounding the given position
        # whether they exist and exclude the original position as well
        for i in range(-1, 2):
            x = position[0] + i
            for j in range(-1, 2):
                y = position[1] + j
                if 0 <= x < self.x_size and 0 <= y < self.y_size and (x, y) != position:
                    neighbors.append((x, y))

        return neighbors

    def __count_neighbors(self, position: Tuple[int, int]) -> Tuple[int, int]:
        """
        Count the occurrence of As and Bs in an agents direct neighborhood
        :param position: the location of the agent whose neighbors are wanted
        :return: a tuple with the count of each A and B neighbors
        """
        # calculate the neighbor boundaries to correctly capture agents at the border

        # initialize counters
        a_count = 0
        b_count = 0

        # find the location of all neighbors
        neighbors = self.__get_neighbor_positions(position=position)

        # iterate over all neighbors and count As and Bs
        for x, y in neighbors:
            if self.grid[x][y] == "A":
                a_count += 1
            elif self.grid[x][y] == "B":
                b_count += 1

        return a_count, b_count

    def print_schelling(self):
        """
        Print the current state of the grid.
        Agents will be highlighted in different colors and
        the grid will be visualized in a checkboard pattern
        """
        # get the colors and bold font for each agent type and empty cells
        print_values = {
            "A": f"{Colors.bold}{Colors.fg.green} A {Colors.reset}",
            "B": f"{Colors.bold}{Colors.fg.blue} B {Colors.reset}",
            None: f"   {Colors.reset}",
        }

        # replace each grid value with a colored print version
        print_grid = [
            [f"{print_values[cell_value]}" for cell_value in row] for row in self.grid
        ]
        # add light grey as every second background colors to help visualize grid
        print_grid = [
            [
                f"{Colors.bg.lightgrey}{cell}"
                if ((i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1))
                else cell
                for j, cell in enumerate(row)
            ]
            for i, row in enumerate(print_grid)
        ]

        # create one printable string
        print_grid = "\n".join(["".join(row) for row in print_grid])

        # actually print grid
        print(print_grid)

    def get_segregation(self) -> float:
        """
        get the share of agents who are happy because they have
        at least stay_threshold * 100 percent of equal letters as neighbors
        :return: fraction of happy agents
        """

        # staying means the agent has >= stay_threshold equal-letter neighbors
        staying = 0
        # check for each agent and skip empty cells
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] is not None:
                    # return the share of same letters in neighborhood
                    neighbor_relation = self.__get_neighbor_relation(position=(i, j))
                    # compare to threshold and
                    if neighbor_relation >= self.stay_threshold:
                        staying += 1

        return staying / self.n_agents

    def plot_segregation_curve(self):
        """
        Plots the fraction on agents with at least
        stay_threshold * 100 percent equal letters as neighbors
        over the number of steps the Schelling model was run
        """

        # plot the steps run and the segregation shares and add lables and title
        plt.plot(list(range(self.steps_run)), self.segregation_shares)
        plt.xlabel("# steps run")
        plt.ylabel("homogeneity")
        plt.title("Schelling segregation model time series")
        plt.show()


if __name__ == "__main__":

    # initialize a schelling model
    schelling_model = SchellingModel(
        grid_size=(15, 15), n_agents=100, share_a=0.5, stay_threshold=0.5
    )

    # run and neatly print the result
    schelling_model.run(steps=2000, print_at_end=True, print_every=100)

    # plot the segregation over time
    schelling_model.plot_segregation_curve()
