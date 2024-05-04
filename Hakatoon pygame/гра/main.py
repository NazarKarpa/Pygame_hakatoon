import time
import pygame.locals
from pygame import *
from random import randint, choice
import os
import sys

init()
font.init()

WIDTH, HEIGHT = 900,600

bg = image.load('background-1.png')
bg = transform.scale(bg, (WIDTH, HEIGHT))


player_image = image.load('car0.png')
player_image = transform.scale(player_image, (50, 80))

button_image_again = image.load('again_1-removebg-preview.png')
button_image_play = image.load('PlayButton.png')
button_image_exit = image.load('Quit_button-removebg-preview.png')
button_image_home = image.load('HomeButton.png')
button_image_setting = image.load('menu_2_2_2.png')

pause_image = image.load('PauseButton.png')

enemy_image2 = image.load('car-truck2.png')
enemy_image3 = image.load('car-truck4.png')
enemy_image4 = image.load('car-truck5.png')

enemys_images = [enemy_image2, enemy_image3, enemy_image4]

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, rect_x, rect_y, speed):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.speed = speed
        self.mask = mask.from_surface(self.image)

    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):

        if keys[K_d] and self.rect.x < 700:
            self.rect.x += self.speed
            self.image = transform.rotate(player_image, -10)
        elif keys[K_a] and self.rect.x > 150:
            self.rect.x -= self.speed
            self.image = transform.rotate(player_image, 10)
        if keys[K_w] and self.rect.y > 50:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 500:
            self.rect.y += self.speed

class Enemy(GameSprite):

    def update(self):

        if self.rect.y > -200:
            self.rect.y -= self.speed

class Button(GameSprite):
    pass

def random_car():
    rand_race = randint(1, 4)
    rand_y = randint(600, 800)
    rand_speed = randint(4, 6)
    enemy_image = choice(enemys_images)
    if rand_race == 1:
        enemy = Enemy(enemy_image, 50, 95, 210, rand_y, rand_speed)
    if rand_race == 2:
        enemy = Enemy(enemy_image, 50, 95, 350, rand_y, rand_speed)
    if rand_race == 3:
        enemy = Enemy(enemy_image, 50, 95, 500, rand_y, rand_speed)
    if rand_race == 4:
        enemy = Enemy(enemy_image, 50, 95, 630, rand_y, rand_speed)
    collision = sprite.spritecollideany(enemy, enemys)


    if not collision:
        enemys.add(enemy)








enemys = sprite.Group()

player = Player(player_image, 48, 80, 340, 300, 5)

button_again = Button(button_image_again, 200, 200, 350, 180, 1)
button_play = Button(button_image_play, 300, 200, 300, 20, 1)
button_exit = Button(button_image_exit, 250, 150, 330, 450, 1)
button_home = Button(button_image_home, 102, 102, 400, 400, 1)
button_setting = Button(button_image_setting, 100, 100, 0, 500, 1)

pause = Button(pause_image, 108, 108, 395, 220, 1)

window = display.set_mode((WIDTH, HEIGHT))

screen = 'menu'
while_game = True
finish = False

FPS = 60



font1 = font.SysFont("Aril", 35)
font2 = font.SysFont("Aril", 100)
txt_lose_game = font2.render("You lose", True, (255, 0, 0))


clock = time.Clock()
start_time = time.get_ticks()
rand_interval = randint(200, 1300)
clock_time = 0
frames = 0



while while_game:
    global mouse_x, mouse_y
    if screen == 'menu':
        window.blit(bg, (0, 0))
        button_play.draw()
        button_exit.draw()
        button_setting.draw()

        button_home.rect.y = 400
        button_home.rect.x = 400

        for e in event.get():
            keys = key.get_pressed()
            if e.type == QUIT:
                while_game = False

            elif e.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = e.pos
                if button_play.rect.collidepoint(mouse_x, mouse_y):
                    screen = 'game'
                if button_exit.rect.collidepoint(mouse_x, mouse_y):
                    while_game = False
                if button_setting.rect.collidepoint(mouse_x, mouse_y):
                    screen = 'setting'
    elif screen == 'setting':
        window.blit(bg, (0, 0))
        for e in event.get():

            keys = key.get_pressed()
            if e.type == QUIT:

                while_game = False
            if e.type == MOUSEBUTTONDOWN:
                if button_home.rect.collidepoint(mouse_x, mouse_y):
                    clock_time = 0
                    screen = 'menu'
                    enemys.empty()
                    player.rect.x = 340
                    player.rect.y = 300
        button_home.rect.y = 490
        button_home.rect.x = 0
        button_home.draw()




    if finish == False and screen == 'game':
        window.blit(bg, (0, 0))

        for e in event.get():
            keys = key.get_pressed()
            if e.type == QUIT:
                while_game = False

            elif e.type == KEYDOWN:

                if keys[K_ESCAPE]:
                    finish = True
                    pause.draw()
                    button_play.draw()
                    button_home.draw()
                    if e.type == MOUSEBUTTONDOWN:
                        if button_home.rect.collidepoint(mouse_x, mouse_y):
                            clock_time = 0
                            screen = 'menu'
                            enemys.empty()
                            player.rect.x = 340
                            player.rect.y = 300



        if time.get_ticks() - start_time > rand_interval:
            random_car()
            start_time = time.get_ticks()
        frames += 1
        if frames >= 55:
            clock_time += 1
            frames = 0

        spritelist = sprite.spritecollide(player, enemys, False)


        for collide in spritelist:

            window.blit(txt_lose_game, (320, 100))
            button_again.draw()
            button_home.draw()
            finish = True







        txt_time = font1.render(f"Час: {clock_time}", True, (200, 200, 100))
        window.blit(txt_time, (30, 30))

        player.draw()
        enemys.draw(window)
        enemys.update()
        player.update()
    elif finish == True:
        for e in event.get():
            keys = key.get_pressed()
            if e.type == QUIT:
                while_game = False

            if e.type == MOUSEBUTTONDOWN:
                if button_play.rect.collidepoint(mouse_x, mouse_y):
                    finish = False

                mouse_x, mouse_y = e.pos
                print(mouse_y, '-y', mouse_x, '-x')

                if button_again.rect.collidepoint(mouse_x, mouse_y):
                    clock_time = 0
                    enemys.empty()

                    player.rect.x = 340
                    player.rect.y = 300

                    finish = False
                elif button_home.rect.collidepoint(mouse_x, mouse_y):
                    clock_time = 0
                    screen = 'menu'
                    enemys.empty()
                    player.rect.x = 340
                    player.rect.y = 300
                    finish = False

    display.update()
    # Обмеження кадрів в секунду (FPS)
    clock.tick(FPS)


