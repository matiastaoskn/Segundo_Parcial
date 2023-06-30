import pygame
import sys
import time
from settings import *
from pygame.locals import *
from class_personaje import *
from modo import *
from animaciones import *


# Funciones
def actualizar_pantalla(pantalla, un_personaje: Personaje, lista_enemigos, fondo, lados_piso, corazones: Corazones):
    # Fondo
    pantalla.blit(fondo, (0, 0))
    # Plataformas
    for plataforma in lista_plataformas:
        PANTALLA.blit(plataforma.image, plataforma.rect)
    # Personaje
    for enemigo in lista_enemigos:
        un_personaje.update(pantalla, lados_piso, lista_plataformas, enemigo)
    
    #enemigo
    #MI PERSONAJE ACA-->
    for enemigo in lista_enemigos:
        enemigo.updateEnemigo(pantalla, lados_piso, lista_plataformas, mi_personaje)
        corazones_restantes = enemigo.vida_personaje
    #corazones
    PANTALLA.blit(corazones.image, (W-200,0))
    if corazones_restantes == 3:
        corazones.cargar_imagen(corazones_3)
    elif corazones_restantes == 2:
        corazones.cargar_imagen(corazones_2)
    elif corazones_restantes == 1:
        corazones.cargar_imagen(corazones_1)
    else:
        corazones.cargar_imagen(corazones_0)


W, H = 1300, 700
TAMAÑO_PANTALLA = (W, H)
FPS = 18
velocidad_personaje = 10
velocidad_enemigo = 8




pygame.init()

RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode(TAMAÑO_PANTALLA)

# Cronometro
tiempo_inicial = 25
tiempo_restante = tiempo_inicial
fuente = pygame.font.SysFont(None, 138)
color_texto = ("black")
pos_texto = (W // 2, H - 550)

# FONDO
fondo = pygame.image.load("Recursos/fondo_space.png")
fondo = pygame.transform.scale(fondo, TAMAÑO_PANTALLA)

# Personaje
posicion_inicial = (H / 2 - 300, 350)
tamaño = (110, 120)

#Enemigos
posicion_inicial_enemigo_1 = (H / 2 + 600, 480)
posicion_inicial_enemigo_2 = (H / 2 - 600, 200)
tamaño_enemigo = (100, 110)



# Crear personaje
mi_personaje = Personaje(tamaño, diccionario_animaciones_personaje, posicion_inicial, velocidad_personaje)

# Crear enemigo
enemigo1 = Enemigos(tamaño_enemigo, animaciones_enemigo, posicion_inicial_enemigo_1, velocidad_enemigo)
enemigo2 = Enemigos(tamaño_enemigo, animaciones_enemigo, posicion_inicial_enemigo_2, velocidad_enemigo)

lista_enemigos = []
lista_enemigos.append(enemigo1)
lista_enemigos.append(enemigo2)

mi_enemigos = None
for enemigo in lista_enemigos:
    mi_enemigos = enemigo

# Piso
piso = pygame.Rect(0, 60, W, 20)
piso.top = H - 99

Plataforma
lista_plataformas = []


def crear_plataforma(x, y, width, height):
    plataforma = Plataforma(x, y, width, height)
    lista_plataformas.append(plataforma)

#Corazones
corazones = Corazones(2, w=200, h=60)



plataformas = [
    crear_plataforma(x=890, y=H - 150, width=500, height=80),
    crear_plataforma(x=500, y=H - 260, width=300, height=80),
    crear_plataforma(x=-30, y=H - 340, width=400, height=80)
]


#Colision Piso
lados_piso = obtener_rectangulos(piso)
print(piso)



# RECTANGULO-PERSONAJE
x_inicial = H / 2 - 400
y_inicial = 750


for lado in mi_personaje.lados:
    rectangulo = mi_personaje.lados[lado]

while tiempo_restante > 0:
    RELOJ.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
            cambiar_modo()

    keys = pygame.key.get_pressed()

    #Detectar Movimiento
    if (keys[pygame.K_RIGHT] and  rectangulo.right < W - velocidad_personaje):
        mi_personaje.que_hace = "derecha"
                
    elif (keys[pygame.K_LEFT] and rectangulo.left > velocidad_personaje):
        mi_personaje.que_hace = "izquierda"
        if(keys[pygame.K_SPACE]):
            mi_personaje.que_hace = "dispara"
    elif keys[pygame.K_UP]:
        if not mi_personaje.esta_saltando:
            mi_personaje.que_hace = "salta"
    elif keys[pygame.K_SPACE]:
        mi_personaje.que_hace = "dispara"
        for enemigo in lista_enemigos:
            mi_personaje.golpear_enemigo(enemigo, PANTALLA)
    else:
        mi_personaje.que_hace = "quieto"

    
    mi_personaje.colision_detectada = False

    #Cronometro
    tiempo_restante -= RELOJ.get_time() / 1000  # Restar el tiempo transcurrido en cada iteración
    
    
    
    actualizar_pantalla(PANTALLA, mi_personaje, lista_enemigos,fondo, lados_piso, corazones)

    if get_modo():
        for enemigo in lista_enemigos:
            for lado in enemigo.lados:
                pygame.draw.rect(PANTALLA, "Blue", mi_enemigos.lados[lado], 2)

        for plataforma in lista_plataformas:
            pygame.draw.rect(PANTALLA, (255, 0, 0), plataforma.rect, width=3)

        for lado in lados_piso:
            pygame.draw.rect(PANTALLA, "Blue", lados_piso[lado], 2)

        for lado in mi_personaje.lados:
            pygame.draw.rect(PANTALLA, "Orange", mi_personaje.lados[lado], 3)

    texto = fuente.render(str(int(tiempo_restante)), True, color_texto) 
    texto_rect = texto.get_rect(center=pos_texto)
    PANTALLA.blit(texto, texto_rect)

    pygame.display.update()

print("¡Tiempo agotado!")