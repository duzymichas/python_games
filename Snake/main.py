import pygame
import random
import copy
import os
pygame.font.init()

WIDTH,HEIGHT = 400,400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

class Snake:
    color = (255, 165, 0)

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.cells = [[self.x,self.y],[self.x-10,self.y]]
        self.direction = "right"
        self.length = len(self.cells)

    def draw_snake(self,window):
        for cell in self.cells:
            pygame.draw.rect(window, self.color, pygame.Rect(cell[0],cell[1], 10, 10))

    def move_snake(self,apples) -> None:
        if_ate = False
        for apple in apples:
            if [self.cells[0][0], self.cells[0][1]] == [apple[0],apple[1]]:
                apples.remove(apple)
                if_ate = True
        cells2 = copy.deepcopy(self.cells)
        for ind, coordinate in enumerate(self.cells):
            if ind != 0:
                coordinate[0] = cells2[ind-1][0]
                coordinate[1] = cells2[ind-1][1]
        if if_ate:
            self.cells.append(cells2[-1])
        if self.direction == "right":
            self.cells[0][0] += 10
        elif self.direction == "left":
            self.cells[0][0] -= 10
        elif self.direction == "up":
            self.cells[0][1] -= 10
        elif self.direction == "down":
            self.cells[0][1] += 10
        self.x = self.cells[0][0]
        self.y = self.cells[0][1]
        self.length = len(self.cells)

    def spawn_egg(self,eggs):
        eggs.append([self.cells[-1][0],self.cells[-1][1],240])

    def if_collide_eggs(self,eggs):
        for egg in eggs:
            if [egg[0],egg[1]] == [self.x,self.y]:
                return True
        return False

    def if_collide_snake(self):
        list_2 = copy.deepcopy(self.cells)
        list_2 = list_2[1:]
        for cell in list_2:
            if [self.cells[0][0],self.cells[0][1]] == [cell[0],cell[1]]:
                return True
        return False
def draw_apples_and_eggs(apples,eggs,window):
    for apple in apples:
        pygame.draw.rect(window, (0,255,0), pygame.Rect(apple[0], apple[1], 10, 10))
    for egg in eggs:
        pygame.draw.rect(window, (255,0, 0), pygame.Rect(egg[0], egg[1], 10, 10))

def main():
    run = True
    move_time = 3
    lost_timer = 0
    lost = False
    FPS = 60
    apples = []
    eggs = []
    clock = pygame.time.Clock()
    snake = Snake(200,200)
    best_font = pygame.font.SysFont("comicsans", 15)
    lost_font = pygame.font.SysFont("comicsans", 30)
    lives_font = pygame.font.SysFont("comicsans", 15)

    def redraw_window():
        WIN.fill("black")
        lives_label = lives_font.render(f"Length: {snake.length}", 1, (255, 255, 255))
        WIN.blit(lives_label, (390 - lives_label.get_width(), lives_label.get_height()/2))
        draw_apples_and_eggs(apples,eggs, WIN)
        if lost == True:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))
            lost_label2 = lost_font.render(f"Your score is {snake.length}", 1, (255, 255, 255))
            WIN.blit(lost_label, (140,120))
            WIN.blit(lost_label2, (100, 160))
            with open("best.txt",'r') as f:
                    best = f.readline()
                    if snake.length > int(best):
                        f.close()
                        os.remove("best.txt")
                        f_new = open("best.txt",'w')
                        f_new.write(str(snake.length))
                        f_new.close()
        snake.draw_snake(WIN)
        with open("best.txt", 'r') as f:
            best = f.readline()
            best_label = best_font.render(f"Best score: {best}", 1, (255, 255, 255))
            f.close()
        WIN.blit(best_label,(10, best_label.get_height()/2))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if lost:
            if lost_timer > 120:
                run = False
            else:
                lost_timer += 1
                continue
        if lost == False:
            if random.randrange(0, 120) == 1:
                new_apple = [random.randrange(0,40)*10,random.randrange(0,40)*10,600]
                apples.append(new_apple)
        if lost == False:
            if random.randrange(0, 120) == 1:
                snake.spawn_egg(eggs)
            for egg in eggs:
                if egg[2] == 0:
                    eggs.remove(egg)
                else:
                    egg[2] -= 1
        if snake.if_collide_eggs(eggs):
            lost = True
        if snake.if_collide_snake():
            lost = True
        for apple in apples:
            apple[2] -= 1
            if apple[2] == 0:
                apples.remove(apple)
        if move_time == 3 and lost == False:
            if keys[pygame.K_a] and snake.direction != "right":
                snake.direction = "left"
            elif keys[pygame.K_d] and snake.direction != "left":
                snake.direction = "right"
            elif keys[pygame.K_w] and snake.direction != "down":
                snake.direction = "up"
            elif keys[pygame.K_s] and snake.direction != "up":
                snake.direction = "down"
            snake.move_snake(apples)
            move_time = 0
        else:
            move_time += 1
        if snake.x >= WIDTH or snake.y >= HEIGHT - 10 or snake.y < 0 or snake.x < 0:
            lost = True

def main_menu():
    run = True
    lost = False
    clock = pygame.time.Clock()
    best_font = pygame.font.SysFont("comicsans", 15)
    start_font = pygame.font.SysFont("comicsans", 30)

    def redraw_window2():
        WIN.fill("black")
        with open("best.txt", 'r') as f:
            best = f.readline()
            best_label = best_font.render(f"Best score: {best}", 1, (255, 255, 255))
            f.close()
        WIN.blit(best_label,(10, best_label.get_height()/2))
        start_label = start_font.render("Press any key to start", 1, (255, 255, 255))
        WIN.blit(start_label, (50, 150))
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

