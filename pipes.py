import pygame
import pathlib

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 195, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 100)  # Color used to show a level is saved/completed!

WIDTH, HEIGHT = 900, 900

# ----------------- SAVE & LOAD SYSTEM -----------------
def save_win(level_name):
    """Saves a level win to saves.txt if it isn't already saved."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    
    # Read existing wins to prevent duplicating entries
    existing_wins = load_wins()
    if level_name in existing_wins:
        print(f"{level_name} is already saved!")
        return
        
    with open(save_path, "a") as file:
        file.write(f"{level_name}\n")
    print(f"Saved win for {level_name}!")

def load_wins():
    """Reads saves.txt and returns a set of completed level names."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    if not save_path.exists():
        return set()
    
    with open(save_path, "r") as file:
        return set(line.strip() for line in file if line.strip())
# ------------------------------------------------------

def load_level(level_name):
    """Safely loads a level and returns (rows, cols, sourcex, sourcey, atlas)"""
    file_path = pathlib.Path(__file__).parent / "levels" / f"{level_name}.txt"
    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file]
        
        # Safe split implementation supporting multi-digit grids
        dimensions = lines[0].split(",")
        rows, cols = int(dimensions[0]), int(dimensions[1])
        
        source_coords = lines[1].split(",")
        sourcex, sourcey = int(source_coords[0]), int(source_coords[1])
        
        mapping = {
            "0": [False, False, False, False],
            "1": [True, False, False, False], "2": [False, True, False, False],
            "3": [False, False, True, False], "4": [False, False, False, True],
            "5": [True, False, True, False], "6": [False, True, False, True],
            "7": [False, True, True, False], "8": [True, False, False, True],
            "9": [True, True, False, False], "A": [False, False, True, True],
            "B": [False, True, True, True], "C": [True, False, True, True],
            "D": [True, True, False, True], "E": [True, True, True, False],
            "F": [True, True, True, True]
        }
        
        atlas = []
        for i in lines[2:rows+3]:
            row = [mapping[j] for j in i.split(",") if j in mapping]
            atlas.append(row)
            
        return rows, cols, sourcex, sourcey, atlas
    except FileNotFoundError:
        return None

def draw_pipe(screen, w, h, atlas, visited):
    y, y2 = 0, 0
    for i in atlas:
        x, x2 = 0, 0  
        for j in i: 
            if [y2, x2] in visited:
                pygame.draw.rect(screen, BLUE, (x + w//3, y + h//3, w//3, h//3))
            if j[0]: # up
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3, y, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + w//3, y), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y), (x + 2*w//3, y + h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w//3, y + h//3), 4)
            if j[1]: # down
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3, y + 2*h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            if j[2]: # left
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x, y + h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x, y + h//3), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + w//3, y + 2*h//3), (x + w//3, y + h//3), 4)
            if j[3]: # right
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + 2*w//3, y + h//3, w//3, h//3))
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + h//3), (x + w, y + h//3), 4)
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + w, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, BLACK, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h//3), 4)
            x += w
            x2 += 1
        y2 += 1
        y += h

def levelgrid(screen, x, y, w, h, rows, cols, saved_wins):
    """Draws selection grid. Turns cells GREEN if that level name has been beaten."""
    font = pygame.font.SysFont(None, 100)
    cell_width = w // cols
    cell_height = h // rows
    k = 1
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            
            # Check if this level number is in our saved_wins set
            level_name = f"level{k}"
            bg_color = GREEN if level_name in saved_wins else WHITE
            
            pygame.draw.rect(screen, bg_color, cell_rect)
            pygame.draw.rect(screen, BLACK, cell_rect, 1)
            
            text_surf = font.render(str(k), True, BLACK)
            screen.blit(text_surf, (x + j * cell_width + cell_width//2 - text_surf.get_width()//2, 
                                    y + i * cell_height + cell_height//2 - text_surf.get_height()//2))
            k += 1

def get_hovered_cell(x, y, w, h, rows, cols):
    mouse_pos = pygame.mouse.get_pos()
    cell_width = w // cols
    cell_height = h // rows
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            if cell_rect.collidepoint(mouse_pos):
                return i, j, cell_rect
    return None, None, None
                
def rotation(atlas, x, y):
    if (x, y) == (None, None) or atlas[x][y] == [False, False, False, False] or atlas[x][y] == [True, True, True, True]:
        return atlas[x][y]
    mapping = {
        (True, False, False, False): [False, False, False, True],
        (False, True, False, False): [False, False, True, False],
        (False, False, True, False): [True, False, False, False],
        (False, False, False, True): [False, True, False, False],
        (True, False, True, False):  [True, False, False, True],
        (False, True, True, False):  [True, False, True, False],
        (False, True, False, True):  [False, True, True, False],
        (True, False, False, True):  [False, True, False, True],
        (True, True, False, False):  [False, False, True, True],
        (False, False, True, True):  [True, True, False, False],
        (False, True, True, True):   [True, True, True, False],
        (True, False, True, True):   [True, True, False, True],
        (True, True, False, True):   [False, True, True, True],
        (True, True, True, False):   [True, False, True, True]
    }
    return mapping.get(tuple(atlas[x][y]), atlas[x][y])
    
def filledpipes(atlas, sourcex, sourcey):
    visited = []
    r_max = len(atlas)
    c_max = len(atlas[0]) if r_max > 0 else 0

    def flow(x, y):
        if [x, y] not in visited:
            visited.append([x, y])
            if atlas[x][y][0] and x > 0 and atlas[x-1][y][1]: 
                flow(x-1, y)
            if atlas[x][y][1] and x < r_max-1 and atlas[x+1][y][0]: 
                flow(x+1, y)
            if atlas[x][y][2] and y > 0 and atlas[x][y-1][3]: 
                flow(x, y-1)
            if atlas[x][y][3] and y < c_max-1 and atlas[x][y+1][2]: 
                flow(x, y+1)
    flow(sourcex, sourcey)
    return visited

def checkwin(atlas, visited):
    for i in range(len(atlas)):
        for j in range(len(atlas[0])):
            if atlas[i][j] != [False, False, False, False] and [i, j] not in visited:
                return False
    return True

# Initialize Game
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pipes")
clock = pygame.time.Clock()

rows, cols, sourcex, sourcey = 4, 4, 0, 0
atlas = []
current_level_name = "level1"

res = load_level(current_level_name)
if res:
    rows, cols, sourcex, sourcey, atlas = res

scene = "menu"
running = True

while running:
    screen.fill(WHITE)
    click_detected = False
    
   
    saved_wins = load_wins()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if scene == "level":
                    visited = filledpipes(atlas, sourcex, sourcey)
                    if checkwin(atlas, visited):
                        save_win(current_level_name)
                    else:
                        print("Can't save! You haven't connected all the pipes yet.")

                scene = "menu"
            elif event.key == pygame.K_x:
                level = input("Enter level name: ")
                res = load_level(level)
                if res:
                    current_level_name = level
                    rows, cols, sourcex, sourcey, atlas = res
                    scene = "level"
            
            elif event.key == pygame.K_s:
                if scene == "level":
                    visited = filledpipes(atlas, sourcex, sourcey)
                    if checkwin(atlas, visited):
                        save_win(current_level_name)
                    else:
                        print("Can't save! You haven't connected all the pipes yet.")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_detected = True

    if scene == "level":
        i, j, cell_rect = get_hovered_cell(0, 0, WIDTH, HEIGHT, rows, cols)
        if i is not None and j is not None:
            pygame.draw.rect(screen, BLUE, cell_rect, 4)
            if click_detected:
                atlas[i][j] = rotation(atlas, i, j)
                
        visited = filledpipes(atlas, sourcex, sourcey)
        draw_pipe(screen, WIDTH // cols, HEIGHT // rows, atlas, visited)
        
        if checkwin(atlas, visited):
            font = pygame.font.SysFont(None, 60)
            text = font.render("You win! Press 'S' to Save", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    elif scene == "menu":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Choose level", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 25))
        
        # Grid now draws green rectangles if level was previously saved
        levelgrid(screen, 100, 100, WIDTH-200, HEIGHT-200, 4, 4, saved_wins)
        i, j, cell_rect = get_hovered_cell(100, 100, WIDTH-200, HEIGHT-200, 4, 4)
        
        if i is not None and j is not None:
            pygame.draw.rect(screen, BLUE, cell_rect, 4)
            if click_detected:
                level_num = i * 4 + j + 1
                level_str = f"level{level_num}"
                res = load_level(level_str)
                if res:
                    current_level_name = level_str
                    rows, cols, sourcex, sourcey, atlas = res
                    scene = "level"

    pygame.display.update()
    clock.tick(60)

pygame.quit()
