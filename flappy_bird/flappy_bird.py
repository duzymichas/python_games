import pygame
import random
import copy
import os
from typing import Union

pygame.font.init()
WIDTH,HEIGHT = 288,512
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
bird_image_down = pygame.image.load(os.path.join("imgs", "bird1.png"))
bird_image_straight = pygame.image.load(os.path.join("imgs", "bird2.png"))
bird_image_up = pygame.image.load(os.path.join("imgs", "bird3.png"))
bg_image = pygame.image.load(os.path.join("imgs", "bg.png"))
base_image = pygame.image.load(os.path.join("imgs", "base.png"))
pipe_image_rotated = pygame.image.load(os.path.join("imgs", "pipe.png"))
pipe_image = pygame.transform.rotate(pipe_image_rotated, 180)

class bird:

    images = [bird_image_straight, bird_image_up, bird_image_down]

    def __init__(self, x: int, y: int, velocity: float,image):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.image = image
        self.mask = pygame.mask.from_surface(bird_image_straight)

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def move_up(self):
        self.velocity = 10

    def change_image(self):
        if self.velocity < 2 and self.velocity > -2:
            self.image = self.images[0]
        elif self.velocity <= -2:
            self.image = self.images[2]
        else:
            self.image = self.images[1]

class Pipe:

    hole_height:int = 100

    def __init__(self,x:int,y:int,velocity:int,img):
        self.x = x
        self.velocity = velocity
        self.mask = pygame.mask.from_surface(img)
        self.y = y
        self.img = img

    def draw(self):
        WIN.blit(self.img, (self.x,self.y))

def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None

def main():
    run = True
    lost = False
    flappy_bird = bird(50,250,0,bird_image_straight)
    FPS = 60
    clock = pygame.time.Clock()
    counter_acceleration = 0
    counter_pipes = 0
    counter_click = 0
    pipes = []
    lost_counter = 0
    lost_font = pygame.font.SysFont("comicsans", 15)
    score:int = 0

    def redraw_window():
        WIN.blit(bg_image, (0, 0))
        WIN.blit(base_image, (0, HEIGHT-base_image.get_height()))
        if lost == False:
            flappy_bird.draw()
            for pipe in pipes:
                pipe.draw()
        if lost == True and lost_counter < FPS * 3:
            for pipe in pipes:
                pipes.remove(pipe)
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 250))
            lost_label2 = lost_font.render(f"Your score is {int(score/2)}", 1, (255, 255, 255))
            WIN.blit(lost_label2, (90, 220))
            with open("best.txt", 'r') as f:
                best = f.readline()
                if score/2 > int(best):
                    f.close()
                    os.remove("best.txt")
                    f_new = open("best.txt", 'w')
                    f_new.write(str(int(score/2)))
                    f_new.close()
        with open("best.txt", 'r') as f:
            best = f.readline()
            best_label = lost_font.render(f"Best score: {best}", 1, (255, 255, 255))
            f.close()
        WIN.blit(best_label, (10, best_label.get_height() / 2))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #moving up
        if counter_pipes == 150:
            rand_height = random.randint(150,350)
            new_pipe1 = Pipe(x = 288, y = rand_height - pipe_image.get_height() - 50,velocity = 1.5, img = pipe_image)
            new_pipe2 = Pipe(x = 288, y = rand_height + 50,velocity = 1.5, img = pipe_image_rotated)
            pipes.append(new_pipe1)
            pipes.append(new_pipe2)
            counter_pipes = 0
        else:
            counter_pipes += 1
        for pipe in pipes:
            pipe.x -= pipe.velocity
            if pipe.x <= -50:
                pipes.remove(pipe)
                score += 1
            if collide(pipe, flappy_bird):
                lost = True
        if counter_click >= 20:
            if keys[pygame.K_SPACE]:
                flappy_bird.velocity = 5
                counter_click = 0
        else:
            counter_click += 1

        #changing image
        flappy_bird.change_image()

        #moving bird
        flappy_bird.y -= flappy_bird.velocity

        #lowering the velocity
        if counter_acceleration == 3:
            flappy_bird.velocity -= 1
            counter_acceleration = 0
        else:
            counter_acceleration += 1
        if lost == True:
            if lost_counter < FPS * 3:
                 lost_counter += 1
            else:
                run = False

def main_menu():
    run = True
    lost = False
    clock = pygame.time.Clock()
    best_font = pygame.font.SysFont("comicsans", 15)
    start_font = pygame.font.SysFont("comicsans", 15)

    def redraw_window2():
        WIN.blit(bg_image, (0, 0))
        WIN.blit(base_image, (0, HEIGHT - base_image.get_height()))
        with open("best.txt", 'r') as f:
            best = f.readline()
            best_label = best_font.render(f"Best score: {best}", 1, (255, 255, 255))
            f.close()
        WIN.blit(best_label,(10, best_label.get_height()/2))
        start_label = start_font.render("Press any key to start", 1, (255, 255, 255))
        WIN.blit(start_label, (65, 150))
        pygame.display.update()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        redraw_window2()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main()

main_menu()
