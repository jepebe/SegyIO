from matplotlib import patches
from matplotlib.ticker import FuncFormatter, AutoLocator
from matplotlib.image import AxesImage
from .slicemodel import SliceModel
import numpy as np


class SliceView(object):
    def __init__(self, axes, model, interpolation="nearest", aspect="auto"):
        super(SliceView, self).__init__()
        data = np.zeros((1, 1))
        self._image = axes.imshow(data, interpolation=interpolation, aspect=aspect, origin='upper')
        """ :type: AxesImage """
        self._model = model
        """ :type: SliceModel """

        style = {"fill": False,
                 "alpha": 1,
                 "color": 'black',
                 "linestyle": 'dotted',
                 "linewidth": 0.75
                 }

        self._vertical_indicator = patches.Rectangle((-0.5, -0.5), 1, model.height, **style)
        self._horizontal_indicator = patches.Rectangle((-0.5, -0.5), model.width, 1, **style)

    def model(self):
        """ :rtype: SliceModel """
        return self._model

    def create_slice(self, context):
        """ :type context: dict """
        model = self._model
        axes = self._image.axes
        """ :type: matplotlib.axes.Axes """

        axes.set_title(model.title, fontsize=13)
        axes.tick_params(axis='both')
        axes.set_ylabel(model.y_axis_name, fontsize=10)
        axes.set_xlabel(model.x_axis_name, fontsize=10)

        axes.get_xaxis().set_major_formatter(FuncFormatter(model.x_axis_formatter))
        axes.get_xaxis().set_major_locator(AutoLocator())

        axes.get_yaxis().set_major_formatter(FuncFormatter(model.y_axis_formatter))
        axes.get_yaxis().set_major_locator(AutoLocator())

        for label in (axes.get_xticklabels() + axes.get_yticklabels()):
            label.set_fontsize(10)

        axes.set_xlim(0, model.width)
        axes.set_ylim(model.height, 0)  # origin in image is upper...

        axes.add_patch(self._vertical_indicator)
        axes.add_patch(self._horizontal_indicator)
        self._update_indicators(context)

        self._image.set_cmap(cmap=context['colormap'])

        if model.data is not None:
            self._image.set_data(model.data)

    def data_changed(self, context):
        """ :type context: dict """
        model = self._model
        self._image.set_data(model.data)
        self._image.set_extent((0, model.width, model.height, 0))

    def context_changed(self, context):
        """ :type context: dict """
        self._image.set_cmap(context['colormap'])
        # self._image.set_clim(context['global_min'], context['global_max'])
        model = self.model()
        self._image.set_clim(model.min_value, model.max_value)
        self._update_indicators(context)

    def _update_indicators(self, context):
        """ :type context: dict """
        model = self._model
        self._vertical_indicator.set_height(model.height + 1)
        self._vertical_indicator.set_width(1)
        self._horizontal_indicator.set_width(model.width + 1)
        self._horizontal_indicator.set_height(1)

        show_indicators = context['show_indicators']

        self._vertical_indicator.set_visible(model.x_index is not None and show_indicators)
        self._horizontal_indicator.set_visible(model.y_index is not None and show_indicators)

        if model.x_index is not None and show_indicators:
            self._vertical_indicator.set_x(model.x_index)

        if model.y_index is not None and show_indicators:
            self._horizontal_indicator.set_y(model.y_index)

