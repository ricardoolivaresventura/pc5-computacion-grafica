import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
from pywavefront import Wavefront
from math import cos, sin, pi

def draw_text(x, y, text):
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glRasterPos2f(x, y)

    # Iteramos sobre cada carácter en el texto y dibújalo
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def draw_star():
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    
    # Ajusta los radios para una estrella más pequeña
    radius = 0.3  # Reducir el radio exterior
    inner_radius = 0.1  # Reducir el radio interior

    for i in range(5):
        # Punto exterior
        outer_x = radius * cos(72 * i * (pi / 180))
        outer_y = radius * sin(72 * i * (pi / 180))

        # Punto interior
        inner_x = inner_radius * cos((72 * i + 36) * (pi / 180))
        inner_y = inner_radius * sin((72 * i + 36) * (pi / 180))

        glVertex3f(outer_x, outer_y + 2.5, 0) 
        glVertex3f(inner_x, inner_y + 2.5, 0)
        glVertex3f(0, 2.5, 0)  # Centro de la estrella (punta del árbol)
    
    glEnd()

def draw_tree():
    glLineWidth(2)
    glColor3f(0.0, 1.0, 0.0) 
    glBegin(GL_TRIANGLES)
    glVertex3f(0, 2.5, 0)
    glVertex3f(-1.5, -1, 0)  # Modifica la coordenada Y para invertir la base
    glVertex3f(1.5, -1, 0)  # Modifica la coordenada Y para invertir la base
    glEnd()
    # Dibujar la estrella en la punta superior del árbol
    draw_star()

# Luces navideñas
def draw_light(x, y, z, r, g, b):
    glColor3f(r, g, b)
    glPushMatrix()
    glTranslatef(x, y, z)
    glutSolidSphere(0.1, 10, 10)
    glPopMatrix()

# Cubos o regalos
def draw_gift(x, y, z):
    glColor3f(1.0, 0.0, 0.0)  # Color rojo
    glPushMatrix()
    glTranslatef(x, y, z)
    glutSolidCube(0.2)
    glPopMatrix()

# Inicializamos OpenGL
def initialize(display):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.0, -5)

# Función principal
def main():
    pygame.init()
    display = (800, 600)
    pygame.mixer.init()
    screen = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    font = pygame.font.Font(None, 36) 

    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.set_volume(0.2) 
    pygame.mixer.music.play(-1)  

    initialize(display)
    glutInit(sys.argv)

    lights = []  # Posiciones de lasluces
    gifts = []   # Posiciones de los regalos

    # Generar posiciones aleatorias para las luces
    for _ in range(10):
        lights.append((random.uniform(-1, 1), random.uniform(0, 2), random.uniform(-1, 1)))

    # Generar posiciones aleatorias para los regalos
    for _ in range(5):
        gifts.append((random.uniform(-1.5, 1.5), -0.5, random.uniform(-1.5, 1.5)))
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 0, 1, 0)  # Rotación en el eje Y

        draw_tree()

        # Dibujar luces navideñas con caída libre
        for idx, light in enumerate(lights):
            draw_light(light[0], light[1], light[2], random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
            lights[idx] = (light[0], light[1] - 0.01, light[2])

            # Volver a posicionar la luz si ha caído
            if light[1] < 0:
                lights[idx] = (random.uniform(-1, 1), random.uniform(2, 4), random.uniform(-1, 1))

        # Dibujar y hacer girar los regalos alrededor del árbol
        for idx, gift in enumerate(gifts):
            glPushMatrix()
            glRotatef(1, 0, 1, 0)
            draw_gift(gift[0], gift[1], gift[2])
            glPopMatrix()

        draw_text(-0.25, 2, "Feliz Navidad y Próspero Año Nuevo 2024")
        draw_text(-0.25, 1.8,"les desea el Curso de Computación Gráfica")

        pygame.display.flip()
        pygame.time.wait(10)

main()