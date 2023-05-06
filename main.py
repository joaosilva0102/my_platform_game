import pygame
import os
import math
import random
from level import *

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

def create_terrain():
    
    blocks = []
    terrain_height = len(level_terrain)
    terrain_width = len(level_terrain[0])
    
    IMG = load_sprites("images","ground", 64, 64)
    
    for row in range(len(level_terrain)):
        for col in range(len(level_terrain[0])):
            terrain_block = level_terrain[row][col]
            if terrain_block == EMPTY:
                continue
            img = IMG[terrain_block]
            x_pos = col * 64
            y_pos = screen_height - (64 * (terrain_height - row))
            block = Block(x_pos, y_pos, 64, 64, img)
            blocks.append(block)

    return blocks

class Block(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos, width, height, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos, y_pos]
        self.mask = pygame.mask.from_surface(self.image)

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
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_count = 0
    
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
        self.y_vel += min(1, (self.fall_count / tick) * 8)
        if not self.moving:
            self.x_vel = 0
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
            
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
        self.mask = pygame.mask.from_surface(self.image)
        
    def landed(self):
        self.fall_count = 0 
        self.y_vel = 0
        self.jump_count = 0
        
    def hit_head(self):
        self.y_vel *= -1
        
    def collision_side(self):
        self.x_vel = 0
        
    def jump(self):
        self.y_vel = -2 * 6
        self.current_sprite = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0
        
                
def draw_win(player_sprites, ground_sprites):
    screen.blit(bg, (0,0))
    ground_sprites.draw(screen)
    player_sprites.draw(screen)
    pygame.display.update()

def handle_collisions(player, ground_sprites):
    for block in ground_sprites:
        collision_point = pygame.sprite.collide_mask(player, block)
        if collision_point:
            if player.y_vel > 0:
                player.rect.bottom = block.rect.top + 17
                player.landed()
                
def handle_horizontal_collisions(player, ground_sprites):
    for block in ground_sprites:
        collision_point = pygame.sprite.collide_mask(player, block)
        if collision_point:
            if player.rect.right > block.rect.left and player.x_vel > 0:
                # Player collided with the left side of the block while moving right
                player.rect.right = block.rect.left
                player.collision_side()
            elif player.rect.left < block.rect.right and player.x_vel < 0:
                # Player collided with the right side of the block while moving left
                player.rect.left = block.rect.right
                player.collision_side()
                
def main():
    player_sprites = pygame.sprite.Group()
    player = Player(100, 100, 32, 32)
    player_sprites.add(player)
    
    ground_sprites = pygame.sprite.Group()
    terrain = create_terrain()
    for block in terrain:
        ground_sprites.add(block)
    
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
        if key[pygame.K_a]:
            player.move_left(10)
        if key[pygame.K_SPACE] and player.jump_count == 0:
            player.jump()
            
        if not True in key:
            player.idle()

        handle_collisions(player, ground_sprites)
        handle_horizontal_collisions(player, ground_sprites)
        ground_sprites.update()
        player_sprites.update()
        draw_win(player_sprites, ground_sprites)
    pygame.quit()

if __name__ == "__main__":
    main()