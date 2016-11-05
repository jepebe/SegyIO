from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QMenu, QAction

from segyview import SliceView, LayoutCanvas, SliceModel, SliceModelController, SliceDataSource


class SliceViewWidget(LayoutCanvas):
    def __init__(self, models, data_source, colormap='seismic', width=11.7, height=8.3, dpi=100, parent=None):
        super(SliceViewWidget, self).__init__(width, height, dpi, parent)

        self._available_slice_models = list(models)
        """ :type: list[SliceModel] """
        self._assigned_slice_models = list(models)
        """ :type: list[SliceModel] """
        self._slice_views = {}
        """ :type: dict[matplotlib.axes.Axes,SliceView] """

        self._slice_model_controller = SliceModelController(self._available_slice_models, data_source)

        self._colormap = colormap
        self._show_indicators = False

        self.layout_changed.connect(self._layout_changed)
        self.subplot_clicked.connect(self._subplot_clicked)

    def colormap(self, colormap):
        self._colormap = colormap
        self._context_changed()

    def show_indicators(self, visible):
        self._show_indicators = visible
        self._context_changed()

    def _create_context(self):
        return {
            "colormap": self._colormap,
            "show_indicators": self._show_indicators,
            "global_min": -1000,
            "global_max": 1000,
        }

    def _layout_changed(self):
        print("layout_changed")
        fig = self.layout_figure()
        axes = fig.layout_axes()
        self._slice_views.clear()

        for model in self._available_slice_models:
            model.visible = False

        for index, ax in enumerate(axes):
            ax.clear()
            if index < len(self._assigned_slice_models):
                model = self._assigned_slice_models[index]
                model.visible = True
                self._slice_views[ax] = SliceView(ax, model)
                self._slice_views[ax].create_slice(self._create_context())

        self._slice_model_controller.load_data()
        self._data_changed()

    def _data_changed(self):
        print("data_changed")
        context = self._create_context()
        for slice_view in self._slice_views.values():
            slice_view.data_changed(context)
        self._context_changed()

    def _context_changed(self):
        print("context_changed")
        for slice_view in self._slice_views.values():
            slice_view.context_changed(self._create_context())
        self.draw()

    def _create_slice_view_context_menu(self, subplot_index):
        context_menu = QMenu("Slice Model Reassignment Menu", self)

        def reassign(model):
            def fn():
                self._assigned_slice_models[subplot_index] = model
                self._layout_changed()
            return fn

        for model in self._available_slice_models:
            action = QAction(model.title, self)
            action.triggered.connect(reassign(model))
            context_menu.addAction(action)

        return context_menu

    def _subplot_clicked(self, event):
        if self._show_indicators and event['button'] == 1:
            subplot_index = event['subplot_index']
            x = int(event['x'])
            y = int(event['y'])
            fig = self.layout_figure()
            ax = fig.layout_axes()[subplot_index]
            slice_model = self._slice_views[ax].model()
            self._slice_model_controller.model_indexes_changed(slice_model, x, y)
            self._data_changed()

        elif event['button'] == 3:
            subplot_index = event['subplot_index']
            context_menu = self._create_slice_view_context_menu(subplot_index)
            context_menu.exec_(self.mapToGlobal(QPoint(event['mx'], self.height() - event['my'])))
