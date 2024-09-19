import OpenGL.GLUT as glut
import OpenGL.GLU as glu

from controls import keyboardFunction, specialKeyboardFunction
from opengl import displayFunction, initGlut, resizeFunction


def main():
    print("Running...")
    initGlut(displayFunction, resizeFunction, keyboardFunction, specialKeyboardFunction)


if __name__ == "__main__":
    main()
