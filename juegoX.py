import pygame
import random
import math

class TrashObject:
    def __init__(self, x, y, image_path, size):
        self.x = x
        self.y = y
        self.size = size  # radio para colisiones

 
        self.vx = 0
        self.vy = 0
        self.friction = 0.95  # para que no se deslicen infinitamente

        # Cargar imagen
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (size * 2, size * 2))

        # Rect para dibujar
        self.rect = self.image.get_rect(center=(self.x, self.y))


    # --------------------------
    #   FÍSICA DE EMPUJE DEL MOUSE
    # --------------------------
    def update(self, mouse_x, mouse_y, width, height):
        dx = self.x - mouse_x
        dy = self.y - mouse_y
        dist = math.hypot(dx, dy)

        # Empuje solo si el mouse está cerca
        if dist < 80 and dist != 0:
            force = (80 - dist) / 80  # fuerza inversa a la distancia
            self.vx += (dx / dist) * force * 1.5
            self.vy += (dy / dist) * force * 1.5

        # Aplicar fricción suave
        self.vx *= self.friction
        self.vy *= self.friction

        # Mover basura
        self.x += self.vx
        self.y += self.vy

        # Bordes pantalla (rebote suave)
        if self.x < self.size:
            self.x = self.size
            self.vx *= -0.5
        if self.x > width - self.size:
            self.x = width - self.size
            self.vx *= -0.5

        if self.y < self.size:
            self.y = self.size
            self.vy *= -0.5
        if self.y > height - self.size:
            self.y = height - self.size
            self.vy *= -0.5

        # Actualizar rect
        self.rect.center = (self.x, self.y)


    # --------------------------
    #   COLISIÓN ENTRE BASURAS
    # --------------------------
    def resolve_collision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)

        min_dist = self.size + other.size

        if dist < min_dist and dist != 0:
            overlap = min_dist - dist

            push_x = (dx / dist) * (overlap / 2)
            push_y = (dy / dist) * (overlap / 2)

            # Separar objetos
            self.x -= push_x
            self.y -= push_y
            other.x += push_x
            other.y += push_y

            # Actualizar rect
            self.rect.center = (self.x, self.y)
            other.rect.center = (other.x, other.y)


    # --------------------------
    #     DIBUJO DEL SPRITE
    # --------------------------
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # --- Ventana ---
        self.WIDTH, self.HEIGHT = 900, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Encuentra el audífono - Ventana de juego")

        self.clock = pygame.time.Clock()
        self.FPS = 60

        # --- Colores ---
        self.WHITE = (255, 255, 255)
        self.GRAY = (40, 40, 40)
        self.RED = (255, 0, 0)
        self.Color = self.GRAY

        self.music_list = [
            "canciones/tema1.mp3",
            "canciones/tema2.mp3",
            "canciones/tema3.mp3"
        ]
        self.current_music = 1

        self.volume = 0.1  # volumen inicial

        # --- Fuente ---
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(
            "Encuentra el audífono. ESC para salir.",
            True,
            self.WHITE
        )

        # --- Estados generales ---
        self.running = True
        self.found = False
        self.show_info = False   

        # --- Carga de recursos ---
        self.load_audio()
        self.load_sprite()
        self.init_headphone_position()
        self.generate_trash()



    # ------------------------------------------------------
    #                   CARGA DE RECURSOS
    # ------------------------------------------------------

    def load_sprite(self):
        try:
            img = pygame.image.load("sprites/audifono.png").convert_alpha()
        except:
            print("ERROR: No se pudo cargar audifono.png")
            self.running = False
            return

        self.headphone_img = pygame.transform.smoothscale(img, (64, 64))
        self.sprite_w = self.headphone_img.get_width()
        self.sprite_h = self.headphone_img.get_height()

    def load_audio(self):
        self.sound = pygame.mixer.Sound(self.music_list[self.current_music])
        self.channel = self.sound.play(loops=-1)


    # ------------------------------------------------------
    #                 POSICIÓN INICIAL AUDÍFONO
    # ------------------------------------------------------

    def init_headphone_position(self):
        self.headphone_radius = 12
        self.headphone_x = random.randint(self.headphone_radius, self.WIDTH - self.headphone_radius)
        self.headphone_y = random.randint(self.headphone_radius, self.HEIGHT - self.headphone_radius)

        # Física del audífono
        self.vx = 0
        self.vy = 0
        self.friction = 0.92
        self.push_strength = 0.18
        self.push_radius = 25

        self.header_text = self.font.render(
            "Encuentra el audífono. ESC para salir.", True, (181, 175, 101)
        )

    # ------------------------------------------------------
    #                     GENERAR BASURA
    # ------------------------------------------------------

    def generate_trash(self):
        trash_sprites = [
            "sprites/cafe.png",
            "sprites/manzana.png",
            "sprites/papas.png",
            "sprites/dulce.png"
        ]

        SIZE_OPTIONS = [
        12, 15, 18,   # basura pequeña
        22, 26, 30,   # basura mediana
        34, 38, 45    # basura grande
        ]

        self.trash = []
        TRASH_AMOUNT = 180
        for _ in range(TRASH_AMOUNT):
            size = random.choice(SIZE_OPTIONS)
            img_path = random.choice(trash_sprites)

            x = random.randint(size, self.WIDTH - size)
            y = random.randint(size, self.HEIGHT - size)

            obj = TrashObject(x, y, img_path, size=size)
            self.trash.append(obj)
    # ------------------------------------------------------
    #                     FÍSICA AUDÍFONO
    # ------------------------------------------------------

    def apply_physics(self, mx, my):
        dx = self.headphone_x - mx
        dy = self.headphone_y - my
        dist = math.hypot(dx, dy)

        if dist < self.push_radius and dist > 0:
            force = (self.push_radius - dist) / self.push_radius
            force *= self.push_strength
            nx, ny = dx/dist, dy/dist
            self.vx += nx * force
            self.vy += ny * force

        self.headphone_x += self.vx
        self.headphone_y += self.vy

        self.vx *= self.friction
        self.vy *= self.friction

        if self.headphone_x < self.headphone_radius:
            self.headphone_x = self.headphone_radius
            self.vx *= -0.4
        if self.headphone_x > self.WIDTH - self.headphone_radius:
            self.headphone_x = self.WIDTH - self.headphone_radius
            self.vx *= -0.4
        if self.headphone_y < self.headphone_radius:
            self.headphone_y = self.headphone_radius
            self.vy *= -0.4
        if self.headphone_y > self.HEIGHT - self.headphone_radius:
            self.headphone_y = self.HEIGHT - self.headphone_radius
            self.vy *= -0.4

    # ------------------------------------------------------
    #                    AUDIO DEL JUEGO
    # ------------------------------------------------------

    def update_audio(self, dist):
        
        # Volumen general controlado por slider
        slider_vol = getattr(self, "volume", 1.0)  # default 1.0 si no existe

        if self.found:
            self.channel.set_volume(slider_vol,slider_vol )
            return


        # Volumen adicional por distancia
        dist_vol = max(0, min(1, 1 - dist / 500))

        # Aplicar multiplicación para combinar ambos
        left_vol = slider_vol
        right_vol = slider_vol * dist_vol

        self.channel.set_volume(left_vol, right_vol)

    # ------------------------------------------------------
    #                         DIBUJO
    # ------------------------------------------------------

    def draw(self, dist):
        self.screen.fill(self.GRAY)

 
        if self.show_info:
            # Info de distancia y estado
            info = self.font.render(f"Distancia: {int(dist)} px | Encontrado: {self.found}", True, self.WHITE)
            self.screen.blit(info, (20, 60))


        if self.show_info:
            self.Color = self.RED  
        else:
            self.Color = self.GRAY
            



        # --- Dibujar audífono SOLO si NO está encontrado (debajo de la basura) ---
        if not self.found:
            # En vez de círculo, lo dibujamos DEL MISMO COLOR DEL FONDO
            pygame.draw.circle(
                self.screen,
                self.Color,  # MISMO COLOR DEL FONDO → se camufla
                (self.headphone_x, self.headphone_y),
                self.headphone_radius
            )

        # --- Dibujar basura (encima del audífono) ---
        for obj in self.trash:
            obj.draw(self.screen)

        # --- Si está encontrado, mostrar sprite real por encima de todo ---
        if self.found:
            self.screen.blit(
                self.headphone_img,
                (self.headphone_x - self.sprite_w // 2,
                self.headphone_y - self.sprite_h // 2)
            )

        self.screen.blit(self.header_text, (20, 20))

    # ------------------------------------------------------
    #                     BUCLE PRINCIPAL
    # ------------------------------------------------------
    def run(self):
        if not self.running:
            return

        while self.running:
            # --- EVENTOS ---
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    self.running = False

            mx, my = pygame.mouse.get_pos()
            dx = mx - self.headphone_x
            dy = my - self.headphone_y
            dist = math.hypot(dx, dy)
            
            # --- FÍSICA DEL AUDÍFONO ---
            if not self.found:
                self.apply_physics(mx, my)

            # --- ACTUALIZAR BASURA ---
            for obj in self.trash:
                obj.update(mx, my, self.WIDTH, self.HEIGHT)

            # --- COLISIONES ENTRE BASURA ---
            for i in range(len(self.trash)):
                for j in range(i+1, len(self.trash)):
                    self.trash[i].resolve_collision(self.trash[j])

            # --- CLICK PARA GANAR ---
            if not self.found and pygame.mouse.get_pressed()[0] and dist < 25:
                self.found = True

            # --- AUDIO ---
            self.update_audio(dist)

            # --- DIBUJAR ---
            self.draw(dist)

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
