import OpenGL.GLUT as glut
import OpenGL.GLU as glu

from opengl import displayFunction, initGlut, resizeFunction



def main():
    print("Running...")
    initGlut(displayFunction, resizeFunction)


if __name__ == "__main__":
    main()
