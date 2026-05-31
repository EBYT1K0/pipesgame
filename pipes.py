import pygame
import pathlib
import random

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 195, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 100)  # Color used to show a level is saved/completed!

WIDTH, HEIGHT = 900, 900

icon_path = pathlib.Path(__file__).parent / "assets" / f"icon4.png"
pygame.display.set_icon(pygame.image.load(icon_path))
# ----------------- SAVE & LOAD SYSTEM -----------------
def save_win(level_name,elapsed_time):
    """Saves a level win to saves.txt if it isn't already saved."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    
    # Read existing wins to prevent duplicating entries
    existing_wins = load_wins()
    if level_name in existing_wins:
        print(f"{level_name} is already saved.")
        return
        
    with open(save_path, "a") as file:
        file.write(f"{level_name},{elapsed_time}\n")
    print(f"Saved win for {level_name}")

def load_wins():
    """Reads saves.txt and returns a list of completed level names."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    if not save_path.exists():
        return list
    
    with open(save_path, "r") as file:
        lines = [line.strip() for line in file if line.strip()]
    wins = []
    for line in lines:
        parts = line.split(",")
        if len(parts) >= 2:
            wins.append(parts[0])  # Only return the level name, not the time
    return wins
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
            bg_color = WHITE
            level_name = f"level{k}"
            if level_name in saved_wins:
                bg_color = GREEN
            else:
                bg_color = WHITE

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
    flow(sourcey, sourcex)
    return visited

def checkwin(atlas, visited):
    for i in range(len(atlas)):
        for j in range(len(atlas[0])):
            if atlas[i][j] != [False, False, False, False] and [i, j] not in visited:
                return False
    return True

def timercheckbox(screen, x, y, size, is_checked):
    pygame.draw.rect(screen, BLACK, (x, y, size, size), 4)
    font = pygame.font.SysFont(None, 50)
    text_surf = font.render("Show Timer (BETA)", True, BLACK)
    screen.blit(text_surf, (x + size + 10, y + size//2 - text_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if pygame.Rect(x, y, size, size).collidepoint(mouse_pos):
         pygame.draw.rect(screen, BLACK, (x, y, size, size), 2)
         if pygame.mouse.get_pressed()[0]:  # Left click
             is_checked = not is_checked
             pygame.time.delay(100)
    if is_checked:
        pygame.draw.line(screen, GREEN, (x + 5, y + size//2), (x + size//2, y + size - 5), 8)
        pygame.draw.line(screen, GREEN, (x + size//2, y + size - 5), (x + size - 5, y + 5), 8)
    return is_checked

def timer(screen, x, y, elapsed_time, show_timer):
    if not show_timer:
        return elapsed_time
    font = pygame.font.SysFont(None, 100)
    total_seconds = elapsed_time // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    milliseconds = elapsed_time % 1000
    time_string = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    text_surf = font.render(time_string, True, BLACK)
    screen.blit(text_surf, (x, y))
    return elapsed_time

def pagebutton(screen, x, y, w, h, page, last_page):
    if page < last_page:
         text = ">"
    font = pygame.font.SysFont(None, 50)
    button_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BLACK, button_rect, 4)
    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        if pygame.mouse.get_pressed()[0]:  # Left click
            return True
    return False

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

show_timer = False
elapsed_time = 0
start_ticks = 0
scene = "menu"
page = 0
last_page = 1
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
                        save_win(current_level_name, elapsed_time)
                        elapsed_time = 0

                scene = "menu"
            elif event.key == pygame.K_x:
                level = input("Enter level name: ")
                res = load_level(level)
                if res:
                    current_level_name = level
                    rows, cols, sourcex, sourcey, atlas = res
                    scene = "level"
                    pygame.display.quit()
                    if rows > cols:
                        HEIGHT = 900
                        WIDTH = int(900 * cols / rows)
                    elif cols > rows:
                        WIDTH = 900
                        HEIGHT = int(900 * rows / cols)
                    else:
                        WIDTH, HEIGHT = 900, 900
                    icon_path_cl = pathlib.Path(__file__).parent / "assets" / "iconlm.png"
                    pygame.display.set_caption("Pipes - Custom Level")
                    pygame.display.set_icon(pygame.image.load(icon_path_cl))
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
        win = checkwin(atlas, visited)
        
        if win:
            font = pygame.font.SysFont(None, 60)
            text = font.render("You win!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            elapsed_time = 0

        else:  # Get current time in milliseconds
            elapsed_time = pygame.time.get_ticks() - start_ticks  # Update elapsed_time with the time since last tick
            timer(screen, 25, 25, elapsed_time, show_timer)

    elif scene == "menu":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Choose level", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 25))
        show_timer = timercheckbox(screen, 25, HEIGHT - 75, 50, show_timer)
        pagebutton(screen, WIDTH - 75, HEIGHT - 75, 50, 50, page, last_page)
        
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
                    scene = "level"  # Reset timer when selecting a new level
                    start_ticks = pygame.time.get_ticks()  # Reset start time

    pygame.display.update()
    clock.tick(60)

pygame.quit()
