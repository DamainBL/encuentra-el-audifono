# Encuentra el Audífono — Juego con Pygame + Control de Audio con Tkinter

Este proyecto implementa un mini-juego en Pygame donde el jugador debe encontrar un audífono oculto bajo objetos que reaccionan físicamente al movimiento del mouse.
Además incluye una ventana externa en Tkinter que permite controlar el volumen del juego, cambiar la canción, y mostrar información en pantalla ― todo esto usando hilos para que ambas ventanas funcionen simultáneamente.

# Características Principales

  ## Objetos ("basura") que:
  
  -Se mueven físicamente con empuje cuando el mouse se acerca.
    
  -Tienen colisiones entre sí.
    
  -Rebotan contra los bordes de la pantalla.

  ## Un audífono oculto que:
  
  -Se desplaza ligeramente cuando el mouse está cerca.
    
  -Se camufla con el color del fondo hasta ser encontrado.
    
  -Mecánica de victoria al hacer clic cerca del audífono.
    
  Sistema de audio direccional:
    
  -El volumen del canal derecho baja con la distancia al audífono.
    
  -Combina distancia + volumen del slider de Tkinter.

  ## 🎚 Ventana de Control (Tkinter)
  
  ### Permite:
    
  -Ajustar volumen global del juego con un slider.
    
  -Cambiar entre distintas canciones.
    
  -Activar o desactivar información de depuración (F1).
    
  -Todo esto sin bloquear el loop de Pygame, gracias al uso de threads.


# Estructura del proyecto

    /mi_proyecto/
    │── JuegoX.py          # Clase Game y TrashObject (Pygame)
    │── Volumen.py       # Ventana auxiliar Tkinter
    │── sprites/
    │      ├── audifono.png
    │      ├── cafe.png
    │      ├── manzana.png
    │      ├── papas.png
    │      └── dulce.png
    │── canciones/
    │      ├── tema1.mp3
    │      ├── tema2.mp3
    │      └── tema3.mp3

# Instalación

Requisitos:

    pip install pygame

## Ejecución

Ejecuta el archivo principal que instancie:

-Un objeto Game

-Una ventana AudioControlWindow

Ejemplo:

    from main_game import Game
    from audio_window import AudioControlWindow
    
    game = Game()
    AudioControlWindow(game)
    game.run()

# Explicación del Código (Resumen Técnico)

## Clase TrashObject

Representa cada objeto que cubre el audífono.

-Tiene física independiente.

-Se mueve por repulsión cuando el mouse se acerca.

-Colisiona con otros objetos usando empuje proporcional a la distancia.

-Aplica fricción para detener el movimiento.

## Métodos clave:

- update() → movimiento + empuje del mouse + rebotes.

- resolve_collision() → evita superposición entre objetos.

- draw() → dibuja el sprite.

## Clase Game

Controla todo el funcionamiento del juego.

## Componentes importantes:

-Inicialización de Pygame

-Carga del sprite del audífono

-Generación aleatoria de basura

-Física del audífono

-Cálculo de distancias

-Control de audio direccional

# Comunicación entre Pygame y Tkinter

El game loop de Pygame corre en el hilo principal.
Tkinter corre en un hilo separado:
    
    [ Hilo Principal ]  --->  Game.run()   (Pygame)
    [ Segundo Hilo   ]  --->  ventana Tkinter

Ambas comparten el mismo objeto game, sincronizando:

- volume

- current_music

- show_info

