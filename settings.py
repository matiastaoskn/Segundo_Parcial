import pygame

def rescalarar_img(lista_imagenes, tamaño):
    for i in range(len(lista_imagenes)):
        lista_imagenes[i] = pygame.transform.scale(lista_imagenes[i], tamaño)

def girar_imagenes(lista_original, flip_x, flip_y):
    lista_girada = []

    for imagen in lista_original:
        lista_girada.append(pygame.transform.flip(imagen, flip_x, flip_y))

    return lista_girada

def obtener_rectangulos(principal)-> dict:
    diccionario = {}
    diccionario["main"] = principal
    diccionario["bottom"] = pygame.Rect(principal.left, principal.bottom - 6, principal.width, 6)
    diccionario["right"] = pygame.Rect(principal.right -2, principal.top, 2, principal.height)
    diccionario["left"] = pygame.Rect(principal.left, principal.top, 2, principal.height)
    diccionario["top"] = pygame.Rect(principal.left, principal.top, principal.width, 6)
    return diccionario
#Personaje
personaje_quieto = [pygame.image.load("Recursos\Quieto/0.png")]
personaje_camina_derecha = [
                    pygame.image.load("Recursos/Camina/Adelante/1.png"),
                    pygame.image.load("Recursos/Camina/Adelante/2.png"),
                    pygame.image.load("Recursos/Camina/Adelante/3.png"),
                    pygame.image.load("Recursos/Camina/Adelante/4.png"),
                    ]
personaje_camina_izquierda = girar_imagenes(personaje_camina_derecha, True, False)
personaje_salta_derecha = [pygame.image.load("Recursos\Salta_derecha/0.png"),
                           #pygame.image.load("Recursos\Salta_derecha/1.png")
                            ]
personaje_salta_izquierda = [pygame.image.load("Recursos\Salta_izquierda/0.png"),
                             #pygame.image.load("Recursos\Salta_izquierda/1.png")
                             ]
personaje_dispara = [pygame.image.load("Recursos/ataca/1.png"),
                     pygame.image.load("Recursos/ataca/2.png"),
                     pygame.image.load("Recursos/ataca/3.png"),
                     pygame.image.load("Recursos/ataca/4.png"),
                     pygame.image.load("Recursos/ataca/5.png"),
                     pygame.image.load("Recursos/ataca/6.png")]


#Enemigo
enemigo_camina_derecha =  [
                pygame.image.load("Recursos\Camina\Adelante\Enemigo1/1.png"),
                pygame.image.load("Recursos\Camina\Adelante\Enemigo1/2.png"),
                pygame.image.load("Recursos\Camina\Adelante\Enemigo1/3.png"),
                pygame.image.load("Recursos\Camina\Adelante\Enemigo1/4.png"),
                   
                pygame.image.load("Recursos\Camina\Adelante\Enemigo1/5.png")
                ]

enemigo_camina_izquierda = girar_imagenes(enemigo_camina_derecha, True, False)

enemigo_quieto = [pygame.image.load("Recursos\Quieto/0.png")]
enemigo_ataca = [pygame.image.load("Recursos\Ataca\Enemigos/1.png"),
                 pygame.image.load("Recursos\Ataca\Enemigos/2.png"),
                 pygame.image.load("Recursos\Ataca\Enemigos/3.png"),
                 pygame.image.load("Recursos\Ataca\Enemigos/4.png"),
                 pygame.image.load("Recursos\Ataca\Enemigos/5.png"),
                 pygame.image.load("Recursos\Ataca\Enemigos/6.png")]

enemigo_daño = [pygame.image.load("Recursos\Daño/0.png")]

corazones_0 = ("Recursos/Corazones/4.png")
corazones_3 = ("Recursos\Corazones\corazones.png")
corazones_2 = ("Recursos\Corazones/2.png")
corazones_1 = ("Recursos\Corazones/3.png")


