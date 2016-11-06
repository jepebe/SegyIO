set(PYTHON_SOURCES
    __init__.py
    linenavigationbar.py
    progresswidget.py
    segyiowrapper.py
    segyplot.py
    slicewidget.py
    viewer.py
    layoutcombo.py
    layoutcanvas.py
    colormapcombo.py
    util.py
    )

add_python_package(segyview segyview "${PYTHON_SOURCES}")
