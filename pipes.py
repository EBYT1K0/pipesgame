import pygame
import pathlib

def draw_pipe(screen, w, h, atlas, visited): # checks each value in atlas and draws the pipes accordingly
    x = 0
    y = 0
    y2 = 0
    for i in atlas:
        x = 0
        x2 = 0  # FIX: Reset x2 to 0 at the start of every row!
        for j in i: 
            if [y2,x2] in visited:
                pygame.draw.rect(screen, BLUE, (x + w//3, y + h//3, w//3, h//3))
            if j[0]: # up
                if [y2,x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3, y, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + w//3, y), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y), (x + 2*w//3, y + h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w//3, y + h//3), 4)
            if j[1]: # down
                if [y2,x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3, y + 2*h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            if j[2]: # left
                if [y2,x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x, y + h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x, y + h//3), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h//3), 4)
            if j[3]: # right
                if [y2,x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + 2*w//3, y + h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h//3), 4)
            x += w
            x2 += 1
        y2 += 1
        y += h

def levelgrid(screen, x, y, w, h, rows, cols): # draws a grid
    font = pygame.font.SysFont(None, 100)
    cell_width = w // cols
    cell_height = h // rows
    mouse_pos = pygame.mouse.get_pos()
    k = 1
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, WHITE, cell_rect)
            pygame.draw.rect(screen, BLACK, cell_rect, 1)
            screen.blit(font.render(str(k), True, BLACK), (x + j * cell_width + cell_width//2 - font.size(str(k))[0]//2, y + i * cell_height + cell_height//2 - font.size(str(k))[1]//2))
            k += 1

def selection(screen, x, y, w, h, rows, cols): # shows a selection box around the cell the mouse is hovering over, and returns the coordinates of the cell when clicked
    cell_width = w // cols
    cell_height = h // rows
    mouse_pos = pygame.mouse.get_pos()
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            if cell_rect.collidepoint(mouse_pos):
                try:
                    pygame.draw.rect(screen, BLUE, cell_rect, 4)

                    if pygame.mouse.get_pressed()[0]: # left click
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # left click release
                                    waiting = False
                                    #print(f"Clicked cell: ({i}, {j})")
                                    return (i, j)
                    else:
                        return (None, None)
                except:
                    return (None, None)
    return (None, None)
                
def rotation(atlas, x, y): #rotates the pipe by 90 degrees clockwise
    if (x, y) == (None, None) or atlas[x][y] == [False, False, False, False] or atlas[x][y] == [True, True, True, True]:
        return atlas[x][y]
    else:
        newatlas = atlas[x][y]
        if atlas[x][y] == [True, False, False, False]: 
            newatlas = [False, False, False, True]
        if atlas[x][y] == [False, True, False, False]:
            newatlas = [False, False, True, False]
        if atlas[x][y] == [False, False, True, False]:
            newatlas = [True, False, False, False]
        if atlas[x][y] == [False, False, False, True]:
            newatlas = [False, True, False, False]
        if atlas[x][y] == [True, False, True, False]:
            newatlas = [True, False, False, True]
        if atlas[x][y] == [False, True, True, False]:
            newatlas = [True, False, True, False]
        if atlas[x][y] == [False, True, False, True]:
            newatlas = [False, True, True, False]
        if atlas[x][y] == [True, False, False, True]:
            newatlas = [False, True, False, True]
        if atlas[x][y] == [True, True, False, False]:
            newatlas = [False, False, True, True]
        if atlas[x][y] == [False, False, True, True]:
            newatlas = [True, True, False, False]
        if atlas[x][y] == [False, True, True, True]:
            newatlas = [True, True, True, False]
        if atlas[x][y] == [True, False, True, True]:
            newatlas = [True, True, False, True]
        if atlas[x][y] == [True, True, False, True]:
            newatlas = [False, True, True, True]
        if atlas[x][y] == [True, True, True, False]:
            newatlas = [True, False, True, True]
        return newatlas
    
def filledpipes(atlas, sourcex, sourcey): # checks if the water can flow from the source to all pipes
    visited = []
    def flow(x, y):
        if [x, y] not in visited:
            visited.append([x, y])
            if atlas[x][y][0] and x > 0 and atlas[x-1][y][1]: # up
                flow(x-1, y)
            if atlas[x][y][1] and x < rows-1 and atlas[x+1][y][0]: # down
                flow(x+1, y)
            if atlas[x][y][2] and y > 0 and atlas[x][y-1][3]: # left
                flow(x, y-1)
            if atlas[x][y][3] and y < cols-1 and atlas[x][y+1][2]: # right
                flow(x, y+1)
    flow(sourcex, sourcey)
    return visited

def checkwin(atlas, visited): # checks if all pipes are filled with water
    for i in range(rows):
        for j in range(cols):
            if atlas[i][j] != [False, False, False, False] and [i, j] not in visited:
                return False
    return True

lines = []
atlas = []
level = "level1"
level += ".txt"

file_path = pathlib.Path(__file__).parent / "levels" / level
with open(file_path, "r") as file:
    for line in file:
        lines.append(line.strip())
    rowsandcols = lines[0]
    rowstring = rowsandcols[0:2]
    colstring = rowsandcols[3:5]
    rows = int(rowstring)
    cols = int(colstring)
    source = lines[1]
    sourcex = int(source[0:2])
    sourcey = int(source[3:5])
    for i in lines[2:rows+3]:
        row = []
        for j in i.split(","):
            if j == "0":
                row.append([False, False, False, False])
            
            elif j == "1": # dead end pipes
                row.append([True, False, False, False])
            elif j == "2":
                row.append([False, True, False, False])
            elif j == "3":
                row.append([False, False, True, False])
            elif j == "4":
                row.append([False, False, False, True])
            
            elif j == "5": # turn pipes
                row.append([True, False, True, False])
            elif j == "6":
                row.append([False, True, False, True])
            elif j == "7":
                row.append([False, True, True, False])
            elif j == "8":
                row.append([True, False, False, True])
            
            elif j == "9": # straight pipes
                row.append([True, True, False, False])
            elif j == "A":
                row.append([False, False, True, True])
            
            elif j == "B": # three way pipes
                row.append([False, True, True, True])
            elif j == "C":
                row.append([True, False, True, True])
            elif j == "D":
                row.append([True, True, False, True])
            elif j == "E":
                row.append([True, True, True, False])
            
            elif j == "F":
                row.append([True, True, True, True])
        atlas.append(row)
        



WHITE = (255, 255, 255)
BLUE = (0, 195, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 900, 900


# atlas = [
#     [[True, False, False, False], [False, True, False, False], [True, False, True, False], [False, False, False, True]],
#     [[True, False, True, False], [False, True, True, False], [False, True, True, True], [True, False, False, True]],
#     [[True, False, False, False], [False, False, True, True], [False, True, True, False], [True, False, True, False]],
#     [[False, True, False, True], [True, False, True, True], [True, True, False, False], [False, True, True, False]]
# ] #[up, down, left, right] bools

scene = "menu"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pipes")
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                scene = "menu"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                level = input("Enter level name: ")
                try:
                    with open(pathlib.Path(__file__).parent / "levels" / f"{level}.txt", "r") as file:
                        lines = []
                        atlas = []
                        for line in file:
                            lines.append(line.strip())
                        rowsandcols = lines[0]
                        rowstring = rowsandcols[0:2]
                        colstring = rowsandcols[3:5]
                        rows = int(rowstring)
                        cols = int(colstring)
                        source = lines[1]
                        sourcex = int(source[0:2])
                        sourcey = int(source[3:5])
                        for i in lines[2:rows+3]:
                            row = []
                            for j in i.split(","):
                                if j == "0":
                                    row.append([False, False, False, False])
                                
                                elif j == "1": # dead end pipes
                                    row.append([True, False, False, False])
                                elif j == "2":
                                    row.append([False, True, False, False])
                                elif j == "3":
                                    row.append([False, False, True, False])
                                elif j == "4":
                                    row.append([False, False, False, True])
                                
                                elif j == "5": # turn pipes
                                    row.append([True, False, True, False])
                                elif j == "6":
                                    row.append([False, True, False, True])
                                elif j == "7":
                                    row.append([False, True, True, False])
                                elif j == "8":
                                    row.append([True, False, False, True])
                                
                                elif j == "9": # straight pipes
                                    row.append([True, True, False, False])
                                elif j == "A":
                                    row.append([False, False, True, True])
                                
                                elif j == "B": # three way pipes
                                    row.append([False, True, True, True])
                                elif j == "C":
                                    row.append([True, False, True, True])
                                elif j == "D":
                                    row.append([True, True, False, True])
                                elif j == "E":
                                    row.append([True, True, True, False])
                                
                                elif j == "F":
                                    row.append([True, True, True, True])
                            atlas.append(row)
                    scene = "level"
                except FileNotFoundError:
                    pass
    #grid(screen, 0, 0, WIDTH, HEIGHT, 4, 4)
    if scene == "level":
        x, y = selection(screen, 0, 0, WIDTH, HEIGHT, rows, cols)
        if x is not None and y is not None:
            atlas[x][y] = rotation(atlas, x, y)
        visited = filledpipes(atlas, sourcex, sourcey)
        
        # FIX: Changed WIDTH // rows -> WIDTH // cols AND HEIGHT // cols -> HEIGHT // rows
        draw_pipe(screen, WIDTH // cols, HEIGHT // rows, atlas, visited)
        
        if checkwin(atlas, visited):
            font = pygame.font.SysFont(None, 100)
            text = font.render("You win!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


    if scene == "menu":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Choose level", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 25))
        levelgrid(screen, 100, 100, WIDTH-200, HEIGHT-200, 4, 4)
        x,y = selection(screen, 100, 100, WIDTH-200, HEIGHT-200, 4, 4)
        if x is not None and y is not None:
            try:
                with open(pathlib.Path(__file__).parent / "levels" / f"level{x*4+y+1}.txt", "r") as file:
                    lines = []
                    atlas = []
                    for line in file:
                        lines.append(line.strip())
                    rowsandcols = lines[0]
                    rowstring = rowsandcols[0:2]
                    colstring = rowsandcols[3:5]
                    rows = int(rowstring)
                    cols = int(colstring)
                    source = lines[1]
                    sourcex = int(source[0:2])
                    sourcey = int(source[3:5])
                    for i in lines[2:rows+3]:
                        row = []
                        for j in i.split(","):
                            if j == "0":
                                row.append([False, False, False, False])
                            
                            elif j == "1": # dead end pipes
                                row.append([True, False, False, False])
                            elif j == "2":
                                row.append([False, True, False, False])
                            elif j == "3":
                                row.append([False, False, True, False])
                            elif j == "4":
                                row.append([False, False, False, True])
                            
                            elif j == "5": # turn pipes
                                row.append([True, False, True, False])
                            elif j == "6":
                                row.append([False, True, False, True])
                            elif j == "7":
                                row.append([False, True, True, False])
                            elif j == "8":
                                row.append([True, False, False, True])
                            
                            elif j == "9": # straight pipes
                                row.append([True, True, False, False])
                            elif j == "A":
                                row.append([False, False, True, True])
                            
                            elif j == "B": # three way pipes
                                row.append([False, True, True, True])
                            elif j == "C":
                                row.append([True, False, True, True])
                            elif j == "D":
                                row.append([True, True, False, True])
                            elif j == "E":
                                row.append([True, True, True, False])
                            
                            elif j == "F":
                                row.append([True, True, True, True])
                        atlas.append(row)
                scene = "level"
            except FileNotFoundError:
                pass
    pygame.display.update()

pygame.quit()
