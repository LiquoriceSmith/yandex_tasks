# ВВОДИМ НАЗВАНИЕ ЛВЛ!!!
import os
import pygame
import sys

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 550, 550
screen = pygame.display.set_mode(size)
player = None


def load_image(name, colorkey=None):
    fullname = os.path.join('../../yandex_tasks/data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        if tile_type == 'wall':
            walls.add(self)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.rect.x -= tile_width
                if pygame.sprite.spritecollideany(self, walls) or self.rect.x <= 0:
                    self.rect.x += tile_width

            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.rect.y -= tile_height
                if pygame.sprite.spritecollideany(self, walls) or self.rect.y <= 0:
                    self.rect.y += tile_height

            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.x += tile_width
                if pygame.sprite.spritecollideany(self, walls) or self.rect.x >= WIDTH:
                    self.rect.x -= tile_width

            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.rect.y += tile_height
                if pygame.sprite.spritecollideany(self, walls) or self.rect.y >= HEIGHT:
                    self.rect.y -= tile_height


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Введите в потоковый ввод название уровня",
                  "Тыкните в любое место, ",
                  "чтобы начать игру"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    running = start_screen()
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')}
    player_image = load_image('mario.png')
    tile_width = tile_height = 50
    walls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    name_of_lvl = input()
    try:
        player, level_x, level_y = generate_level(load_level(name_of_lvl))
    except FileNotFoundError:
        print('Уровень ' + name_of_lvl + ' не найден')
        sys.exit()
    while running:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player_group.update(event)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()
