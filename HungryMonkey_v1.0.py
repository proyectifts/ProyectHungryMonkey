# -*- encoding: utf-8 -*-

'''
Hungry MonkeyPYTHON

Juego desarrollado en Python utilizando el framework de Pilas Engine.

Autores:			Fecha: NOV-2015
Silvera Claudia
Ritacco Dario
'''

import random
import pilasengine

'''
Estado

Clase base de todos los estados posibles del juego.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class Estado:

    def __init__(self, mono):
        self.mono = mono
        self.iniciar()

    def iniciar(self):
        pass

'''
Ingresando

Setea todos los valores iniciales del juego y te da un tiempo de un segundo para iniciar el juego.
Inicia el juego.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class Ingresando(Estado):

    def iniciar(self):
        self.contador = 0
        self.mono.y = -380
        self.mono.y = [-180], 0.5

    def actualizar(self):
        self.contador += 1

        if self.contador == 60:
            pilas.avisar("Llega a 20 bananas para pasar de nivel")
            self.mono.estado = Jugando(self.mono)

'''
Jugando

Permite controlar los movimiento del personaje y los limites de la pantalla.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class Jugando(Estado):

    def iniciar(self):
        pass

    def actualizar(self):
        velocidad = 5

        if pilas.escena.control.derecha:
            self.mono.x += velocidad
        elif pilas.escena.control.izquierda:
            self.mono.x -= velocidad

        if self.mono.x > 210:
            self.mono.x = 210
        elif self.mono.x < -210:
            self.mono.x = -210

'''
Perdiendo

Genera la animacion cuando se pierde en el juego.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class Perdiendo(Estado):

    def iniciar(self):
        self.mono.centro = ('centro', 'centro')
        self.velocidad = -2

    def actualizar(self):
        self.mono.rotacion += 7
        self.mono.escala += 0.01
        self.mono.x -= self.velocidad
        self.velocidad += 0.2
        self.mono.y -= 1

'''
Ganando

Clase que representa el estado "ganar" del juego.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class Ganando(Estado):

    def iniciar(self):
        self.mono.centro = ('centro', 'centro')

    def actualizar(self):
        self.mono.escala = 1

'''
MonoPersonalizado

Hijo del actor Mono de Pilas con metodos especificos para determinar el
comportamiento especifico de cuando se gana o se pierde el juego.

Autor:				Fecha: NOV-2015
Ritacco Dario
'''
class MonoPersonalizado(pilasengine.actores.Mono):

    def iniciar(self):
        self.escala = 0.5
        self.y = -170
        self.estado = Ingresando(self)
        self.contador = 0

    def actualizar(self):
        self.estado.actualizar()

    def perder(self):
        mono.gritar()
        self.estado = Perdiendo(self)
        t = pilas.actores.Texto("Perdiste =(")
        t.definir_color(pilas.colores.negro)
        t.x = 0
        t.y = 0
        t.escala = 0
        t.escala = [1], 0.5
        mono.radio_de_colision = 0
        pilas.tareas.eliminar_todas() #elimina tareas de agregar bananas y bombas

    def ganar(self):
        mono.radio_de_colision = 0
        mono.sonreir()
        mono.escala = 1.5
        mono.x = [1],  3
        mono.y = [1],  3
        mono.decir("Ganaste!!")
        self.estado = Ganando(self)
        pilas.tareas.eliminar_todas()

'''
Enemigo

Hijo del actor Bomba de Pilas con seteos especificos para hacer
aleatorio el lugar donde aparece cada bomba, determinar la velocidad
de caida, el punto de partida y la configuraciones del objeto.

Autor:				Fecha: NOV-2015
Silvera Claudia
'''
class Enemigo(pilasengine.actores.Bomba):

    def iniciar(self):
        pilasengine.actores.Bomba.iniciar(self)
        self.escala = 0.75
        self.arriba = 320
        self.x = random.randint(-210, 210)

    def actualizar(self):
        self.y -= 5
        pilasengine.actores.Bomba.actualizar(self)

'''
Item

Hijo del actor Banana de Pilas con seteos especificos para hacer
aleatorio el lugar donde aparece cada banana, determinar la velocidad
de caida, el punto de partida y la configuraciones del objeto.
Verifica las bananas que dejo pasar el personaje y aumenta un contador.

Autor:				Fecha: NOV-2015
Silvera Claudia
'''
class Item(pilasengine.actores.Banana):

    def iniciar(self):
        self.arriba = 320
        self.x = random.randint(-210, 210)

    def actualizar(self):
        self.abajo -= 5

        if self.arriba < -230:
            vidasPuntaje.aumentar(1)
            self.eliminar()

'''
ContadorDeVidas

Actor que representa un contador de vidas del personaje.
Hace referencia a las tres bananas de vidas que aparecen en el extremo
superior izquierdo de la pantalla.
Está la logica para que se pierdan vidas ante cada banana que no agarro
el personaje. Si se consumen las tres bananas se pierde el juego.

Autor:				Fecha: NOV-2015
Silvera Claudia
'''
class ContadorDeVidas(pilasengine.actores.Actor):

	#iniciamos el actor y lo sacamos de pantalla
    def iniciar(self):
        self.x = 500
        self.vidas = [pilas.actores.Banana() for x in range(3)]
		#recorro las vidas para moverlas y que no se superpongan
        for indice, vida in enumerate(self.vidas):
            vida.escala=1.25
            vida.x = -270 + indice * 40
            vida.arriba = 200

	#se ejecuta cada vez que cambia el frame
    def actualizar(self):
		#ante cada banana que pasa se resta una vida.
		#se agrego len(self.vidas) ya que vidasPuntaje.obtener no alcanza para que se descuente
		#solo una banana cada vez que el personaje deja pasar una banana.
        if((vidasPuntaje.obtener() == 1 and len(self.vidas) == 3)
                or (vidasPuntaje.obtener() == 2 and len(self.vidas) == 2)
                or (vidasPuntaje.obtener() == 3 and len(self.vidas) == 1)):
				#elimina una vida tomando el ultimo registro de la pila.
                vida = self.vidas.pop()
                vida.eliminar()
		#si se dejan pasar tres bananas se ejecuta el metodo perder del mono.
        if(vidasPuntaje.obtener() == 3 and len(self.vidas) == 0):
                vidasPuntaje.aumentar(1)
                mono.perder()


'''
Se definen todos los elementos que componenen el juego.
Funciones:
    crear_item --> Para crear las bananas
    cuando_toca_item --> Logica de colisiones con las bananas
    crear_enemigo--> Para crear las bombas
    cuando_toca_enemigo--> Logica de colisiones con las bombas


Autor:				Fecha: NOV-2015
Silvera Claudia
Ritacco Dario
'''
pilas = pilasengine.iniciar()

fondo = pilas.fondos.Selva()

vidasPuntaje = pilas.actores.Puntaje(x=500, y=150)

puntos = pilas.actores.Puntaje(x=280, y=150)

nivel = pilas.actores.Texto(x=270, y=180)
nivel.definir_texto("Nivel 1")
nivel.definir_color(pilas.colores.negro)

mono = MonoPersonalizado(pilas)
items = []
enemigos = []

#vinculo a mi actor personalizado dentro de pilas para poder ser utilizado
pilas.actores.vincular(ContadorDeVidas)
vidas = pilas.actores.ContadorDeVidas()

def crear_item():
    un_item = Item(pilas)
    items.append(un_item)
    return True

#Se agrega una tarea a pilas de crear banana cada dos segundos
pilas.tareas.agregar(2, crear_item)

def cuanto_toca_item(v, i):
    mono.sonreir()
    i.eliminar()
    puntos.aumentar(1)
    puntos.escala = 4
    puntos.escala = [1], 0.2
    puntos.rotacion = random.randint(30, 60)
    puntos.rotacion = [0], 0.2
    if(puntos.obtener() == 20):
        pilas.avisar("Llega a 50 bananas para ganar el juego")
        nivel.definir_texto("Nivel 2")
        nivel.escala = 4
        nivel.escala = [1], 0.2
        nivel.rotacion = random.randint(30, 60)
        nivel.rotacion = [0], 0.2
    if(puntos.obtener() == 50):
        mono.ganar()

#cuando el personaje colisiona con una banana ejecuta el metodo cuando_toca_item
pilas.colisiones.agregar(mono, items, cuanto_toca_item)

def crear_enemigo():
    un_enemigo = Enemigo(pilas)
    enemigos.append(un_enemigo)
    return True

#Se agrega una tarea a pilas de crear bomba cada 3.3 segundos
pilas.tareas.agregar(3.3, crear_enemigo)


def cuanto_toca_enemigo(mono, enemigo):
    enemigo.eliminar()
    mono.perder()

#cuando el personaje colisiona con una bomba ejecuta el metodo cuando_toca_enemigo
pilas.colisiones.agregar(mono, enemigos, cuanto_toca_enemigo)

pilas.ejecutar()
