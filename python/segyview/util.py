import os

img_prefix = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resources", "img"))


def resource_icon(name):
    """Load an image as an icon"""
    # print("Icon used: %s" % name)
    from PyQt4.QtGui import QIcon
    return QIcon(os.path.join(img_prefix, name))
