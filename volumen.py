import tkinter as tk
from tkinter import ttk
import threading
import pygame

class AudioControlWindow:
    def __init__(self, game_instance):
        self.game = game_instance

        # Crear ventana Tkinter en un hilo aparte
        self.thread = threading.Thread(target=self.create_window)
        self.thread.daemon = True
        self.thread.start()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Control de Audio")
        self.root.geometry("320x220")
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
