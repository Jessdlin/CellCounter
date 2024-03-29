from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import numpy as np


class DrawingImage(pg.ImageItem):
    colors = {'r': 0, 'g': 1, 'b': 2}

    def __init__(self, c, image=None, **kargs):
        pg.ImageItem.__init__(self, image, **kargs)
        self.c = c
        self.setKernel(5)
        self.x = None
        self.y = None

    def setKernel(self, size):
        self.centerValue = int((size - 1) / 2)
        self.kern = np.zeros((size, size, 3), dtype=np.uint8)
        self.mask = np.zeros((size, size, 3), dtype=np.uint8)
        y, x = np.mgrid[-self.centerValue:size - self.centerValue, -self.centerValue:size - self.centerValue]
        self.mask[:, :, :] = (x * x + y * y <= (size - 1) / 2 * (size - 1) / 2)[:, :, None]
        self.kern[:, :, DrawingImage.colors[self.c]] = 255

    def mouseClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDrawKernel(self.kern, self.mask, center=(self.centerValue, self.centerValue))
            self.drawAt(event.pos(), event)
        if event.button() == Qt.RightButton:
            self.setDrawKernel(self.kern * 0, self.mask, center=(self.centerValue, self.centerValue))
            self.drawAt(event.pos(), event)

    def mouseDragEvent(self, event):
        if event.isStart():
            if event.button() == Qt.LeftButton:
                self.setDrawKernel(self.kern, self.mask, center=(self.centerValue, self.centerValue))
            if event.button() == Qt.RightButton:
                self.setDrawKernel(self.kern * 0, self.mask, center=(self.centerValue, self.centerValue))
        if event.button() in [Qt.LeftButton, Qt.RightButton]:

            pos = event.pos()
            x, y = int(np.round(pos.x())), int(np.round(pos.y()))
            self.drawAt(event.pos(), event)
            if self.x is None or self.y is None:
                self.x = x
                self.y = y
                return
            sx, sy = np.sign(x - self.x), np.sign(y - self.y)

            if sx == 0:
                self.x = x
                self.y = y
                if event.isFinish():
                    self.x = None
                    self.y = None
                return

            if sy == 0:
                self.x = x
                self.y = y
                if event.isFinish():
                    self.x = None
                    self.y = None
                return

            X, Y = np.meshgrid(np.arange(1, abs(x - self.x)) * sx, np.arange(1, abs(y - self.y)) * sy)
            slope = (y - self.y) / (x - self.x)
            if sx == 1 and sy == 1:
                gte = slope >= (2 * Y - 1) / (2 * X + 1)
                lte = slope <= (2 * Y + 1) / (2 * X - 1)
            elif sx == 1 and sy == -1:
                lte = slope <= (2 * Y + 1) / (2 * X + 1)
                gte = slope >= (2 * Y - 1) / (2 * X - 1)
            elif sx == -1 and sy == -1:
                lte = slope <= (2 * Y - 1) / (2 * X + 1)
                gte = slope >= (2 * Y + 1) / (2 * X - 1)
            elif sx == -1 and sy == 1:
                lte = slope <= (2 * Y - 1) / (2 * X - 1)
                gte = slope >= (2 * Y + 1) / (2 * X + 1)

            result = lte * gte
            pixels = np.where(result.T)

            xs = sx * pixels[0] + self.x
            ys = sy * pixels[1] + self.y
            for x1, y1 in zip(xs, ys):
                p = QPoint(x1, y1)
                self.drawAt(p)

            self.x = x
            self.y = y

            if event.isFinish():
                self.x = None
                self.y = None

    def hoverEvent(self, event):
        if not event.isExit():
            # the mouse is hovering over the image; make sure no other items
            # will receive left click/drag events from here.
            event.acceptDrags(Qt.LeftButton)
            event.acceptClicks(Qt.LeftButton)
            event.acceptDrags(Qt.RightButton)
            event.acceptClicks(Qt.RightButton)


class HoverImage(pg.ImageItem):

    def __init__(self, img_dim, image=None, **kargs):
        pg.ImageItem.__init__(self, image, **kargs)
        self.setKernel(5, img_dim)

    def setKernel(self, size, img_dim):
        self.img_dim = img_dim
        if self.img_dim == 3:
            self.centerValue = int((size - 1) / 2)
            self.kern = np.zeros((size, size, 3), dtype=np.uint8) * 255
            mask = np.zeros((size, size, 3), dtype=np.uint8)
            y, x = np.mgrid[-self.centerValue:size - self.centerValue, -self.centerValue:size - self.centerValue]
            mask[:, :, :] = (x * x + y * y <= (size - 1) / 2 * (size - 1) / 2)[:, :, None]
            # self.kern[mask] = 255
            self.kern[:, :, :] = 255
            self.setDrawKernel(self.kern, mask, center=(self.centerValue, self.centerValue))
        elif self.img_dim == 2:
            self.centerValue = int((size - 1) / 2)
            self.kern = np.zeros((size, size), dtype=np.uint8) * 255
            y, x = np.mgrid[-self.centerValue:size - self.centerValue, -self.centerValue:size - self.centerValue]
            mask = x * x + y * y <= (size - 1) / 2 * (size - 1) / 2
            self.kern[mask] = 255
            self.setDrawKernel(self.kern, center=(self.centerValue, self.centerValue))

    def hoverEvent(self, event):
        if self.img_dim == 3:
            if not event.isExit():
                self.image[:, :, :] = 0
                self.updateImage()
                self.drawAt(event.pos(), event)
            else:
                self.image[:, :, :] = 0
                self.updateImage()
        elif self.img_dim == 2:
            if not event.isExit():
                self.image[:, :] = 0
                self.updateImage()
                self.drawAt(event.pos(), event)
            else:
                self.image[:, :] = 0
                self.updateImage()