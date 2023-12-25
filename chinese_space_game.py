import pygame
from sys import exit
import random
from dictionary import words, word_list
"""
Maybe a rocket heading towards USsss
"""
pygame.init() #starts pygame

def place_word(words, word_list, font):
    word_list = word_list[:]

    magic_choice = random.choice(word_list)
    word_list.remove(magic_choice)
    bum_choice1 = random.choice(word_list)
    word_list.remove(bum_choice1)
    bum_choice2 = random.choice(word_list)
    word_list.remove(bum_choice2)

    rand_choices = []
    x=0
    for choice in [magic_choice, bum_choice1, bum_choice2]:
        rand_choices.insert(random.randint(0, len(rand_choices)), words[choice])
        x += 1

    print(rand_choices)
    print(words[magic_choice])
    for i, choice in enumerate(rand_choices):
        if choice == words[bum_choice1]:
            x_pos1 = i
        elif choice == words[bum_choice2]:
            x_pos2 = i
    return(magic_choice, rand_choices, x_pos1, x_pos2)

def spawn_lasers(pos1, pos2):
    if pos1 == 0:
        a = 50
    elif pos1 == 1:
        a = 183
    else:
        a = 316

    if pos2 == 0:
        b = 50
    elif pos2 == 1:
        b = 183
    else:
        b = 316

    laser_surf1 = pygame.Surface((133.33, 800))
    laser_rect1 = laser_surf1.get_rect(center = (a,-1600))
    laser_surf2 = pygame.Surface((133.33, 800))
    laser_rect2 = laser_surf2.get_rect(center=(b, -1600))
    return([laser_surf1,laser_rect1,laser_surf2,laser_rect2])


word_font = pygame.font.Font(None, 50)
char_font = pygame.font.Font("chinese.stsong.ttf", 50)
screen = pygame.display.set_mode((400, 800)) #initializes display window
pygame.display.set_caption("Chinese Space Game")
clock = pygame.time.Clock() #initializes clock object
word_timer = pygame.USEREVENT + 1
pygame.time.set_timer(word_timer,5000)

player_surf = pygame.Surface((15, 15))
player_rect = player_surf.get_rect(center = (200,700))

magic_word = ""
rand_chars = []
lasers = []
move_left = False
move_right = False
while True:
    for event in pygame.event.get(): #gets all possible events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            move_left = False
            move_right = False
        if event.type == word_timer:
            magic_word, rand_chars, x_pos1, x_pos2 = place_word(words, word_list, word_font)
            print(x_pos1, x_pos2)
            lasers = spawn_lasers(x_pos1, x_pos2)
            #print(rand_chars)
            #print(magic_word)

    screen.fill("Blue")

    if move_left:
        if not player_rect.x < 0:
            player_rect.x -= 4
    if move_right:
        if not player_rect.x > 385:
            player_rect.x += 4

    screen.blit(player_surf, player_rect)
    pygame.draw.rect(screen, "Pink", player_rect)
    pygame.draw.polygon(screen, "Red", [(player_rect.centerx-25,player_rect.centery+25),(player_rect.centerx,player_rect.centery-25),(player_rect.centerx + 25,player_rect.centery+25)])

    word_surf = word_font.render(magic_word, False, "Black")
    word_rect = word_surf.get_rect(center=(200, 400))
    screen.blit(word_surf, word_rect)

    x = 50
    if rand_chars:
        for char in rand_chars:
            screen.blit(char_font.render(char, False, "Black"), (x, 60))
            x += 133
        x = 50

    if lasers:
        screen.blit(lasers[0], lasers[1])
        screen.blit(lasers[2], lasers[3])
        lasers[1].y += 10
        lasers[3].y += 10
        if lasers[1].colliderect(player_rect) or lasers[3].colliderect(player_rect):
             pygame.quit()
             exit()
    pygame.display.update() #updates pygame
    clock.tick(60) #this loop does not runnen faster than 60 frames