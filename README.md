# Encuentra el Audífono — Juego con Pygame + Control de Audio con Tkinter

Este proyecto implementa un mini-juego en Pygame donde el jugador debe encontrar un audífono oculto bajo objetos que reaccionan físicamente al movimiento del mouse.
Además incluye una ventana externa en Tkinter que permite controlar el volumen del juego, cambiar la canción, y mostrar información en pantalla ― todo esto usando hilos para que ambas ventanas funcionen simultáneamente.

#Características Principales

##Juego en Pygame

  ##Objetos ("basura") que:
  
  -Se mueven físicamente con empuje cuando el mouse se acerca.
    
  -Tienen colisiones entre sí.
    
  -Rebotan contra los bordes de la pantalla.

  ##Un audífono oculto que:
  
  -Se desplaza ligeramente cuando el mouse está cerca.
    
  -Se camufla con el color del fondo hasta ser encontrado.
    
  -Mecánica de victoria al hacer clic cerca del audífono.
    
  Sistema de audio direccional:
    
  -El volumen del canal derecho baja con la distancia al audífono.
    
  -Combina distancia + volumen del slider de Tkinter.

  ##🎚 Ventana de Control (Tkinter)
  
  ###Permite:
    
  -Ajustar volumen global del juego con un slider.
    
  -Cambiar entre distintas canciones.
    
  -Activar o desactivar información de depuración (F1).
    
  -Todo esto sin bloquear el loop de Pygame, gracias al uso de threads.
