from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib import gridspec


class LayoutCanvas(FigureCanvas):
    def __init__(self, parent=None, width=11.7, height=8.3, dpi=100):
        self._figure = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self._axes = []
        """ :type: list[Axes] """

        FigureCanvas.__init__(self, self._figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def set_plot_layout(self, layout_spec):
        grid_spec = gridspec.GridSpec(*layout_spec['dims'])

        for axes in self._axes:
            self._figure.delaxes(axes)

        self._axes = [self._figure.add_subplot(grid_spec[sub_spec]) for sub_spec in layout_spec['grid']]

        for axes in self._axes:
            axes.hold(False)

        self.draw()

    def index(self, axes):
        """
        Args:
            axes (Axes): The Axes instance to find the index of.

        Returns:
            int
        """
        return self._axes.index(axes)

    def __getitem__(self, index):
        """
        Args:
            index (int):

        Returns:
            Axes
        """
        return self._axes[index]

    def __len__(self):
        return len(self._axes)

    def __iter__(self):
        for x in range(len(self)):
            yield self[x]
