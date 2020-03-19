
import sys
import time
import csv
from PySide2.QtCore import(Property, QObject, QPropertyAnimation, Signal, Qt, QTimer)
from PySide2.QtGui import (QGuiApplication, QMatrix4x4, QQuaternion, QVector3D, QColor, QTransform, QIcon, QKeySequence, QPainter)
from PySide2.Qt3DCore import (Qt3DCore)
from PySide2.Qt3DExtras import (Qt3DExtras)
from PySide2.QtWidgets import (QPushButton, QWidget)
from PySide2.QtSensors import (QRotationReading, QSensor)
from cuboid import (Cuboid)
from sphere import (Sphere)

class Window(Qt3DExtras.Qt3DWindow):

    def __init__(self):
        super().__init__()
        #store objects into array
        self.i = 0
        self.listOfObjects = []
        with open('local2.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.listOfObjects.append(row)
        print(self.listOfObjects)
        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        #setting focus on selected object
        if self.listOfObjects[0][0] == 's':
            self.camera().setPosition(QVector3D(int(row[7]), int(row[8]), 50+int(row[9])))
            self.camera().setViewCenter(QVector3D(int(row[7]), int(row[8]), int(row[9])))
        else:
            self.camera().setPosition(QVector3D(int(row[9]), int(row[10]), 50 + int(row[11])))
            self.camera().setViewCenter(QVector3D(int(row[9]), int(row[10]), int(row[11])))
        # For camera controls
        self.rootEntity = Qt3DCore.QEntity()

        self.showAll()
        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())
        self.setRootEntity(self.rootEntity)
        #self.addObject(["c","three",0,0,255,155,6,6,6,-10,-6,-8,0,0,0])
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.deleteObject("second"))
        # self.timer.start(1)
        # self.timer.singleShot(1000,0,self.longer(),'1')
        # self.timer.timeout.connect(self.longer())

    #object selector
    def follow(self):
        if QKeySequence(Qt.CTRL + Qt.SHIFT):
            self.i = 1 + self.i

    # shows all objects
    def showAll(self):

        self.rootEntity = Qt3DCore.QEntity()
        self.materialSquare = Qt3DExtras.QPhongMaterial(self.rootEntity)
        self.materialSphere = Qt3DExtras.QPhongMaterial(self.rootEntity)
        # self.material = Qt3DExtras.QPhongMaterial(self.rootEntity)
        with open('local2.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 's':

                    self.sphereEntity = Qt3DCore.QEntity(self.rootEntity)
                    self.sphereMesh = Qt3DExtras.QSphereMesh()
                    self.name = row[1]
                    self.materialSphere.setAmbient(QColor(int(row[2]), int(row[3]), int(row[4]), int(row[5])))
                    self.sphereMesh.setRadius(int(row[6]))
                    self.QTransformSphere = Qt3DCore.QTransform()
                    self.sphereEntity.addComponent(self.sphereMesh)
                    self.sphereEntity.addComponent(self.materialSphere)
                    self.sphereEntity.addComponent(self.QTransformSphere)
                    sphereVector3D = QVector3D()
                    sphereVector3D.setX(int(row[7]))
                    sphereVector3D.setY(int(row[8]))
                    sphereVector3D.setZ(int(row[9]))
                    self.QTransformSphere.setTranslation(sphereVector3D)

                else:

                    self.squareEntity = Qt3DCore.QEntity(self.rootEntity)
                    self.squareMesh = Qt3DExtras.QCuboidMesh()
                    self.name = row[1]
                    self.materialSquare.setAmbient(QColor(int(row[2]), int(row[3]), int(row[4]), int(row[5])))
                    self.squareMesh.setXExtent(int(row[6]))
                    self.squareMesh.setYExtent(int(row[7]))
                    self.squareMesh.setZExtent(int(row[8]))
                    self.QTransformSquare = Qt3DCore.QTransform()
                    self.squareEntity.addComponent(self.squareMesh)
                    self.squareEntity.addComponent(self.materialSquare)
                    self.squareEntity.addComponent(self.QTransformSquare)

                    squareVector3D = QVector3D()
                    squareVector3D.setX(int(row[9]))
                    squareVector3D.setY(int(row[10]))
                    squareVector3D.setZ(int(row[11]))
                    self.QTransformSquare.setTranslation(squareVector3D)
                    self.QTransformSquare.setRotationX(int(row[12]))
                    self.QTransformSquare.setRotationY(int(row[13]))
                    self.QTransformSquare.setRotationZ(int(row[14]))

    # delete node
    def deleteObject(self, name):
        with open('local2.csv', 'w+') as out:
            writer = csv.writer(out)
            # writer.writerow(2)
            for row in csv.reader(out):
                if row[1] == name:
                    print('delete row')
                    writer.writerow(row)

    #add node
    def addObject(self, myList = []):
        with open(r'local2.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(myList)

    #testing purpose
    def call(self):
        print("timer call")

    #menu
    def controls(self):
        if QKeySequence(Qt.CTRL + Qt.Key_A):
            self.showAll()
        elif QKeySequence(Qt.CTRL + Qt.Key_B):
            self.showOne()
        elif QKeySequence(Qt.CTRL + Qt.Key_C):
            self.changeAttributes()
    #testing purpose
    def longer(self):
        self.squareMesh.setXExtent(self.squareMesh.xExtent()+1)

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = Window()
    view.show()
    (app.exec_())

    while True:
        view.show()
        view.squareMesh.setXExtent(view.squareMesh.xExtent()+1)
        (app.exec_())


    # sys.exit(app.exec_())

