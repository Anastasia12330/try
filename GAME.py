import pygame, os, random

pygame.init()
# окно
size = width, height = 600, 500 + 30
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ЗВЕЗДНЫЕ ВОЙНЫ')

#холст
window = pygame.Surface((width, height - 30))
info_string = pygame.Surface((width, 30))
screen2 = pygame.Surface(screen.get_size())
pygame.display.flip()
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT,20)

#определяем время исчезновения взрыва
MOMENT = pygame.USEREVENT
pygame.time.set_timer(MOMENT,2000)

#размер окна для сравнения при выходе за окно
screen_rect = (0, 0, width, height)
GRAVITY = 1

global x_geroy, y_geroy, LIVE

LIVE = 100
x_geroy = width // 2
y_geroy =height - 50


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    return image

# создаем класс космических кораблей
class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image_boom = Bomb.image_boom
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(x1, width - x1)
        self.rect.y = 0#random.randrange(y1, height - y1)
        self.speed = 1
        self.kill()
        while pygame.sprite.spritecollideany(self, all_bombs):
            self.rect.x = random.randint(x1, width - x1)
            self.rect.y = 0#random.randrange(y1, height - y1)
        all_bombs.add(self)


    def update(self):
        global LIVE
        if pygame.sprite.spritecollide(self, all_sprites1, True):
            all_bombs.remove(self)
            create_particles((self.rect.x, self.rect.y))
            print(LIVE)
            LIVE = 0
        if pygame.sprite.spritecollideany(self, all_bullets):
            self.kill()
            create_particles((self.rect.x, self.rect.y))
            #self.image = self.image_boom
        elif self.rect.y < height-50:
            #self.rect.x = self.rect.x + random.randint(-5, 5)
            self.rect.y += self.speed
        elif self.rect.y >= height - 50:
            self.kill()
            LIVE -= 10
            print(LIVE)
        pass


# создаем класс пуль
class Ball(pygame.sprite.Sprite):
    image = load_image("boom.png")
    image = pygame.transform.scale(image, (20, 20))
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = 0
        self.vy = -2
        self.speed = -5

    def update(self):
        self.rect = self.rect.move(self.vx, self.speed)
        # если попадает в корабль, то удаляется из группы
        # если промах, то удаляется из группы
        if not self.rect.colliderect(screen_rect):
            self.kill()
        if pygame.sprite.spritecollide(self, all_bombs, True):
            all_bullets.remove(self)
            create_particles((self.rect.x, self.rect.y))
            pass

        #if self.rect.y < 10:
            #self.kill()

#создаем класс конец игры
class GameOver(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        super().__init__()
        self.image = load_image(filename)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.dx = 2

    def update(self):
        self.rect.x -= self.dx
        #self.rect.y += self.dx
        if self.rect.x == width - x_image_game_over:# and self.rect.y == height - y_image_game_over:
            self.dx = 0

# создадим класс, разлетающугося взрыва
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        #self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        #self.velocity[1] += self.gravity
        #self.velocity[0] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

#функция перемещения героя
def move_geroy(keys):
    global x_geroy, y_geroy

    if keys[pygame.K_LEFT]:
        if x_geroy <= 0:
            x_geroy += 0
        else:
            x_geroy -= 3
    elif keys[pygame.K_RIGHT]:
        if x_geroy <= width - 50:
            x_geroy += 3
        else:
            x_geroy += 0
    elif keys[pygame.K_UP]:
        if y_geroy <= 0:
            y_geroy += 0
        else:
            y_geroy -= 3
    elif keys[pygame.K_DOWN]:
        if y_geroy < height - 50:
            y_geroy += 3
        else:
            y_geroy += 0

# создадим группу, разлетающугося взрыва
all_sprites = pygame.sprite.Group()

# создадим группу, содержащую все бомбочки
all_bombs = pygame.sprite.Group()

bomb_image = load_image("bomb.png")
x1, y1 = bomb_image.get_rect().size

# создадим группу, содержащую все шарики(пули)
all_bullets = pygame.sprite.Group()

#создаем героя
sprite = pygame.sprite.Sprite()
sprite.image = load_image("creature.png")
sprite.image = pygame.transform.scale(sprite.image, (50, 50))
sprite.rect = sprite.image.get_rect()
all_sprites1 = pygame.sprite.Group()

# создадим спрайт
#sprite = pygame.sprite.Sprite()
# определим его вид
#sprite.image = load_image("bomb.png")
# и размеры
#sprite.rect = sprite.image.get_rect()
# добавим спрайт в группу
all_sprites1.add(sprite)

# создадим спрайт конец игры
image_game_over = load_image('gameover.jpg')
image_game_over = pygame.transform.scale(image_game_over, (width, height))
x_image_game_over, y_image_game_over = image_game_over.get_rect().size
gameover = GameOver(width, -height, 'gameover.jpg')

image_begin = load_image("car2.png")
image_begin = pygame.transform.scale(image_begin, (width, height))

running = True
running_end = False
running_begin = False
running_game = False
#screen.fill(pygame.Color('white'))
while running:
    screen.fill((255, 255, 255))
    screen.blit(image_begin, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame. K_RETURN:
                running_game = True
                running = False
        # при нажатии правой мышкой конец игры
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                running_end = True
                running_game = False

    # основная игра
    while running_game:
        info_string.fill((45, 80, 45))
        screen.fill((255, 255, 255))
        screen.blit(info_string, (0,0))
        screen.blit(sprite.image, (x_geroy, y_geroy))
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
                #running = True

            #появление кораблей через интервал
            if event.type == pygame.USEREVENT:
                Bomb(all_bombs)

            if event.type == pygame.MOUSEBUTTONDOWN:# выстрел
                if event.button == 1:
                    Ball(all_bullets, (x_geroy, y_geroy))

            # при нажатии правой мышкой конец игры
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    running_end = True
                    running_game = False
            # возвращение на предыдущую страницу
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_game = False
                    running_end = False
                    running = True

        #for laser in all_bullets:
            #hit_list = pygame.sprite.spritecollide(laser, all_bombs, False)
            #for enemy in hit_list:
                #all_bullets.remove(laser)

        #движение героя
        keys = pygame.key.get_pressed()
        move_geroy(keys)

        # screen.fill(pygame.Color('white'))
        all_bombs.draw(screen)
        all_bombs.update()
        all_bullets.draw(screen)
        all_bullets.update()
        all_sprites.update()
        all_sprites.draw(screen)



        if LIVE == 0:# or pygame.sprite.spritecollideany(sprite.image_geroy, all_bombs, True) == 0:
            running_end = True
            running_game = False
            LIVE = 100
        pygame.display.flip()

    # конец игры score
    while running_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_game = True
                    running_end = False
                    running = True

        screen.fill(pygame.Color('blue'))
        screen.blit(gameover.image, gameover.rect)
        pygame.display.update()
        clock.tick(200)
        gameover.update()

    pygame.display.flip()
pygame.quit()
