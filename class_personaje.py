import pygame
from settings import *
import random
import time


class Personaje:
    def __init__(self, tamaño, animaciones, posicion_inicial, velocidad):
        self.ancho = tamaño[0]
        self.alto = tamaño[1]

        self.vida_personaje = 3

        #Movimiento
        self.contador_pasos = 0
        self.accion = "quieto"
        self.animaciones = animaciones
        self.rescalar_animaciones()
        self.esta_saltando = False

        #Colision
        rectangulo = self.animaciones["camina_derecha"][0].get_rect()
        rectangulo.x = posicion_inicial[0]
        rectangulo.y = posicion_inicial[1]
        self.lados = obtener_rectangulos(rectangulo)
        
        #Salto
        self.desplazamiento_y = 0
        self.velocidad = velocidad
        self.que_hace = "quieto"
        self.esta_disparando = False
        self.puede_saltar = True
        self.direccion = ""

        self.gravedad = 1
        self.potencia_salto = -15
        self.limite_velocidad_caida = 15

        #Atacar
        self.colision_detectada = False
        self.timer = pygame.USEREVENT + 1
        
        

        pygame.time.set_timer(self.timer, 2000)
        self.ultimo_golpe = pygame.time.get_ticks()
    def rescalar_animaciones(self):
        for clave in self.animaciones:
            rescalarar_img(self.animaciones[clave], (self.ancho, self.alto))
    
    def animar(self, pantalla, que_animacion):
        animacion = self.animaciones[que_animacion]
        largo = len(animacion)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0

        pantalla.blit(animacion[self.contador_pasos], self.lados["main"])
        self.contador_pasos += 1

    def mover(self, velocidad):
        #Se mueve el personaje
        for lado in self.lados:
            self.lados[lado].x += velocidad
        
    def golpear_enemigo(self, enemigo, pantalla):
        tiempo_actual = pygame.time.get_ticks() 
        if tiempo_actual - self.ultimo_golpe >= 2000:  # 2000 milisegundos = 2 segundos
            if self.lados["main"].colliderect(enemigo.lados['main']):
                try:
                    print("Hiciste daño")
                except:
                    print("No se puede colisionar")
                #self.animar(pantalla, "enemigo_dañado")
                self.ultimo_golpe = tiempo_actual 

    def aplicar_gravedad(self, pantalla, piso, lista_plataformas):
        if self.esta_saltando:
            if self.direccion == "izquierda":
                self.animar(pantalla, "salta_izquierda")
            else:
                self.animar(pantalla, "salta_derecha")

            for lado in self.lados:
                self.lados[lado].y += self.desplazamiento_y

            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_caida:
                self.desplazamiento_y += self.gravedad

        if self.lados["bottom"].colliderect(piso["main"]):
            self.desplazamiento_y = 0
            self.esta_saltando = False
            self.lados["main"].bottom = piso["main"].top + 5
            self.puede_saltar = True
        else:
            self.esta_saltando = True
        
        for plataforma in lista_plataformas:
            if self.lados["bottom"].colliderect(plataforma.rect) and self.desplazamiento_y >= 0:
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.lados["main"].bottom = plataforma.rect.top + 5
                self.puede_saltar = True
                break

    def update(self, pantalla, piso, lista_plataformas, enemigo):
        
        
        if self.que_hace == "dispara":
            self.animar(pantalla, "personaje_dispara")
            self.golpear_enemigo(enemigo, pantalla)

        elif self.que_hace == "izquierda":
            if not self.esta_saltando:
                self.animar(pantalla, "camina_izquierda")
            self.mover(self.velocidad * -1)
            self.direccion = "izquierda"

        elif self.que_hace == "quieto":
            if not self.esta_saltando:
                self.animar(pantalla, "quieto")

        elif self.que_hace == "salta":
           if not self.esta_saltando and self.puede_saltar:
            self.esta_saltando = True
            self.desplazamiento_y = self.potencia_salto 
            self.puede_saltar = False
        
        elif self.que_hace == "derecha":
            if not self.esta_saltando:
                self.animar(pantalla, "camina_derecha")
            self.mover(self.velocidad)
            self.direccion = "derecha"
        
        

        self.aplicar_gravedad(pantalla, piso, lista_plataformas)


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("Recursos\Plataformas\plataforma1.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y


class Enemigos(Personaje):
    def __init__(self, tamaño, animaciones, posicion_inicial, velocidad):
        self.ancho = tamaño[0]
        self.alto = tamaño[1]
    
        self.contador_pasos = 0
        self.accion = "camina_derecha"
        self.animaciones = animaciones
        self.rescalar_animaciones()
        self.esta_saltando = False
 
        rectangulo = self.animaciones["camina_derecha"][0].get_rect()
        rectangulo.x = posicion_inicial[0]
        rectangulo.y = posicion_inicial[1]
        self.lados = obtener_rectangulos(rectangulo)

        #Salto
        self.desplazamiento_y = 0
        self.velocidad = velocidad
        self.que_hace = "quieto"
        self.puede_saltar = True
        self.direccion = 1

        self.gravedad = 1
        self.potencia_salto = -15
        self.limite_velocidad_caida = 15

        #Atacar
        self.vida_personaje = 3

        self.timer = pygame.USEREVENT + 1
        self.vida_enemigo = 3
        self.golpe_realizado = False

        pygame.time.set_timer(self.timer, 2000)
        self.ultimo_golpe = pygame.time.get_ticks()

    def rescalar_animaciones(self):
        for clave in self.animaciones:
            rescalarar_img(self.animaciones[clave], (self.ancho, self.alto))

    def animar(self, pantalla, que_animacion):
        animacion = self.animaciones[que_animacion]
        largo = len(animacion)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        
        pantalla.blit(animacion[self.contador_pasos], self.lados["main"])
        self.contador_pasos += 1


    def mover(self, velocidad):
        if(self.que_hace != "golpear"):
            for lado in self.lados:
                self.lados[lado].x += velocidad

    def aplicar_gravedad(self, piso, lista_plataformas):
        if self.esta_saltando:
            for lado in self.lados:
                self.lados[lado].y += self.desplazamiento_y

            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_caida:
                self.desplazamiento_y += self.gravedad

        if self.lados["bottom"].colliderect(piso["main"]):
            self.desplazamiento_y = 0
            self.esta_saltando = False
            self.lados["main"].bottom = piso["main"].top + 5
            self.puede_saltar = True
        else:
            self.esta_saltando = True
        
        for plataforma in lista_plataformas:
            if self.lados["bottom"].colliderect(plataforma.rect) and self.desplazamiento_y >= 0:
                self.desplazamiento_y = 0
                self.esta_saltando = False
                self.lados["main"].bottom = plataforma.rect.top + 5
                self.puede_saltar = True
                break



    def updateEnemigo(self, pantalla, piso, lista_plataformas, personaje):
        global vida_jugador
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_golpe >= 2000:
            self.golpe_realizado = False

        
        if self.lados["main"].colliderect(personaje.lados["main"]) and self.golpe_realizado == False:
            self.animar(pantalla, "ataca_derecha")
            self.golpe_realizado = True
            self.ultimo_golpe = tiempo_actual
            self.vida_personaje -= 1
            
        else:
            if self.que_hace == "quieto":
                self.animar(pantalla, "quieto")

            elif self.que_hace == "camina_derecha":
                self.animar(pantalla, "camina_derecha")

            elif self.que_hace == "camina_izquierda":
                self.animar(pantalla, "camina_izquierda")

            elif self.que_hace == "golpeando":
                self.animar(pantalla, "ataca_derecha")
        
            for lado in self.lados:
                rectangulo = self.lados[lado]

            if(rectangulo.right < 1280 - self.velocidad and self.direccion == 1):
                self.mover(self.velocidad)
                self.que_hace = "camina_derecha"
                
            elif rectangulo.right >= 1280 - self.velocidad and self.direccion == 1:
                self.direccion = -1
                self.mover(self.velocidad * -1)
                self.que_hace = "camina_izquierda"

            elif rectangulo.left > self.velocidad and self.direccion == -1:
                self.mover(self.velocidad * -1)
            elif rectangulo.left <= self.velocidad and self.direccion == -1:
                self.direccion = 1
                self.mover(self.velocidad)



        self.aplicar_gravedad(piso, lista_plataformas)




 
class Corazones():
    def __init__(self, vidas, w, h):
        self.w = w
        self.h = h
        self.vidas = vidas
        self.corazones = corazones_3
        self.image = pygame.image.load(self.corazones)
        self.image = pygame.transform.scale(self.image, (w, h))
        
    def cargar_imagen(self, imagen):
        self.imagen = imagen
        self.image = pygame.image.load(self.imagen)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

