from PySide6.QtWidgets import (
    QWidget,QVBoxLayout, QPushButton, QFileDialog, QLabel
)
from PySide6.QtGui import QMouseEvent, QIcon
from PySide6.QtCore import QSize
import struct
import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

from apps.base.base import make_card

def load_stl(filename):
    with open(filename, 'rb') as f:
        header = f.read(80)
        if b"solid" in header[:5].lower():
            return load_ascii_stl(filename)
        return load_binary_stl(filename)


def load_binary_stl(filename):
    vertices = []
    with open(filename, 'rb') as f:
        f.seek(80)
        triangle_count = struct.unpack('<I', f.read(4))[0]
        for _ in range(triangle_count):
            f.read(12)
            for _ in range(3):
                vertices.append(struct.unpack('<fff', f.read(12)))
            f.read(2)
    return np.array(vertices, dtype=np.float32)


def load_ascii_stl(filename):
    vertices = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip().startswith("vertex"):
                parts = line.strip().split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(vertices, dtype=np.float32)


class GLWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.vertices = None
        self.rotation_x = 20
        self.rotation_y = 30
        self.zoom = -10
        self.last_pos = None
        self.translation = np.array([0.0, 0.0, 0.0])

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 2, 3, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        # Background: light mint matching Figma
        glClearColor(0.91, 0.97, 0.96, 1)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h else 1, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, self.zoom)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        glTranslatef(*self.translation)

        if self.vertices is not None:
            # Teal primary color matching Figma
            glColor3f(0.05, 0.58, 0.53)
            glBegin(GL_TRIANGLES)
            for i in range(0, len(self.vertices) - 2, 3):
                v0, v1, v2 = self.vertices[i], self.vertices[i+1], self.vertices[i+2]
                # compute normal for lighting
                edge1 = v1 - v0
                edge2 = v2 - v0
                normal = np.cross(edge1, edge2)
                length = np.linalg.norm(normal)
                if length > 0:
                    normal /= length
                glNormal3f(*normal)
                glVertex3f(*v0)
                glVertex3f(*v1)
                glVertex3f(*v2)
            glEnd()
        else:
            self._draw_placeholder()

    def _draw_placeholder(self):
        """Draw a simple teal cube as placeholder"""
        glColor3f(0.05, 0.58, 0.53)
        size = 1.5
        faces = [
            [(size,size,-size),(size,-size,-size),(-size,-size,-size),(-size,size,-size)],
            [(size,size,size),(-size,size,size),(-size,-size,size),(size,-size,size)],
            [(size,size,-size),(size,size,size),(size,-size,size),(size,-size,-size)],
            [(-size,size,-size),(-size,-size,-size),(-size,-size,size),(-size,size,size)],
            [(size,-size,-size),(size,-size,size),(-size,-size,size),(-size,-size,-size)],
            [(size,size,-size),(-size,size,-size),(-size,size,size),(size,size,size)],
        ]
        normals = [(0,0,-1),(0,0,1),(1,0,0),(-1,0,0),(0,-1,0),(0,1,0)]
        glBegin(GL_QUADS)
        for face, normal in zip(faces, normals):
            glNormal3f(*normal)
            for v in face:
                glVertex3f(*v)
        glEnd()

    def load_model(self, path):
        verts = load_stl(path)
        # Centre and normalise
        if len(verts):
            centre = verts.mean(axis=0)
            verts -= centre
            scale = np.abs(verts).max()
            if scale > 0:
                verts /= scale
                verts *= 4
        self.vertices = verts
        self.rotation_x, self.rotation_y = 20, 30
        self.zoom = -10
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        self.last_pos = event.position()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_pos:
            dx = event.position().x() - self.last_pos.x()
            dy = event.position().y() - self.last_pos.y()
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5
            self.last_pos = event.position()
            self.update()

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() / 240
        self.update()

class STLViewerTab(QWidget):
    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(0)

        # Title
        title = QLabel("3D STL Viewer")
        title.setObjectName("section_title")
        outer.addWidget(title)
        outer.addSpacing(4)
        sub = QLabel("Load an STL file — drag to rotate, scroll to zoom")
        sub.setObjectName("section_sub")
        outer.addWidget(sub)
        outer.addSpacing(16)

        # Viewport card
        viewport_card, vp_lay = make_card("v", (4, 4, 4, 4), 0)
        self.gl_widget = GLWidget()
        self.gl_widget.setMinimumHeight(380)
        vp_lay.addWidget(self.gl_widget)
        outer.addWidget(viewport_card, stretch=1)

        outer.addSpacing(16)

        # Bottom bar
        bottom, bot_lay = make_card("h", (14, 14, 14, 14), 12)
        hint = QLabel("Preview cube is shown by default. Load your own STL model")
        hint.setObjectName("hint")
        bot_lay.addWidget(hint)
        bot_lay.addStretch()

        btn_load = QPushButton("Load STL File")
        btn_load.setIcon(QIcon("icons/Add.svg"))
        btn_load.setIconSize(QSize(20, 20))
        btn_load.setObjectName("stl_load")
        btn_load.clicked.connect(self.load_stl)
        bot_lay.addWidget(btn_load)
        outer.addWidget(bottom)

    def load_stl(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open STL", "", "STL Files (*.stl)"
        )
        if file_path:
            self.gl_widget.load_model(file_path)
