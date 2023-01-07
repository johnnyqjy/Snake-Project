#Imports & Inits
import pygame
import random
import time
import os

#This should solve the sound lagging problem?
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

#Setting up game window
screen_dimensions = (400, 400)
screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption("Super-powered Snake")

#initial score
score = 0

# sound effects
apple_bite = pygame.mixer.Sound(os.path.join('Game_Assets','Apple_Crunch.wav'))
game_over_sound = pygame.mixer.Sound(os.path.join('Game_Assets','death.wav'))
bgm = pygame.mixer.Sound(os.path.join('Game_Assets','game_music1.wav'))

#defining basic colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

#load images
apple = pygame.image.load(os.path.join('Game_Assets','apple_regular_30_30px.png'))
apple = pygame.transform.scale(apple,(10,10))
pois_apple = pygame.image.load(os.path.join('Game_Assets','apple_rotten_30_30px.png'))
pois_apple = pygame.transform.scale(pois_apple,(10,10))
snake_head = pygame.image.load(os.path.join('Game_Assets','head_up.png'))
snake_head = pygame.transform.rotate(pygame.transform.scale(snake_head,(10,10)),90)#since it's initially facing upwards, we need to rotate it
#horizontal
snake_body = pygame.image.load(os.path.join('Game_Assets','body_horizontal.png'))
snake_body = pygame.transform.scale(snake_body,(10,10))
#vertical
snake_body_v = pygame.image.load(os.path.join('Game_Assets','body_vertical.png'))
snake_body_v = pygame.transform.scale(snake_body_v,(10,10))

#Sets snake starter position and movement
vt_movement = 0  #Insert Code for Snake initial vertical movement
hz_movement = 10  #Insert Code for Snake initial horizontal movement
snake_x = 50  #Insert Code for Snake starting x position
snake_y = 50  #Insert Code for Snake starting y position

#Pre-Generates apple location
#we don't want the food to spawn on the edge
food_x = random.randrange(10, screen.get_width()) // 10 * 10
food_y = random.randrange(10, screen.get_height()) // 10 * 10
food = apple.get_rect()
food.x,food.y = food_x,food_y

#Pre-generates poisonous apple location
def spawn_more_pois(food_x,food_y):
  '''
  This function considers the current apple location and spawns   
  poisonous apples elsewhere
  '''
  pois_x = random.randrange(0, screen.get_width()) // 10 * 10
  pois_y = random.randrange(0, screen.get_height()) // 10 * 10
  #make sure apple and poisonous apple don't stack
  while pois_x == food_x and pois_y == food_y:
    pois_x = random.randrange(0, screen.get_width()) // 10 * 10
    pois_y = random.randrange(0, screen.get_height()) // 10 * 10

  return pois_x, pois_y

pois_apple_list = []
location_list = []
for _ in range(3): #the number of poisonous apples we want/difficulty level
  pois_x,pois_y = spawn_more_pois(food_x,food_y)
  pois = pois_apple.get_rect()
  pois.x,pois.y = pois_x,pois_y
  location_list.append((pois_x,pois_y))
  pois_apple_list.append(pois)

snake_segments = [(snake_x, snake_y)]
# the snake_head image does not look good, so I decided to not use it
head = snake_head.get_rect()
head.x, head.y = snake_x,snake_y
# head = pygame.Rect(snake_segments[0][0], snake_segments[0][1], 10,10)  

# I was thinking of increasing poisonous apples as the game goes on.
# if score != 0 and score % 5 == 0:
#       new_pois_x, new_pois_y = spawn_more_pois(food_x,food_y)
#       pygame.draw.rect(screen, black, [new_pois_x,new_pois_y, 10, 10])

def apples(x, y):
    '''
  Function to generate new apples after current one is eaten.

  Inputs:
  x: x value of the current apple
  y: y value of the current apple

  Outputs:
  food_x: x value of the new apple
  food_y: y value of the new apple
  '''
    #we don't want the food to spawn on the edges, so the range starts at 10
    while ((x, y) in snake_segments):
        x = random.randrange(10, screen.get_width()) // 10 * 10
        y = random.randrange(10, screen.get_height()) // 10 * 10

    return x, y
  
def show_score(choice, color, font, size):
  '''
  Function to display game score on the screen
  ''' 
  score_font = pygame.font.SysFont(font, size)
   
  score_surface = score_font.render('Score : ' + str(score), True, color)
   
  score_rect = score_surface.get_rect()
   
  screen.blit(score_surface, score_rect)

def display_endscore():
   
    my_font = pygame.font.SysFont('times new roman', 20)
     
    game_over_surface = my_font.render(
        'Game Over! Your Score is: ' + str(score), True, red)
     
    game_over_rect = game_over_surface.get_rect()
     
    game_over_rect.midtop = (screen_dimensions[0]/2, screen_dimensions[1]/2)
     
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
     
    time.sleep(5) #delay

def game_over():
    '''
  Checks for all possible ways the snake could die and ends the program if one is true
    1. Snake runs off edge of screen
    2. Snake hits its own body (HINT: DON'T USE RECTANGLE COLLISIONS FOR THIS)
  No Inputs/Outputs
  '''
    # check if head is outside of boundaries
    for body in snake_segments[:-1]: #the last element in snake_segments is the head
      if body == (head[0],head[1]):
        bgm.stop()
        game_over_sound.play()
        display_endscore()
        pygame.quit()
        quit()
      
    # # Checks if snake runs off of screen
    # if (head.left < -10 or head.right > (screen.get_width()+10) or head.top < -10 or head.bottom >    (screen.get_height()+10)):
    #   bgm.stop()
    #   game_over_sound.play()
    #   display_endscore()
    #   pygame.quit()
    #   quit()

    # this works better than the one above
    for segment in snake_segments[::-1]:
      if segment[0] < 0 or segment[0] > screen_dimensions[0]:
        bgm.stop()
        game_over_sound.play()
        display_endscore()
        pygame.quit()
        quit()
      if segment[1] < 0 or segment[1] > screen_dimensions[1]:
        bgm.stop()
        game_over_sound.play()
        display_endscore()
        pygame.quit()
        quit()


bgm.play(-1) # this plays indefinitely until we stop it
while True:
    screen.fill(black)
    #Draws apple
    screen.blit(apple, food)
    #Draws bad apples
    for x in pois_apple_list:
      screen.blit(pois_apple, x)
    

    #Snake movement
    snake_x = snake_x + hz_movement
    snake_y = snake_y + vt_movement

    #Draws snake
    for (a, b) in snake_segments:
        if hz_movement != 0:
          body = snake_body.get_rect()
          body.x, body.y = a,b
          screen.blit(snake_body,body)
        else:
          body = snake_body_v.get_rect()
          body.x, body.y = a,b
          screen.blit(snake_body_v,body)
    
    head = snake_head.get_rect()
    head.x,head.y = snake_segments[-1][0], snake_segments[-1][1]
    screen.blit(snake_head,head)
    
    #Appends new snake pos.
    snake_segments.append((snake_x,snake_y))

    #Remakes food (apple) and head(front on snake) variables
    food = pygame.Rect(food_x, food_y, 10, 10)
    head = pygame.Rect(snake_segments[-1][0], snake_segments[-1][1], 10, 10) 
    if pygame.Rect.colliderect(head, food):
        apple_bite.play(loops=0, maxtime=0, fade_ms=0)
        score += 1
        food_x, food_y = apples(food_x,food_y)  #Generates new position for food  
    else:
        del snake_segments[0]  #Deletes old position
      
    for x in pois_apple_list:
      if pygame.Rect.colliderect(head, x):
        bgm.stop()
        game_over_sound.play()
        display_endscore()
        pygame.quit()
        quit()
    
    game_over()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            #added wasd movment controls as well
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if hz_movement != 10:
                  hz_movement = -10
                  vt_movement = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
              if hz_movement != -10:
                  hz_movement = 10
                  vt_movement = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if vt_movement != 10:
                  hz_movement = 0
                  vt_movement = -10
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if vt_movement != -10:
                  hz_movement = 0
                  vt_movement = 10 
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
          
    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    clock.tick(10)