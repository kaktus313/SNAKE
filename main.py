import pygame
from sys import exit
from time import sleep
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FIELD_SIZE = 30
TILE_SIZE = 20
SCREEN_SIZE = (FIELD_SIZE * TILE_SIZE), (FIELD_SIZE * TILE_SIZE)
FRAME_TIME = 0.09

def random_tuple_not_in_list(lst):
    while True:
        x, y = randint(1, FIELD_SIZE - 2), randint(1, FIELD_SIZE - 2)
        if not (x, y) in lst:
            return x, y

class Snake:
    def __init__(self, points_composition=[(25, 26), (25, 27), (25, 28), (25, 29)], direction = pygame.K_UP):
        self.points_composition = points_composition # tuples is (x, y)
        self.direction = direction
        self.is_growing_now = False

    def move(self):

        if not self.is_growing_now:
            del self.points_composition[-1]

        head = self.points_composition[0]

        if head in self.points_composition[1:]:
            return False

        if self.direction == pygame.K_LEFT:
            x, y = head[0] - 1, head[1]
        elif self.direction == pygame.K_RIGHT:
            x, y = head[0] + 1, head[1]
        elif self.direction == pygame.K_UP:
            x, y = head[0], head[1] - 1
        elif self.direction == pygame.K_DOWN:
            x, y = head[0], head[1] + 1

        if x < 0 or y < 0 or x > FIELD_SIZE - 1 or y > FIELD_SIZE - 1:
            return False

        self.points_composition.insert(0, (x, y))

        return True

    def directon_setter(self, value):

        if (self.direction == pygame.K_UP and value == pygame.K_DOWN) \
            or (self.direction == pygame.K_DOWN and value == pygame.K_UP) \
            or (self.direction == pygame.K_LEFT and value == pygame.K_RIGHT) \
            or (self.direction == pygame.K_RIGHT and value == pygame.K_LEFT):
            return

        self.direction = value

def main():

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("ЗМЕЙКА БЛЯТЬ")

    pygame.font.init()
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 15)

    snake = Snake()

    score_point_x, score_point_y = 3, 6

    frame_grow_counter = 0
    score = 0
    song = "napas_lavandos.ogg"

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)
    except:
        pass

    pygame.key.set_repeat()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_LEFT \
                    or event.key == pygame.K_UP \
                    or event.key == pygame.K_DOWN:
                    snake.directon_setter(event.key)
                elif event.key == pygame.K_m:
                    pygame.mixer.music.set_volume(not pygame.mixer.music.get_volume())

        #fill screen White
        screen.fill(WHITE)

        #frame delaying for growing snake
        if frame_grow_counter > 0:
            frame_grow_counter -= 1
        else:
            snake.is_growing_now = False

        #moving snake
        successful_moving = snake.move()
        if not successful_moving:
            break


        #building game_field
        game_field = [[0 for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)]
        for column, row in snake.points_composition:
            game_field[row][column] = BLACK

        #score point coordinates getting and putting on game_field
        game_field[score_point_y][score_point_x] = RED

        #if snake eat score_point
        if snake.points_composition[0] == (score_point_x, score_point_y):
            snake.is_growing_now = True
            frame_grow_counter += 4
            score_point_x, score_point_y = random_tuple_not_in_list(snake.points_composition)
            score += 1


        #drawing game_field on surface
        for row in range(len(game_field)):
            for column in range(len(game_field)):
                if game_field[row][column]:
                    pygame.draw.rect(screen, game_field[row][column]
                                     , (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # "delay"
        sleep(FRAME_TIME)

        scoretext = font_renderer.render("Score:" + str(score), 1, (45, 2, 64))
        musicinfotext = font_renderer.render("Чтобы выключить или включить блятскую музыку, можете нажать кнопку M", 1
        ,(45, 2, 64))

        screen.blit(musicinfotext, (10, 30))
        screen.blit(scoretext, (10, 10))

        # i don't know
        pygame.display.flip()

if __name__ == "__main__":
    main()
