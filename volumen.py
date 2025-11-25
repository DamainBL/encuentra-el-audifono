import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pygame

class AudioControlWindow:
    def __init__(self, game_instance):
        self.game = game_instance

        # Crear ventana Tkinter en un hilo aparte
        self.thread = threading.Thread(target=self.create_window)
        self.thread.daemon = True
        self.thread.start()
        self.win_shown = False


    def create_window(self):
        self.root = tk.Tk()
        self.root.title("spotify")
        self.root.geometry("320x300")
        self.root.wm_resizable(0,0)
        # Dentro de create_window()
        self.root.bind("<F1>", self.toggle_info)


        # -----------------------------
        # SLIDER DE VOLUMEN
        # -----------------------------
        tk.Label(self.root, text="Volumen", font=("Arial", 12)).pack(pady=5)

        self.volume_slider = ttk.Scale(
            self.root,
            from_=0,
            to=1,
            orient="horizontal",
            length=250,
            command=self.update_volume
        )
        self.volume_slider.pack()

        # -----------------------------
        # LISTA DE CANCIONES
        # -----------------------------
        tk.Label(self.root, text="Selecciona canción", font=("Arial", 12)).pack(pady=10)

        self.song_listbox = tk.Listbox(self.root, height=6)
        self.song_listbox.pack(pady=5, fill=tk.X, padx=20)

        # Insertar canciones
        for idx, song in enumerate(self.game.music_list):
            self.song_listbox.insert(idx, song)

        # Seleccionar canción actual
        self.song_listbox.select_set(self.game.current_music)
        self.song_listbox.bind("<<ListboxSelect>>", self.select_song)

        

        # -----------------------------
        # info de como jugar
        # -----------------------------

        boton = tk.Button(self.root, text="como jugar", command=self.mostrar_mensaje)
        boton.pack(pady=20)

        self.check_win_condition()
        self.root.mainloop()

    # -----------------------------
    # FUNCIONES DE CONTROL
    # -----------------------------
    def update_volume(self, value):
        """Actualiza el volumen del canal de pygame."""
        vol = float(value)
        self.game.volume = vol

    def select_song(self, event):
        """Cambia la música según lo seleccionado en el Listbox"""
        if not self.game:
            return

        selection = self.song_listbox.curselection()
        if not selection:
            return

        idx = selection[0]
        if idx == self.game.current_music:
            return  # ya está sonando

        self.game.current_music = idx
        new_path = self.game.music_list[idx]

        # cargar nuevo sonido
        new_sound = pygame.mixer.Sound(new_path)

        # reproducir con el mismo volumen del slider
        vol = getattr(self.game, "volume", 1.0)
        channel = self.game.channel

        channel.stop()
        channel.play(new_sound, loops=-1)
        channel.set_volume(vol, vol)

        # actualizar referencia
        self.game.sound = new_sound
        
    def toggle_info(self, event):
        if self.game:
            self.game.show_info = not self.game.show_info
            print("Mostrar info:", self.game.show_info)

    def check_win_condition(self):
   
        if self.game.found and not self.win_shown:
            self.win_shown = True
            messagebox.showinfo("¡Ganaste!", "¡Felicitaciones, encontraste tu otro audifono! ahora podras escuchar musica por ambos lados \n\npara salir puedes precionar ¨esc¨")
        
        # Revisar cada 200 ms
        if not self.win_shown:
            self.root.after(200, self.check_win_condition)

    def mostrar_mensaje(self):
        messagebox.showinfo(title ="Como jugar / historia", message="Estabas caminando y escuchando tu musica sin copyrght comodamente hasta que tropezaste y se te callo tu audifono derecho, ahora debes buscarlo entre la basura de la calle \n\nComo jugar? \n\nutiliza tu mouse para mover la basura y buscar tu audifono, entre mas te acerques mas se escuchara en tu audifono o parlante derecho \n\ncuando creas que estas lo suficientemente cerca de el o sobre el da click para encontrarlo", icon = 'info')
