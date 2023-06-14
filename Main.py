import pygame
from sys import exit
from random import randint

pygame.init()

#variaveis
screen = pygame.display.set_mode((2030, 1080))
pygame.display.set_caption("Jogo")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 100)
game_active = False
start_time = 0

#imagens
sky_surface = pygame.image.load('graphics/sky.png').convert()
sky_surface = pygame.transform.scale(sky_surface, (2060, 800))
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_surface = pygame.transform.scale(ground_surface, (2060, 280))
text_surface = test_font.render('Bem vindo ao meu jogo!', False, (64, 64, 64))

end_text_surface = test_font.render('Pixel Runner', False, (64,64,64))
end_text_rect = end_text_surface.get_rect(midbottom = (1030, 120))

other_end_surface = test_font.render('Press to run', False, (64,64,64))
other_end_rect = other_end_surface.get_rect(midbottom = (1030, 1000))


#FUNCTIONS
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (350, 250))
    screen.blit(score_surf, score_rect)
    return current_time
score = 0


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8
            
            if obstacle_rect.bottom == 800:
                screen.blit(snail_surface, obstacle_rect)
            elif obstacle_rect.bottom == 500:
                screen.blit(fly_surface, obstacle_rect)
            
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False
    return True


#score_surface = test_font.render('Score:', False, (64,64,64))
#score_rect = score_surface.get_rect(midbottom = (350, 250))
#Obstacle

obstacle_rect_list = []

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_surface = pygame.transform.scale(snail_surface, (160, 100))
snail_x_position = 1600
snail_y_position = 800


fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_surface = pygame.transform.scale(fly_surface, (160, 100))
fly_rect = fly_surface.get_rect(midbottom = (1700, 500))


text_rect = text_surface.get_rect(midbottom = (1030, 120))


player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (120, 200))
player_rect = player_surface.get_rect(midbottom = (450, 800))

player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 4)
player_stand_rect = player_stand_surface.get_rect(center = (1030, 540))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

player_gravity = 0
#loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.FINGERDOWN and player_rect.bottom == 800:
                player_gravity = -28
        else:
            if event.type == pygame.FINGERDOWN:
                game_active = True
                
                start_time = int(pygame.time.get_ticks()/1000)
        
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(2030, 2400), snail_y_position)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(2030, 2400), 500)))
#GAME
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,800))
        screen.blit(text_surface, text_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 40)
        #screen.blit(score_surface, score_rect)
        score = display_score()
        
        #PLAYER
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 800:
            player_rect.bottom = 800
            
        screen.blit(player_surface, player_rect)
        
        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        
        #Collision
        game_active = collisions(player_rect, obstacle_rect_list)
        #snail_rect.right -= 8
        #if snail_rect.right <= 0:
            #snail_rect.left = 2060
        #screen.blit(snail_surface, snail_rect)
        
            #MENU
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rect)
        
        obstacle_rect_list.clear()
        player_rect.midbottom = (450, 800)
        player_gravity = 0
        
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(midbottom = (1030, 900))
        screen.blit(end_text_surface, end_text_rect)
        if score == 0:
            screen.blit(other_end_surface, other_end_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
