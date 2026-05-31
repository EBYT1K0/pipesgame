import pygame
import pathlib
import random

def draw_pipe(screen, w, h, atlas, sourcex, sourcey): # checks each value in atlas and draws the pipes accordingly
    x = 0
    y = 0
    for i in atlas:
        x = 0
        for j in i: 
            if j[0]: # up
                pygame.draw.line(screen, BLACK, (x + w//3, y), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y), (x + 2*w//3, y + h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w//3, y + h//3), 4)
            if j[1]: # down
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            if j[2]: # left
                pygame.draw.line(screen, BLACK, (x, y + h//3), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h//3), 4)
            if j[3]: # right
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h//3), 4)
            x += w
        y += h

def draw_source(screen, w, h, sourcex, sourcey, atlas):
    # Calculate the top-left pixel position of the source cell directly
    x = sourcex * w
    y = sourcey * h
    
    # Draw the central blue square matching the pipe width
    pygame.draw.rect(screen, BLUE, (x + w//3, y + h//3, w//3, h//3))

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
                                    return (i, j, "left")
                    elif pygame.mouse.get_pressed()[2]: # right click
                        waiting = True
                        while waiting:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP and event.button == 3: # right click release
                                    waiting = False
                                    return (i, j, "right")
                    else:
                        return (None, None, None)
                except:
                    return (None, None, None)
    return (None, None, None)

def rotation(atlas, x, y): # rotates the pipe by 90 degrees clockwise
    if x is None or y is None:
        return [False, False, False, False]
    
    current_pipe = atlas[x][y]
    
    # current_pipe order: [Up, Down, Left, Right]
    # We want new order:  [Left, Right, Down, Up]
    # A simple slice shift accomplishes this:
    up, down, left, right = current_pipe
    return [left, right, down, up]
                
def change_pipe(atlas, x, y):
    if atlas[x][y].count(True) == 0:
        atlas[x][y] = [True, False, False, False]
    elif atlas[x][y].count(True) == 1:
        atlas[x][y] = [True, True, False, False]
    elif atlas[x][y] == [True, True, False, False] or atlas[x][y] == [False, False, True, True]:
        atlas[x][y] = [True, False, True, False]
    elif atlas[x][y].count(True) == 2:
        atlas[x][y] = [True, True, True, False]
    elif atlas[x][y].count(True) == 3:
        atlas[x][y] = [True, True, True, True]
    elif atlas[x][y].count(True) == 4:
        atlas[x][y] = [False, False, False, False]

def shuffle(atlas):
    for i in range(len(atlas)):
        for j in range(len(atlas[0])):
            for _ in range(random.randint(0, 3)):
                atlas[i][j] = rotation(atlas, i, j)


userinput = input('Enter "/n" to create a new level, or enter "levelname" to load an existing level: ')
if userinput[0:2] != "/n":
    lines = []
    atlas = []
    level = userinput
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
elif userinput[0:2] == "/n":
    level_name = userinput[2:]
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    sourcex = int(input("Enter source x coordinate (0-indexed): "))
    sourcey = int(input("Enter source y coordinate (0-indexed): "))
    atlas = [[[False, False, False, False] for j in range(cols)] for i in range(rows)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 195, 255)

if rows > cols:
    HEIGHT = 900
    WIDTH = int(900 * cols / rows)
elif cols > rows:
    WIDTH = 900
    HEIGHT = int(900 * rows / cols)
else:
    WIDTH, HEIGHT = 900, 900

pygame.init()
icon_path = pathlib.Path(__file__).parent / "assets" / "iconlm.png"
if userinput[0:2] == "/n":
    pygame.display.set_caption("Pipes LM - New Level")
else:
    pygame.display.set_caption("Pipes LM - " + userinput)
    
pygame.display.set_icon(pygame.image.load(icon_path))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                 shuffle(atlas)
            if event.key == pygame.K_t:
                if WHITE == (255, 255, 255):
                    WHITE = (80, 80, 80)
                    BLACK = (0, 0, 0)
                    BLUE = (0, 195, 255)
                else:
                    WHITE = (255, 255, 255)
                    BLACK = (0, 0, 0)
                    BLUE = (0, 195, 255)
            if event.key == pygame.K_n:
                level_name = userinput[2:]
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                sourcex = int(input("Enter source x coordinate (0-indexed): "))
                sourcey = int(input("Enter source y coordinate (0-indexed): "))
                atlas = [[[False, False, False, False] for j in range(cols)] for i in range(rows)]
        x, y, click_type = selection(screen, 0, 0, WIDTH, HEIGHT, rows, cols)
        if x is not None and y is not None:
            if click_type == "left":
        # Capture the returned value and assign it back to the grid
                atlas[x][y] = rotation(atlas, x, y) 
            elif click_type == "right":
                change_pipe(atlas, x, y)
        draw_source(screen, WIDTH // cols, HEIGHT // rows, sourcex, sourcey, atlas)
        draw_pipe(screen, WIDTH // cols, HEIGHT // rows, atlas, sourcex, sourcey)
        
        pygame.display.update()
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                level_name = input("Enter level name to save as: ")
                level_name += ".txt"
                file_path = pathlib.Path(__file__).parent / "levels" / level_name
                with open(file_path, "w") as file:
                    file.write(f"{rows:02d},{cols:02d}\n")
                    file.write(f"{sourcex:02d},{sourcey:02d}\n")
                    for i in atlas:
                        row = []
                        for j in i:
                            if j == [False, False, False, False]:
                                row.append("0")
                            elif j == [True, False, False, False]: # dead end pipes
                                row.append("1")
                            elif j == [False, True, False, False]:
                                row.append("2")
                            elif j == [False, False, True, False]:
                                row.append("3")
                            elif j == [False, False, False, True]:
                                row.append("4")
                            elif j == [True, False, True, False]: # turn pipes
                                row.append("5")
                            elif j == [False, True, False, True]:
                                row.append("6")
                            elif j == [False, True, True, False]:
                                row.append("7")
                            elif j == [True, False, False, True]:
                                row.append("8")
                            elif j == [True, True, False, False]: # straight pipes
                                row.append("9")
                            elif j == [False, False, True, True]:
                                row.append("A")
                            elif j == [False, True, True, True]: # three way pipes
                                row.append("B")
                            elif j == [True, False, True, True]:
                                row.append("C")
                            elif j == [True, True, False, True]:
                                row.append("D")
                            elif j == [True, True, True, False]:
                                row.append("E")
                            elif j == [True, True, True, True]:
                                row.append("F")
                        file.write(",".join(row) + "\n")
                    print(f"Level saved to {file_path}")
                    pygame.display.set_caption("Pipes LM - " + level_name[:-4])
                
