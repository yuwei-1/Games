import pygame
import random

pygame.init()
pygame.font.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

font_style = pygame.font.SysFont('Arial',20)


def message(msg, color): #function for displaying messages to player
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [20, 20])

def dis_score(score, color): #displaying the score
    ur_score = font_style.render('score: ' + str(score), True, color)
    dis.blit(ur_score, [500,500])

dis_dim = 600 #dimensions of the game screen

dis=pygame.display.set_mode((dis_dim, dis_dim))
pygame.display.set_caption('Snake game by Yuwei Zhu') #window caption
pygame.display.update()

def game_loop(): #main game loop
    grow = False
    snake_line = []
    score = 0

    x = dis_dim/2
    y = dis_dim/2
    x_move = 0
    y_move = 0

    clock = pygame.time.Clock()

    snake_block = 20
    snake_speed = 15

    game_close = False
    game_over = False

    foodx = 40
    foody = 40

    while not game_over:
        while game_close == True:
            dis.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", blue)
            pygame.display.update()
 
            for event in pygame.event.get(): #keys that control whether the user plays again
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN: #Snake controlled by arrow keys
                if event.key == pygame.K_LEFT:
                    x_move = -snake_block
                    y_move = 0
                elif event.key == pygame.K_RIGHT:
                    x_move = snake_block
                    y_move = 0
                elif event.key == pygame.K_UP:
                    x_move = 0
                    y_move = -snake_block
                elif event.key == pygame.K_DOWN:
                    x_move = 0
                    y_move = snake_block
        if x <= 0 or x >= dis_dim or y < 0 or y >=dis_dim:
            game_close = True



        x += x_move
        y += y_move

    # recording movements of snake
        snake_bod = []
        snake_bod.append(x)
        snake_bod.append(y)
        snake_line.append(snake_bod)

        rep = 0
        dis.fill(white)

        for i in snake_line: #Creating the snake
            pygame.draw.rect(dis, blue, [i[0], i[1], snake_block, snake_block])
            rep += 1
            if i == snake_line[0] and len(snake_line) > 1 and rep > 1:
                game_close = True


# stops the snake growing if the food is not eaten
        if grow is False:
            snake_line.pop(0)

        grow = False

        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        dis_score(score, green)
        pygame.display.update()
        clock.tick(snake_speed)

#creates food if original food is eaten
        if x == foodx and y == foody:
            print("nom")
            foodx = random.randrange(1, 20) * 20.0
            foody = random.randrange(1, 25) * 20.0
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
            score = score + 1
            grow = True


    pygame.quit()
    quit()
game_loop()
