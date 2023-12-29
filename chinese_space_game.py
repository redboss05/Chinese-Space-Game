import pygame
from sys import exit
import random
from dictionary import words, word_list
from stars import star_list
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
        rand_choices.insert(random.randint(0, len(rand_choices)), words[choice][0])
        x += 1

    rand_words = []
    for rand_choice in rand_choices:
        for choice in [magic_choice, bum_choice1, bum_choice2]:
            if rand_choice == words[choice][0]:
                rand_words.append(words[choice][1])

    for i, choice in enumerate(rand_choices):
        if choice == words[bum_choice1][0]:
            x_pos1 = i
        elif choice == words[bum_choice2][0]:
            x_pos2 = i
    return(magic_choice, rand_choices, x_pos1, x_pos2, rand_words)

def stars(spawned, star_list):
    if spawned == False:
        for star in star_list:
            star.append(star[0].get_rect(center=(random.randrange(400),random.randrange(-100,800))))
    for star in star_list:
        screen.blit(star[0],star[1])
        pygame.draw.rect(screen, "White", star[1])
        star[1].y += 10
        if star[1].y > 800:
            star[1].x = random.randrange(400)
            star[1].y = random.randrange(-200,0)

def spawn_lasers(pos1, pos2):
    if pos1 == 0:
        a = 65
    elif pos1 == 1:
        a = 190
    else:
        a = 335

    if pos2 == 0:
        b = 65
    elif pos2 == 1:
        b = 190
    else:
        b = 335

    laser_surf1 = pygame.Surface((145, 800))
    laser_rect1 = laser_surf1.get_rect(center = (a,-1600))
    laser_surf2 = pygame.Surface((145, 800))
    laser_rect2 = laser_surf2.get_rect(center=(b, -1600))
    return([laser_surf1,laser_rect1,laser_surf2,laser_rect2])


word_font = pygame.font.Font(None, 50)
char_font = pygame.font.Font("chinese.stsong.ttf", 50)
pronounced_font = pygame.font.Font(None, 25)
screen = pygame.display.set_mode((400, 800)) #initializes display window
pygame.display.set_caption("Rocket Chinese")
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
spawned = False
game_running = False
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
        if event.type == pygame.KEYDOWN:
            game_running = True
        if event.type == pygame.KEYUP:
            move_left = False
            move_right = False
        if event.type == word_timer:
            if game_running:
                magic_word, rand_chars, x_pos1, x_pos2, rand_words = place_word(words, word_list, word_font)
                lasers = spawn_lasers(x_pos1, x_pos2)
                #print(rand_chars)
                #print(magic_word)

    screen.fill("Black")
    stars(spawned, star_list)

    if game_running == True:

        if move_left:
            if not player_rect.x < 0:
                player_rect.x -= 4
        if move_right:
            if not player_rect.x > 385:
                player_rect.x += 4

        screen.blit(player_surf, player_rect)
        pygame.draw.rect(screen, "Pink", player_rect)
        pygame.draw.polygon(screen, "White", [(player_rect.centerx-25,player_rect.centery+25),(player_rect.centerx,player_rect.centery-25),(player_rect.centerx + 25,player_rect.centery+25)])

        word_surf = word_font.render(magic_word, False, "White")
        word_rect = word_surf.get_rect(center=(200, 400))
        screen.blit(word_surf, word_rect)

        #stars(spawned, star_list)
        #spawned = True

        x = 50
        if rand_chars:
            for i, char in enumerate(rand_chars):
                char_surf = char_font.render(char, False, "White")
                char_rect = char_surf.get_rect(center=(x,60))
                pronounced_surf = pronounced_font.render(rand_words[i], False, "White")
                pronounced_rect = pronounced_surf.get_rect(center=(x, 30))
                screen.blit(char_surf,char_rect)
                screen.blit(pronounced_surf,pronounced_rect)
                x += 150

        if lasers:
            screen.blit(lasers[0], lasers[1])
            pygame.draw.rect(screen, "Red", lasers[1])
            screen.blit(lasers[2], lasers[3])
            pygame.draw.rect(screen, "Red", lasers[3])
            lasers[1].y += 10
            lasers[3].y += 10
            if lasers[1].colliderect(player_rect) or lasers[3].colliderect(player_rect):
                 game_running = False
                 lasers[1].x = 1000
                 lasers[3].x = 1000
                 magic_word = None
                 for char in rand_chars[:]:
                     rand_chars.remove(char)
                 print(rand_chars)

    else:

        title_surf = word_font.render("Rocket Chinese", False, "White")
        title_rect = title_surf.get_rect(center=(200, 50))
        screen.blit(title_surf, title_rect)

        subtext_surf = pronounced_font.render("press any button to start", False, "White")
        subtext_rect = subtext_surf.get_rect(center=(200, 100))
        screen.blit(subtext_surf, subtext_rect)

        pygame.draw.polygon(screen, "White", [(player_rect.centerx - 25, player_rect.centery + 25),
                                              (player_rect.centerx, player_rect.centery - 25),
                                              (player_rect.centerx + 25, player_rect.centery + 25)])



    pygame.display.update() #updates pygame
    clock.tick(60) #this loop does not runnen faster than 60 frames