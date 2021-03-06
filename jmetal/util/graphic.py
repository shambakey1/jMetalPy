import logging
from typing import TypeVar, List, Tuple

import matplotlib.pyplot as plt

from jmetal.core.solution import Solution

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S = TypeVar('S')

"""
.. module:: graphics
   :platform: Unix, Windows
   :synopsis: Class for plotting solutions.

.. moduleauthor:: Antonio Benítez <antonio.b@uma.es>
"""


class ScatterPlot():

    def __init__(self, plot_title: str, animation_speed: float = 1*10e-10):
        """ Creates a new :class:`ScatterPlot` instance.
        Args:
           plot_title (str): Title of the scatter diagram.
           animation_speed (float): Delay (for live plot only). Allow time for the gui event loops to trigger
           and update the display.
        """
        self.plot_title = plot_title
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(111)
        self.sc = None

        # Real-time plotting options
        self.animation_speed = animation_speed

    def __init_plot(self, is_auto_scalable: bool = True) -> None:
        """ Initialize the scatter plot the first time. """
        if is_auto_scalable:
            self.axis.set_autoscale_on(True)
            self.axis.autoscale_view(True, True, True)

        logger.info("Generating plot...")

        # Style options
        self.axis.grid(color='#f0f0f5', linestyle='-', linewidth=2, alpha=0.5)
        self.fig.suptitle(self.plot_title, fontsize=14, fontweight='bold')

    def __get_data_points(self, solution_list: List[S]) -> Tuple[list, list]:
        """ Get coords (x,y) from a solution_list. """

        if solution_list is None:
            raise Exception("Solution list is none!")

        points = list(solution.objectives for solution in solution_list)
        x_values, y_values = [point[0] for point in points], [point[1] for point in points]

        return x_values, y_values

    def retrieve_info(self, solution: Solution) -> None:
        """ Retrieve more information about a solution object. """
        pass

    def __search_solution(self, solution_list: List[S], x_val: float, y_val: float) -> None:
        """ Return a solution object associated with some values of (x,y). """

        sol = next((solution for solution in solution_list
                    if solution.objectives[0] == x_val and solution.objectives[1]), None)

        if sol is not None:
            logger.info('Solution associated to ({0}, {1}): {2}'.format(x_val, y_val, sol))
            self.retrieve_info(sol)
        else:
            raise Exception("Solution is none.")

    def __pick_handler(self, event, solution_list: List[S]):
        """ Handler for picking points from the plot. """
        line, ind = event.artist, event.ind[0]
        x, y = line.get_xdata(), line.get_ydata()

        logger.info('Selected data point ({0}): ({1}, {2})'.format(ind, x[ind], y[ind]))
        self.__search_solution(solution_list, x[ind], y[ind])

    def simple_plot(self, solution_list: List[S], file_name: str = "output",
                    fmt: str = 'eps', dpi: int = 200, save: bool = True) -> None:
        """ Create a simple plot. """
        self.__init_plot()
        x_values, y_values = self.__get_data_points(solution_list)

        self.sc, = self.axis.plot(x_values, y_values, 'go', markersize=5, picker=10)

        if save:
            supported_formats = ["eps", "jpeg", "jpg", "pdf", "pgf", "png", "ps",
                                 "raw", "rgba", "svg", "svgz", "tif", "tiff"]
            if fmt not in supported_formats:
                raise Exception(fmt + " is not a valid format! Use one of these instead: "
                                + str(supported_formats))

            self.fig.savefig(file_name + '.' + fmt, format=fmt, dpi=dpi)
            logger.info("Output file (function plot): " + file_name + '.' + fmt)

    def interactive_plot(self, solution_list: List[S]) -> None:
        """ Create a plot to get to directly access the coords (x,y) of a point by a mouse click. """

        self.__init_plot()
        x_values, y_values = self.__get_data_points(solution_list)

        self.sc, = self.axis.plot(x_values, y_values, 'go', markersize=5, picker=10)
        self.fig.canvas.mpl_connect('pick_event', lambda event: self.__pick_handler(event, solution_list))

        plt.show()

    def update(self, solution_list: List[S], evaluations: int = 0, computing_time: float = 0) -> None:
        """ Update a simple_plot(). Note that the plot must be initialized first. """

        if self.sc is None:
            raise Exception("Error while updating! Initialize plot first with "
                            "simple_plot(solution_list: List[S])")

        x_values, y_values = self.__get_data_points(solution_list)

        # Update points
        self.sc.set_data(x_values, y_values)
        event_handler = self.fig.canvas.mpl_connect('pick_event', lambda event: self.__pick_handler(event, solution_list))

        # Update title
        self.fig.suptitle(self.plot_title
                          + ', \n Eval: ' + str(evaluations)
                          + ', Time: ' + str('%.3f'%computing_time), fontsize=14, fontweight='bold')

        # Re-align the axis.
        self.axis.relim()
        self.axis.autoscale_view(True, True, True)

        # Draw
        self.fig.canvas.draw()
        plt.pause(self.animation_speed)

        # Disconnect the pick event for the next update
        self.fig.canvas.mpl_disconnect(event_handler)
