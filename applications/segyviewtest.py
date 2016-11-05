#!/usr/bin/env python
import os
import sys

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMainWindow, QWidget, QApplication, QHBoxLayout, QToolBar, QComboBox, QCheckBox

import segyio
from segyview import *

import numpy as np

from segyview import SliceViewWidget
from segyview.slicemodel import SliceDirection as SD


class SegyViewer(QMainWindow):
    def __init__(self, s):
        QMainWindow.__init__(self)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("SegyViewer")

        inline = SliceModel("Inline", SD.inline, SD.crossline, SD.depth)
        xline = SliceModel("Crossline", SD.crossline, SD.inline, SD.depth)
        depth = SliceModel("Depth", SD.depth, SD.inline, SD.crossline)

        slice_models = [inline, xline, depth]
        slice_data_source = SliceDataSource(s)

        self._slice_view_widget = SliceViewWidget(slice_models, slice_data_source)

        toolbar = self.addToolBar("Stuff")
        """:type: QToolBar"""

        layout_combo = LayoutCombo()
        toolbar.addWidget(layout_combo)
        layout_combo.layout_changed.connect(self._slice_view_widget.set_plot_layout)

        self._colormap_combo = QComboBox()
        for cmap in ['seismic', 'spectral', 'RdGy', 'hot', 'jet', 'gray']:
            self._colormap_combo.addItem(cmap)

        self._colormap_combo.currentIndexChanged[int].connect(self._colormap_changed)

        toolbar.addWidget(self._colormap_combo)

        indicator_visibility = QCheckBox("Indicators")
        indicator_visibility.toggled.connect(self._slice_view_widget.show_indicators)
        toolbar.addWidget(indicator_visibility)

        indicator_visibility.setChecked(True)
        self._colormap_combo.setCurrentIndex(0)
        layout_combo.setCurrentIndex(2)

        self.setCentralWidget(self._slice_view_widget)

    def _colormap_changed(self, index):
        colormap = str(self._colormap_combo.itemText(index))
        self._slice_view_widget.colormap(colormap)


def run(filename):
    with segyio.open(filename, "r") as s:
        segy_viewer = SegyViewer(s)
        segy_viewer.show()
        segy_viewer.raise_()
        sys.exit(q_app.exec_())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: segyviewer.py [file]")

    filename = sys.argv[1]

    q_app = QApplication(sys.argv)

    # import cProfile
    # cProfile.run('run(%s)' % filename, filename=None, sort='cumulative')
    run(filename)
