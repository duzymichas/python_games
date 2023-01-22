import pygame
import os
import random
import time
pygame.font.init()

WIDTH,HEIGHT = 600,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Laser:

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        WIN.blit(self.img, (self.x,self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self):
        return not(self.y < HEIGHT and self.y >= 0)

    def colision(self, obj):
        return collide(obj, self)


class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.cooldown_counter = 0
        self.lasers = []

    def draw(self, window):
        WIN.blit(self.ship_img, (self.x, self.y, 20 ,20))
        for laser in self.lasers:
            laser.draw()

    def move_lasers(self,vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.colision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cooldown_counter >=  self.COOLDOWN:
            self.cooldown_counter = 0
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

    def get_height(self):
        return self.ship_img.get_height()

    def get_width(self):
        return self.ship_img.get_width()

class Player(Ship):

    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            for obj in objs:
                if laser.colision(obj):
                    objs.remove(obj)
                    self.lasers.remove(laser)
            if laser.off_screen() and laser in self.lasers:
                self.lasers.remove(laser)

    def health_bar(self, window):
        pygame.draw.rect(window, (255,0,0),pygame.Rect(self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0),pygame.Rect( self.x, self.y + self.get_height() + 10, self.get_width()*(self.health/self.max_health), 10))

class Enemy(Ship):

    COLORMAP = {
        "GREEN":(GREEN_SPACE_SHIP, GREEN_LASER),
        "BLUE": (BLUE_SPACE_SHIP, BLUE_LASER),
        "RED": (RED_SPACE_SHIP, RED_LASER)
    }

    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img,self.laser_img = self.COLORMAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x - 20,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cooldown_counter = 1

def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None

def main():
    start_flag = False
    FPS = 60
    lost = False
    lost_counter = 0
    run = True
    clock = pygame.time.Clock()
    player = Player(500,500)
    Ship_velocity = 10
    laser_velocity = 10
    wave = 1
    enemies = []
    enemies_velocity = 1
    level = -1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 40)




    def redraw_window():
        WIN.blit(BACKGROUND, (0,0))
        lives_label = main_font.render(f"Lives: {lives}", 1 ,(255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        for enemy in enemies:
            enemy.draw(WIN)
        player.draw(WIN)
        player.health_bar(WIN)
        if start_flag == False:
            start_label = main_font.render(f"Press space to play once more", 1, (255, 255, 255))
            WIN.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, 250))
        if lost == True and lost_counter < FPS * 3:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,250))
        pygame.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()

        keys = pygame.key.get_pressed()

        if start_flag == False:
            if lost == False:
                if keys[pygame.K_SPACE]:
                    start_flag = True
                    continue
            else:
                if keys[pygame.K_SPACE]:
                    start_flag = True
                    main()



        if lives <= 0 or player.health <= 0:
            lost = True
            lost_counter += 1

        if lost:
            if lost_counter > FPS * 3:
                start_flag = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if start_flag == True:
            if len(enemies) == 0:
                level+= 1
                wave += 5
                for i in range(wave):
                    enemy = Enemy(random.randrange(50,WIDTH - 100),random.randrange(-1500,- 100), random.choice(["RED","GREEN","BLUE"]))
                    enemies.append(enemy)
            if keys[pygame.K_a] and player.x + 10 > 0:
                player.x -= Ship_velocity
            if keys[pygame.K_d] and player.x < WIDTH - player.get_height():
                player.x += Ship_velocity
            if keys[pygame.K_w] and player.y + 10 > 0:
                player.y -= Ship_velocity
            if keys[pygame.K_s] and player.y < HEIGHT - player.get_width() + 10:
                player.y += Ship_velocity

            if keys[pygame.K_SPACE]:
                player.shoot()

            for enemy in enemies[:]:
                enemy.y += enemies_velocity
                enemy.move_lasers(laser_velocity, player)
                if random.randrange(0,120) == 1:
                    enemy.shoot()
                if collide(enemy,player):
                    player.health -= 10
                    enemies.remove(enemy)
                elif enemy.y + enemy.get_height() > HEIGHT:
                    lives -= 1
                    enemies.remove(enemy)

            player.move_lasers(-laser_velocity,enemies)
main()