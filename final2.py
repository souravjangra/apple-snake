import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
orange = (255,165,0)
red = (255,0,0)
green = (0,155,0)
yellow = (255,255,0)
light_red = (255,160,122)
light_green = (144,238,144)
light_yellow = (255,255,224)

display_width = 800
display_height  = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game')

icon = pygame.image.load('applenew.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snake_head.png')
appleimg = pygame.image.load('applenew.png')
wallimg = pygame.image.load('snake5.png').convert()

clock = pygame.time.Clock()

AppleThickness = 30
block_size = 20
FPS = 15

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def intro(clock):
    gameDisplay.blit(wallimg,[0,0])
    pygame.display.update()
    time.sleep(2)

def pause():

    paused = True
    message_to_screen("Paused",
                      black,
                      -100,
                      size="large")

    message_to_screen("Press P to continue or Q to quit.",
                      black,
                      25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # gameDisplay.fill(white)
        
        clock.tick(5)
                    

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0

    return randAppleX,randAppleY

def game_intro():
    
    intro = True
    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
   
        gameDisplay.fill(white)
        # gameDisplay.blit(wallimg,[0,0])
        message_to_screen("Welcome to APPLE SNAKE",
                          green,
                          -100,
                          "medium")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)

        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)

        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)

        message_to_screen("Press P to play, S to pause or Q to quit.",
                          black,
                          180)

        button("PLAY", 300,500,100,50, green, light_green,action = "play")
        # button("MADE BY", 350,500,100,50, yellow, light_yellow,action = "controls")
        button("QUIT", 450,500,100,50, red, light_red,action = "quit")
        # gameDisplay.blit(wallimg,[0,0])
        # time.sleep(2)
        pygame.display.update()
        clock.tick(15)
        
        


def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    if direction == "left":
        head = pygame.transform.rotate(img, 90)

    if direction == "up":
        head = img

    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def button(text, x, y, width, height, inactive_color, active_color,action="None"):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
            
            if action == "controls":
                message_to_screen("Made By : ", orange, 620, 300)
                message_to_screen("Sourav Jangra", black, 600, 350)
                pygame.display.update()
                        
            if action == "play":
                gameLoop()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    global direction
    
    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randAppleGen()
    
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game over",
                              red,
                              y_displace=-50,
                              size="large")
            
            message_to_screen("Press P to play again or Q to quit",
                              black,
                              50,
                              size="medium")
            pygame.display.update()
            

        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_p:
                        gameLoop()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0

                elif event.key == pygame.K_s:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
      

        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white)

        
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        gameDisplay.blit(appleimg, (randAppleX, randAppleY))


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        
        snake(block_size, snakeList)

        score(snakeLength-1)

        
        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:

                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:

                randAppleX,randAppleY = randAppleGen()
                snakeLength += 1

            
            

        
            
        
        

        clock.tick(FPS)
        
    pygame.quit()
    quit()
intro(clock)
game_intro()
gameLoop()