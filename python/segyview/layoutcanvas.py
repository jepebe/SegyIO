from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, Qt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from segyview import LayoutFigure


class LayoutCanvas(FigureCanvas):
    layout_changed = pyqtSignal()
    subplot_clicked = pyqtSignal(dict)

    def __init__(self, width=11.7, height=8.3, dpi=100, parent=None):
        self._figure = LayoutFigure(width, height, dpi)

        FigureCanvas.__init__(self, self._figure)
        self.setParent(parent)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()
        self.setFocusPolicy(Qt.ClickFocus)
        self.setFocus()

        self.mpl_connect('button_press_event', self._mouse_clicked)

    def _mouse_clicked(self, event):
        if event.inaxes is not None:
            data = {
                "x": event.xdata,
                "y": event.ydata,
                "mx": event.x,
                "my": event.y,
                "button": event.button,
                "key": event.key,
                "subplot_index": self._figure.index(event.inaxes)
            }
            self.subplot_clicked.emit(data)

    def set_plot_layout(self, layout_spec):
        self._figure.set_plot_layout(layout_spec)
        self.layout_changed.emit()
        self.draw()

    def layout_figure(self):
        """ :rtype: LayoutFigure """
        return self._figure
