import pygame, sys
import random

WHITE = (255, 255, 255)
BLACK = (60, 60, 60)
GREEN = (102, 255, 102)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HEADER = 50

pygame.init()
screen = pygame.display.set_mode((950, 950))
pygame.display.set_caption("Mã Đi Tuần")
running = True
clock = pygame.time.Clock()

def font(size):
    return pygame.font.SysFont('arial', size)

class Cell:
    def __init__(self, size, color, i, j):
        self.size = size
        self.color = color
        self.i = i
        self.j = j

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.j*self.size+HEADER, self.i*self.size+HEADER, self.size, self.size))
        pygame.display.update()

    def ableMove(self):
        pygame.draw.rect(screen, RED, (self.j*self.size+HEADER, self.i*self.size+HEADER, self.size, self.size))

class Matrix:
    def __init__(self, col, row, size):
        self.col = col
        self.row = row
        self.L = [[None for i in range(col)] for j in range(row)]
        self.visited = [[False for i in range(col)] for j in range(row)]
        self.start = None
        for i in range(row):
            for j in range(col):
                if (i + j) % 2 == 0:
                    self.L[i][j] = Cell(size//col, WHITE, i, j)
                else:
                    self.L[i][j] = Cell(size//col, BLACK, i, j)
    
    def draw(self):
        for i in range(self.row):
            for j in range(self.col):
                self.L[i][j].draw()
        for i in range(self.col):
            sur = pygame.draw.rect(screen, WHITE, (i*100+HEADER, 0, 100, 50))
            text = pygame.font.Font.render(font(50), '{}'.format(i), True, BLACK)
            sur_text = text.get_rect()
            sur_text.center = sur.center
            screen.blit(text, sur_text)
        
        for i in range(self.row):
            sur = pygame.draw.rect(screen, WHITE, (0, i*100+HEADER, 50, 100))
            text = pygame.font.Font.render(font(50), '{}'.format(i), True, BLACK)
            sur_text = text.get_rect()
            sur_text.center = sur.center
            screen.blit(text, sur_text)
        for i in range(self.col):
            pygame.draw.line(screen, BLACK, (0, i*100 + 50), (850, i*100 + 50), 2)
            pygame.draw.line(screen, BLACK, (i*100 + 50, 0), (i*100 + 50, 850), 2)

        sur = pygame.draw.rect(screen, GREEN, (0, 852, 950, 100))
        text = "Knight's tour"
        text = pygame.font.Font.render(font(50), text, True, BLACK)
        sur_text = text.get_rect()
        sur_text.center = sur.center
        screen.blit(text, sur_text)

        pygame.draw.line(screen, BLACK, (0, 50-2), (850, 50-2), 2)
        pygame.draw.line(screen, BLACK, (50-2, 0), (50-2, 850), 2)
        pygame.display.update()
    
    def reset(self):
        for i in range(self.row):
            for j in range(self.col):
                self.L[i][j].draw()
        self.visited = [[False for i in range(self.col)] for j in range(self.row)]
        return Horse(self.start[0], self.start[1], 100)


class Horse:
    def __init__(self, i, j, size):
        self.i = i
        self.j = j
        self.size = size
        self.img = pygame.image.load('./KnightTour/horse.png')
    
    def draw(self):
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        screen.blit(self.img, (self.j*self.size+HEADER, self.i*self.size+HEADER))
        pygame.display.update()
        # pygame.display.flip()
    
    @staticmethod
    def listAblemove(i, j, matrix: Matrix):
        ds = []
        if i-2 >= 0 and j-1>=0 and matrix.visited[i-2][j-1] == False:
            ds.append((i-2,j-1))
        if i-2 >= 0 and j+1<=7 and matrix.visited[i-2][j+1] == False:
            ds.append((i-2,j+1))
        if i+2 <= 7 and j-1>=0 and matrix.visited[i+2][j-1] == False:
            ds.append((i+2,j-1))
        if i+2 <= 7 and j+1<=7 and matrix.visited[i+2][j+1] == False: 
            ds.append((i+2,j+1))
        if i-1 >= 0 and j-2 >= 0 and matrix.visited[i-1][j-2] == False:
            ds.append((i-1,j-2))
        if i+1 <= 7 and j-2 >= 0 and matrix.visited[i+1][j-2] == False:
            ds.append((i+1,j-2))
        if i-1 >= 0 and j+2 <= 7 and matrix.visited[i-1][j+2] == False:
            ds.append((i-1,j+2))
        if i+1 <= 7 and j+2 <= 7 and matrix.visited[i+1][j+2] == False:
            ds.append((i+1,j+2))
        return ds

    def ableMove(self, matrix):
        ds = Horse.listAblemove(self.i, self.j, matrix)
        # print(ds)
        for (i, j) in ds:
            matrix.L[i][j].ableMove()

    def move(self, i, j, matrix, number):
        ds = Horse.listAblemove(self.i, self.j, matrix)
        matrix.L[self.i][self.j].draw()
        text = pygame.font.Font.render(font(50), '{}'.format(number), True, (255, 10, 10))
        screen.blit(text, (self.j*100+HEADER, self.i*100+HEADER, 100, 100))
        if (i, j) in ds:
            self.i = i
            self.j = j
            self.draw()

class Button:
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.surface = pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))
        
    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.w, self.h), width=10)
        text = pygame.font.Font.render(font(30), self.text, True, BLUE)
        sur_text = text.get_rect()
        sur_text.center = self.surface.center
        screen.blit(text, sur_text)
    
    def hover(self):
        x, y = pygame.mouse.get_pos()
        if self.surface.collidepoint(x, y):
            self.surface = pygame.draw.rect(screen, WHITE, (self.x, self.y, self.w, self.h))
        else:
            self.surface = pygame.draw.rect(screen, RED, (self.x, self.y, self.w, self.h))

    def click(self):
        x, y = pygame.mouse.get_pos()
        if self.surface.collidepoint(x, y):
            return True
        return False

def Algo(matrix: Matrix, horse: Horse):
    cnt = 1
    matrix.visited[horse.i][horse.j] = True
    while cnt < 64:
        pygame.event.pump()
        clock.tick(2)
        # pygame.time.wait(500)
        ds = Horse.listAblemove(horse.i, horse.j, matrix)
        random.shuffle(ds)
        tmp = dict()
        for (i, j) in ds:
            tmp[len(Horse.listAblemove(i, j, matrix))] = (i, j)
        n = min(list(tmp.keys()))
        (i, j) = tmp[n]
        # horse.ableMove()
        horse.move(i, j, matrix, cnt)
        matrix.visited[horse.i][horse.j] = True
        cnt += 1
    return (horse.i, horse.j)

button_reset = Button(850, 0, 100, 475, 'Reset')
button_run = Button(850, 475, 100, 475, 'Run')
button_reset.draw()
button_run.draw()
m = Matrix(8, 8, 800)
horse = None
ableMove = False
m.draw()
# pygame.display.update()
arr = dict()
while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            sys.exit(0)
        
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= HEADER and x < 850 and y >= HEADER and y < 850:
                i = (y-HEADER)//100
                j = (x-HEADER)//100
                if horse != None:
                    m.L[horse.i][horse.j].draw()
                horse = Horse(i, j, 100)
                m.start = (i, j)
            if button_reset.click():
                try:
                    horse = m.reset()
                except:
                    pass
            if button_run.click():
                try:
                    pygame.event.pump()
                    print(Algo(m, horse))
                except:
                    pass
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                try:
                    pygame.event.pump()
                    Algo(m, horse)
                except:
                    pass
            if e.key == pygame.K_UP:
                horse = m.reset()

    button_reset.hover()
    button_reset.draw()
    button_run.hover()
    button_run.draw()
    if horse != None:
        horse.draw()
    
    pygame.display.update()
pygame.quit()