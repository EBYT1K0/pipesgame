import pygame
import pathlib

# Colors
BGCOLOR = (255, 255, 255)
BLUE = (0, 195, 255)
TEXTCOLOR = (0, 0, 0)
GREEN = (0, 200, 100)  # Color used to show a level is saved/completed!

WIDTH, HEIGHT = 900, 900

icon_path = pathlib.Path(__file__).parent / "assets" / f"icon4.png"
pygame.display.set_icon(pygame.image.load(icon_path))
# ----------------- SAVE & LOAD SYSTEM -----------------
def save_win(level_name, elapsed_time):
    """Saves a level win to saves.txt, updating the time ONLY if it is faster."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    
    # 1. Read all existing records into a dictionary {level_name: elapsed_time}
    records = {}
    if save_path.exists():
        with open(save_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and "," in line:
                    name, t_str = line.split(",", 1)
                    try:
                        records[name] = int(t_str)
                    except ValueError:
                        continue

    # 2. Check if we should update: 
    # If the level hasn't been beaten yet, OR if the new time is lower than the old time
    if level_name not in records or elapsed_time < records[level_name]:
        records[level_name] = elapsed_time
        print(f"New Personal Best for {level_name}! Time: {elapsed_time}ms")
        
        # 3. Save everything back to the file cleanly
        with open(save_path, "w") as file:
            for name, t in records.items():
                file.write(f"{name},{t}\n")
    else:
        print(f"Level {level_name} completed, but your time ({elapsed_time}ms) wasn't faster than your best ({records[level_name]}ms).")


def load_wins():
    """Reads saves.txt and returns a list of completed level names and their times."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    if not save_path.exists():
        return [], []  # Crucial fix: returns empty lists instead of the type 'list'
    
    wins = []
    time_data = []
    
    with open(save_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and "," in line:
                parts = line.split(",", 1)
                try:
                    level_name = parts[0]
                    elapsed = int(parts[1])
                    
                    wins.append(level_name)
                    time_data.append([level_name, elapsed])
                except ValueError:
                    continue  # Skip malformed lines safely
    return wins, time_data
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
                pygame.draw.line(screen, TEXTCOLOR, (x + w//3, y), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y), (x + 2*w//3, y + h//3), 4)
            else:
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + h//3), (x + w//3, y + h//3), 4)
            if j[1]: # down
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3, y + 2*h//3, w//3, h//3))
                pygame.draw.line(screen, TEXTCOLOR, (x + w//3, y + 2*h//3), (x + w//3, y + h), 4)
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h), 4)
            else:
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            if j[2]: # left
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x, y + h//3, w//3, h//3))
                pygame.draw.line(screen, TEXTCOLOR, (x, y + h//3), (x + w//3, y + h//3), 4)
                pygame.draw.line(screen, TEXTCOLOR, (x, y + 2*h//3), (x + w//3, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, TEXTCOLOR, (x + w//3, y + 2*h//3), (x + w//3, y + h//3), 4)
            if j[3]: # right
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + 2*w//3, y + h//3, w//3, h//3))
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + h//3), (x + w, y + h//3), 4)
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + 2*h//3), (x + w, y + 2*h//3), 4)
            else:
                pygame.draw.line(screen, TEXTCOLOR, (x + 2*w//3, y + 2*h//3), (x + 2*w//3, y + h//3), 4)
            x += w
            x2 += 1
        y2 += 1
        y += h

def levelgrid(screen, x, y, w, h, rows, cols, saved_wins, show_timer, page):
    """Draws selection grid. Turns cells GREEN if that level name has been beaten."""
    font = pygame.font.SysFont(None, 100)
    # A smaller font helps the timer string fit inside the grid cell cleanly
    timer_font = pygame.font.SysFont(None, 50) 
    
    cell_width = w // cols
    cell_height = h // rows
    k = 1 + (page*16)
    
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            level_name = f"level{k}"
            
            # 1. Determine if this level has been beaten and find its record
            bg_color = BGCOLOR
            record_time = None
            
            for z in saved_wins:
                if level_name == z[0]:  # Match the exact level name string
                    bg_color = GREEN
                    record_time = z[1]
                    break  # Found it! Break early so it doesn't get overwritten

            # 2. Draw the cell background and border
            pygame.draw.rect(screen, bg_color, cell_rect)
            pygame.draw.rect(screen, TEXTCOLOR, cell_rect, 1)
            
            # 3. Draw the level number text centered
            text_surf = font.render(str(k), True, TEXTCOLOR)
            screen.blit(text_surf, (x + j * cell_width + cell_width//2 - text_surf.get_width()//2, 
                                    y + i * cell_height + cell_height//2 - text_surf.get_height()//2))
            
            # 4. Draw the personal best timer INSIDE the cell if enabled and beaten
            if show_timer and record_time is not None:
                total_seconds = record_time // 1000
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                milliseconds = record_time % 1000
                time_string = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                
                timetext = timer_font.render(time_string, True, TEXTCOLOR)
                # Places the timer text near the bottom edge of the individual cell
                screen.blit(timetext, (x + j * cell_width + cell_width//2 - timetext.get_width()//2,
                                       y + i * cell_height + cell_height - timetext.get_height() - 5))
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
    pygame.draw.rect(screen, TEXTCOLOR, (x, y, size, size), 4)
    font = pygame.font.SysFont(None, 50)
    text_surf = font.render("Show Timer", True, TEXTCOLOR)
    screen.blit(text_surf, (x + size + 10, y + size//2 - text_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if pygame.Rect(x, y, size, size).collidepoint(mouse_pos):
         pygame.draw.rect(screen, TEXTCOLOR, (x, y, size, size), 2)
         if pygame.mouse.get_pressed()[0]:  # Left click
             is_checked = not is_checked
             pygame.time.delay(100)
    if is_checked:
        pygame.draw.line(screen, GREEN, (x + 5, y + size//2), (x + size//2, y + size - 5), 8)
        pygame.draw.line(screen, GREEN, (x + size//2, y + size - 5), (x + size - 5, y + 5), 8)
    return is_checked

def darkthemecheckbox(screen, x, y, size, is_checked):
    pygame.draw.rect(screen, TEXTCOLOR, (x, y, size, size), 4)
    font = pygame.font.SysFont(None, 50)
    text_surf = font.render("Dark Theme", True, TEXTCOLOR)
    screen.blit(text_surf, (x + size + 10, y + size//2 - text_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if pygame.Rect(x, y, size, size).collidepoint(mouse_pos):
         pygame.draw.rect(screen, TEXTCOLOR, (x, y, size, size), 2)
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
    text_surf = font.render(time_string, True, TEXTCOLOR)
    screen.blit(text_surf, (x, y))
    return time_string

def pagebutton(screen, x, y, w, h, page, last_page):
    text = ">"
    text2 = "<"
    button = False
    button2 = False
    if page < last_page:
        button = True
    if page > 0:
        button2 = True
    font = pygame.font.SysFont(None, 50)
    button_rect = pygame.Rect(x, y, w, h)
    button2_rect = pygame.Rect(x-50, y, w, h)
    if button:
        pygame.draw.rect(screen, TEXTCOLOR, button_rect, 2)
        text_surf = font.render(text, True, TEXTCOLOR)
        screen.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))
    if button2:
        pygame.draw.rect(screen, TEXTCOLOR, button2_rect, 2)
        text2_surf = font.render(text2, True, TEXTCOLOR)
        screen.blit(text2_surf, (x + w//2 - text2_surf.get_width()//2 - 50, y + h//2 - text2_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and button:
        pygame.draw.rect(screen, BLUE, button_rect, 4)
        if pygame.mouse.get_pressed()[0]:  # Left click
            return page+1
    elif button2_rect.collidepoint(mouse_pos) and button2:
        pygame.draw.rect(screen, BLUE, button2_rect, 4)
        if pygame.mouse.get_pressed()[0]:
            return page-1
    return page

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

show_timer = True
dark_theme = True
record = 0
start_ticks = 0
time_string = "00:00.000"
scene = "menu"
page = 0
last_page = 1
running = True

while running:
    screen.fill(BGCOLOR)
    click_detected = False
    
   
    saved_wins, levelandtime = load_wins()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if scene == "level":
                    visited = filledpipes(atlas, sourcex, sourcey)
                    if checkwin(atlas, visited):
                        save_win(current_level_name, record)
                        record = 0

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
            font = pygame.font.SysFont(None, 100)
            text = font.render("You win!", True, TEXTCOLOR)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()*3))
            if show_timer:
                if time_string == None:
                    time_string = "00:00.000"
                text = font.render(time_string, True, TEXTCOLOR)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()))
            #elapsed_time = 0

        else:  # Get current time in milliseconds
            record = pygame.time.get_ticks() - start_ticks  # Update elapsed_time with the time since last tick
            time_string = timer(screen, 25, 25, record, show_timer)

    elif scene == "menu":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Choose level", True, TEXTCOLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 25))
        show_timer = timercheckbox(screen, 25, HEIGHT - 75, 50, show_timer)
        dark_theme = darkthemecheckbox(screen, 325, HEIGHT - 75, 50, dark_theme)
        if dark_theme:
            BGCOLOR = (80,80,80)
            TEXTCOLOR = (200,200,200)
            BLUE = (0, 58, 112)
            GREEN = (0, 94, 24)
        else:
            BGCOLOR = (255,255,255)
            TEXTCOLOR = (0,0,0)
            BLUE = (0, 195, 255)
            GREEN = (0, 200, 100)

        page = pagebutton(screen, WIDTH - 75, HEIGHT - 75, 50, 50, page, last_page)
        
        # Grid now draws green rectangles if level was previously saved
        levelgrid(screen, 100, 100, WIDTH-200, HEIGHT-200, 4, 4, levelandtime, show_timer, page)
        i, j, cell_rect = get_hovered_cell(100, 100, WIDTH-200, HEIGHT-200, 4, 4)
        
        if i is not None and j is not None:
            pygame.draw.rect(screen, BLUE, cell_rect, 4)
            if click_detected:
                level_num = i * 4 + j + 1 + page*16
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
