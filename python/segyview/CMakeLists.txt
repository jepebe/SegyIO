set(PYTHON_SOURCES
    __init__.py
    controlwidgets.py
    progresswidget.py
    segyiowrapper.py
    segyplot.py
    slicewidget.py
    viewer.py
    layoutcombo.py
    colormapcombo.py
    layoutfigure.py
    slicemodel.py
    slicedatasource.py
    slicemodelcontroller.py
    sliceview.py
    sliceviewwidget.py
    )

add_python_package(segyview segyview "${PYTHON_SOURCES}")
