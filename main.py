import pygame
import os
import math
import random

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
tick = 30

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "bg", "background0.png")), (screen_width, screen_height))


def load_sprites(dir1, dir2, width, height):
    list_sprites = os.listdir(os.path.join("assets", dir1, dir2))
    sprites = []
    for sprite_img in list_sprites:
        sprites.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", dir1, dir2, sprite_img)), (width, height)))
    
    return sprites

class Player(pygame.sprite.Sprite):
    
    SPRITES = load_sprites("images", "player", 128, 128)
    
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.current_sprite = 0
        self.image = self.SPRITES[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos, y_pos]
        self.moving = False
        self.direction = "right"
        self.x_vel = 0
        self.y_vel = 0
        self.fall_count = 0
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        
    def move_right(self, vel):
        if self.rect.x <= screen_width:
            self.moving = True
            self.x_vel = vel
            self.direction = "right"
            
    def move_left(self, vel):
        if self.rect.x >= 0:
            self.moving = True
            self.x_vel = -vel
            self.direction = "left"
    
    def idle(self):
        self.moving = False
    
    def loop(self):
        self.y_vel += min(1, (self.fall_count / tick) * 1)
        self.move(self.x_vel, self.y_vel)
            
    def update(self):
        self.loop()
        if self.direction == "right":
                self.image = self.SPRITES[int(self.current_sprite)]
        if self.direction == "left":
            self.image = pygame.transform.flip(self.SPRITES[int(self.current_sprite)], True, False)
        if self.moving:
            self.current_sprite += 0.4
            if self.current_sprite >= len(self.SPRITES):
                self.current_sprite = 0
        else:
            self.current_sprite = 0
        self.fall_count += 1
        self.landed()
        
    def landed(self):
        if self.rect.y >= screen_height:
            self.fall_count = 0 
            self.y_vel = 0
  
                
def draw_win(sprites):
    screen.blit(bg, (0,0))
    sprites.draw(screen)
    pygame.display.update()

def main():
    sprites = pygame.sprite.Group()
    player = Player(100, 100, 32, 32)
    sprites.add(player)
    
    running = True
    while running:
        clock.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            player.move_right(10)
        elif key[pygame.K_a]:
            player.move_left(10)
        else:
            player.idle()
        
        
        sprites.update()
        draw_win(sprites)
    pygame.quit()

if __name__ == "__main__":
    main()