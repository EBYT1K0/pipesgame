import pygame
import pathlib
import os
import random

# Colors
BGCOLOR = (255, 255, 255)
BLUE = (0, 195, 255)
TEXT_COLOR = (0, 0, 0)
GREEN = (0, 200, 100)  # Color used to show a level is saved/completed!

WIDTH, HEIGHT = 900, 900

icon_path = pathlib.Path(__file__).parent / "assets" / f"icon4.png"

# ----------------- SAVE & LOAD SYSTEM -----------------
def save_win(level_name, elapsed_time):
    """Saves a level win to saves.txt, updating the time ONLY if it is faster."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    
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

    if level_name not in records or elapsed_time < records[level_name]:
        records[level_name] = elapsed_time
        print(f"New Personal Best for {level_name}! Time: {elapsed_time}ms")
        
        with open(save_path, "w") as file:
            for name, t in records.items():
                file.write(f"{name},{t}\n")
    else:
        print(f"Level {level_name} completed, but your time ({elapsed_time}ms) wasn't faster than your best ({records[level_name]}ms).")


def load_wins():
    """Reads saves.txt and returns a list of completed level names and their times."""
    save_path = pathlib.Path(__file__).parent / "saves.txt"
    if not save_path.exists():
        return [], []
    
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
                    continue
    return wins, time_data
# ------------------------------------------------------

def load_level(level_name):
    """Safely loads a level and returns (rows, cols, source_x, source_y, atlas)"""
    file_path = pathlib.Path(__file__).parent / "levels" / f"{level_name}.txt"
    try:
        with open(file_path, "r") as file:
            lines = [line.strip() for line in file]
        
        dimensions = lines[0].split(",")
        rows, cols = int(dimensions[0]), int(dimensions[1])
        
        source_coords = lines[1].split(",")
        source_x, source_y = int(source_coords[0]), int(source_coords[1])
        
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
            
        return rows, cols, source_x, source_y, atlas
    except FileNotFoundError:
        return None

def draw_pipe(screen, w, h, atlas, visited, sx, sy):
    y, y2 = 0, 0
    for i in atlas:
        x, x2 = 0, 0  
        for j in i: 
            if [y2, x2] in visited:
                pygame.draw.rect(screen, BLUE, (x + w//3 + sx, y + h//3 + sy, w//3, h//3))
            if j[0]: # up
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3 + sx, y + sy, w//3, h//3))
                pygame.draw.line(screen, TEXT_COLOR, (x + w//3 + sx, y + sy), (x + w//3 + sx, y + h//3 + sy), 4)
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + sy), (x + 2*w//3 + sx, y + h//3 + sy), 4)
            else:
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + h//3 + sy), (x + w//3 + sx, y + h//3 + sy), 4)
            if j[1]: # down
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + w//3 + sx, y + 2*h//3 + sy, w//3, h//3))
                pygame.draw.line(screen, TEXT_COLOR, (x + w//3 + sx, y + 2*h//3 + sy), (x + w//3 + sx, y + h + sy), 4)
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + 2*h//3 + sy), (x + 2*w//3 + sx, y + h + sy), 4)
            else:
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + 2*h//3 + sy), (x + w//3 + sx, y + 2*h//3 + sy), 4)
            if j[2]: # left
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + sx, y + h//3 + sy, w//3, h//3))
                pygame.draw.line(screen, TEXT_COLOR, (x + sx, y + h//3 + sy), (x + w//3 + sx, y + h//3 + sy), 4)
                pygame.draw.line(screen, TEXT_COLOR, (x + sx, y + 2*h//3 + sy), (x + w//3 + sx, y + 2*h//3 + sy), 4)
            else:
                pygame.draw.line(screen, TEXT_COLOR, (x + w//3 + sx, y + 2*h//3 + sy), (x + w//3 + sx, y + h//3 + sy), 4)
            if j[3]: # right
                if [y2, x2] in visited:
                    pygame.draw.rect(screen, BLUE, (x + 2*w//3 + sx, y + h//3 + sy, w//3, h//3))
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + h//3 + sy), (x + w + sx, y + h//3 + sy), 4)
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + 2*h//3 + sy), (x + w + sx, y + 2*h//3 + sy), 4)
            else:
                pygame.draw.line(screen, TEXT_COLOR, (x + 2*w//3 + sx, y + 2*h//3 + sy), (x + 2*w//3 + sx, y + h//3 + sy), 4)
            x += w
            x2 += 1
        y2 += 1
        y += h

def level_grid(screen, x, y, w, h, rows, cols, saved_wins, show_timer, page):
    font = pygame.font.SysFont(None, 100)
    timer_font = pygame.font.SysFont(None, 50) 
    
    cell_width = w // cols
    cell_height = h // rows
    k = 1 + (page*16)
    
    for i in range(rows):
        for j in range(cols):
            cell_rect = pygame.Rect(x + j * cell_width, y + i * cell_height, cell_width, cell_height)
            level_name = f"level{k}"
            
            bg_color = BGCOLOR
            record_time = None
            
            for z in saved_wins:
                if level_name == z[0]:
                    bg_color = GREEN
                    record_time = z[1]
                    break

            pygame.draw.rect(screen, bg_color, cell_rect)
            pygame.draw.rect(screen, TEXT_COLOR, cell_rect, 1)
            
            text_surf = font.render(str(k), True, TEXT_COLOR)
            screen.blit(text_surf, (x + j * cell_width + cell_width//2 - text_surf.get_width()//2, 
                                    y + i * cell_height + cell_height//2 - text_surf.get_height()//2))
            
            if show_timer and record_time is not None:
                total_seconds = record_time // 1000
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                milliseconds = record_time % 1000
                time_string = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
                
                time_text = timer_font.render(time_string, True, TEXT_COLOR)
                screen.blit(time_text, (x + j * cell_width + cell_width//2 - time_text.get_width()//2,
                                       y + i * cell_height + cell_height - time_text.get_height() - 5))
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
    
def filled_pipes(atlas, source_x, source_y):
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
    flow(source_y, source_x)
    return visited

def check_win(atlas, visited):
    for i in range(len(atlas)):
        for j in range(len(atlas[0])):
            if atlas[i][j] != [False, False, False, False] and [i, j] not in visited:
                return False
    return True

def draw_check_box(screen, x, y, size, is_checked, text):
    pygame.draw.rect(screen, TEXT_COLOR, (x, y, size, size), 4)
    font = pygame.font.SysFont(None, 50)
    text_surf = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surf, (x + size + 10, y + size//2 - text_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if pygame.Rect(x, y, size, size).collidepoint(mouse_pos):
         pygame.draw.rect(screen, TEXT_COLOR, (x, y, size, size), 2)
         if pygame.mouse.get_pressed()[0]:  # Left click
             is_checked = not is_checked
             click_sound.play()
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
    text_surf = font.render(time_string, True, TEXT_COLOR)
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
        pygame.draw.rect(screen, TEXT_COLOR, button_rect, 2)
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (x + w//2 - text_surf.get_width()//2, y + h//2 - text_surf.get_height()//2))
    if button2:
        pygame.draw.rect(screen, TEXT_COLOR, button2_rect, 2)
        text2_surf = font.render(text2, True, TEXT_COLOR)
        screen.blit(text2_surf, (x + w//2 - text2_surf.get_width()//2 - 50, y + h//2 - text2_surf.get_height()//2))
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and button:
        pygame.draw.rect(screen, BLUE, button_rect, 4)
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(100)
            click_sound.play()
            return page+1
    elif button2_rect.collidepoint(mouse_pos) and button2:
        pygame.draw.rect(screen, BLUE, button2_rect, 4)
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(100)
            click_sound.play()
            return page-1
    return page

def textured_button(screen, x, y, w, h, icon):
    button_rect = pygame.Rect(x, y, w, h)
    screen.blit(icon, (x, y))
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, button_rect, 4)
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(100)
            click_sound.play()
            return True
    return False

def draw_frame(screen, x, y, w, h):
    pygame.draw.rect(screen, TEXT_COLOR, (x, y, w, h), 2)

def screenflags(wm_info):
    if wm_info.get("display_name", "").startswith("wayland") or "wayland" in wm_info.get("display_name", "").lower():
        return pygame.RESIZABLE | pygame.SCALED
    return pygame.RESIZABLE


# ----------------- NEW DYNAMIC SETTINGS SYSTEM -----------------

# 1. Just add new settings here! The UI and storage will adjust automatically.
DEFAULT_SETTINGS = {
    "Show Timer": True,
    "Show Level Name": True,
    "Dark Theme": True,
    "Borderless Window": False,
    "Mute Sound": False,
    "Mute Music": True,
  # "New Setting Example": False  <-- Try adding your next settings here!
}

def save_settings(settings_dict):
    settings_path = pathlib.Path(__file__).parent / "settings.txt"
    with open(settings_path, "w") as file:
        for name, val in settings_dict.items():
            file.write(f"{name}:{val}\n")

def load_settings():
    settings_path = pathlib.Path(__file__).parent / "settings.txt"
    current_settings = DEFAULT_SETTINGS.copy()
    
    if not settings_path.exists():
        return current_settings
        
    with open(settings_path, "r") as file:
        for line in file:
            line = line.strip()
            if ":" in line:
                name, val_str = line.split(":", 1)
                if name in current_settings:
                    current_settings[name] = val_str.lower() == "true"
                    
    return current_settings

# Initialize Game
screen_width, screen_height = 1200, 900
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.mixer.init()

# Load images after pygame.init() so the display subsystem is ready
light_settings_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "settings_light.png")
dark_settings_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "settings_dark.png")
light_settings = pygame.transform.smoothscale(light_settings_unscaled, (75, 75))
dark_settings = pygame.transform.smoothscale(dark_settings_unscaled, (75, 75))
light_x_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "x_light.png")
dark_x_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "x_dark.png")
light_x = pygame.transform.smoothscale(light_x_unscaled, (75, 75))
dark_x = pygame.transform.smoothscale(dark_x_unscaled, (75, 75))
light_play_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "play_light.png")
dark_play_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "play_dark.png")
light_play = pygame.transform.smoothscale(light_play_unscaled, (200, 200))
dark_play = pygame.transform.smoothscale(dark_play_unscaled, (200, 200))
light_backarrow_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "backarrow_light.png")
dark_backarrow_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "backarrow_dark.png")
light_backarrow = pygame.transform.smoothscale(light_backarrow_unscaled, (75, 75))
dark_backarrow = pygame.transform.smoothscale(dark_backarrow_unscaled, (75, 75))
logo_unscaled = pygame.image.load(pathlib.Path(__file__).parent / "assets" / "logo.png")
logo = pygame.transform.scale(logo_unscaled, (900, 300))
pygame.display.set_icon(pygame.image.load(icon_path))
wm_info = pygame.display.get_wm_info()
click_sound = pygame.mixer.Sound(str(pathlib.Path(__file__).parent / "sounds" / "click.wav"))
click_sound.set_volume(0.2)
whoosh_sound = pygame.mixer.Sound(str(pathlib.Path(__file__).parent / "sounds" / "whoosh.wav"))
whoosh_sound.set_volume(0.2)
music_list = [f.name for f in pathlib.Path('music').iterdir() if f.is_file()]
screen = pygame.display.set_mode((screen_width, screen_height), screenflags(wm_info))
pygame.display.set_caption("Pipes")
clock = pygame.time.Clock()

rows, cols, source_x, source_y = 4, 4, 0, 0
atlas = []
current_level_name = "level1"

res = load_level(current_level_name)
if res:
    rows, cols, source_x, source_y, atlas = res

# Load settings dict
game_settings = load_settings()

record = 0
start_ticks = 0
time_string = "00:00.000"
scene = "main_menu"
page = 0
last_page = 1

if game_settings["Borderless Window"]:
    screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
    pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
else:
    screen_width, screen_height = 1200, 900
    pygame.display.set_mode((screen_width, screen_height), screenflags(wm_info))
running = True

while running:
    screen.fill(BGCOLOR)
    click_detected = False
    
    saved_wins, level_and_time = load_wins()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), screenflags(wm_info))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if scene == "level":
                    visited = filled_pipes(atlas, source_x, source_y)
                    if check_win(atlas, visited):
                        save_win(current_level_name, record)
                        record = 0
                    scene = "selector"
                    break
                scene = "main_menu"
                WIDTH, HEIGHT = 900, 900
            elif event.key == pygame.K_x:
                level = input("Enter level name: ")
                res = load_level(level)
                if res:
                    current_level_name = level
                    rows, cols, source_x, source_y, atlas = res
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
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), screenflags(wm_info))
            elif event.key == pygame.K_F11:
                game_settings["Borderless Window"] = not game_settings["Borderless Window"]
                if game_settings["Borderless Window"]:
                    screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
                    pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
                else:
                    screen_width, screen_height = 1200, 900
                    pygame.display.set_mode((screen_width, screen_height), screenflags(wm_info))
                save_settings(game_settings)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_detected = True

    if scene == "level":
        draw_frame(screen, (screen_width - WIDTH)//2 - 4, (screen_height - HEIGHT)//2 - 4, WIDTH + 8, HEIGHT + 8)
        i, j, cell_rect = get_hovered_cell((screen_width - WIDTH)//2, (screen_height - HEIGHT)//2, WIDTH, HEIGHT, rows, cols)
        if i is not None and j is not None:
            pygame.draw.rect(screen, BLUE, cell_rect, 4)
            if click_detected and not win:
                atlas[i][j] = rotation(atlas, i, j)
                whoosh_sound.play()
                
        visited = filled_pipes(atlas, source_x, source_y)
        draw_pipe(screen, WIDTH // cols, HEIGHT // rows, atlas, visited, (screen_width - WIDTH)//2, (screen_height - HEIGHT)//2)
        win = check_win(atlas, visited)
        
        if win:
            font = pygame.font.SysFont(None, 100)
            text = font.render("You win!", True, TEXT_COLOR)
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() * 3))
            if game_settings["Show Timer"]:
                if time_string == None:
                    time_string = "00:00.000"
                text = font.render(time_string, True, TEXT_COLOR)
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height()))
        else:
            record = pygame.time.get_ticks() - start_ticks
            time_string = timer(screen, 25, 25, record, game_settings["Show Timer"])
            if game_settings["Show Level Name"]:
                font = pygame.font.SysFont(None, 100)
                level_text = font.render(current_level_name, True, TEXT_COLOR)
                screen.blit(level_text, (screen_width // 2 - level_text.get_width() // 2, 25))

    elif scene == "selector":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Choose level", True, TEXT_COLOR)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, (screen_height - HEIGHT)//2 + 25))
        page = pagebutton(screen, screen_width//2, (screen_height - HEIGHT)//2 + HEIGHT - 75, 50, 50, page, last_page)
        if textured_button(screen, 25,25, 75, 75, back_icon):
            scene = "main_menu"
        
        level_grid(screen, (screen_width - WIDTH)//2 + 100, (screen_height - HEIGHT)//2 + 100, WIDTH-200, HEIGHT-200, 4, 4, level_and_time, game_settings["Show Timer"], page)
        i, j, cell_rect = get_hovered_cell((screen_width - WIDTH)//2 + 100, (screen_height - HEIGHT)//2 + 100, WIDTH-200, HEIGHT-200, 4, 4)
        
        if i is not None and j is not None:
            pygame.draw.rect(screen, BLUE, cell_rect, 4)
            if click_detected:
                click_sound.play()
                level_num = i * 4 + j + 1 + page*16
                level_str = f"level{level_num}"
                res = load_level(level_str)
                if res:
                    current_level_name = level_str
                    rows, cols, source_x, source_y, atlas = res
                    scene = "level"
                    start_ticks = pygame.time.get_ticks()
                    
    elif scene == "settings":
        font = pygame.font.SysFont(None, 100)
        text = font.render("Settings", True, TEXT_COLOR)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, (screen_height - HEIGHT)//2 + 25))
        
        # --- DYNAMIC CHECKBOX LAYOUT GENERATION ---
        start_y = (screen_height - HEIGHT)//2 + 150
        spacing = 100
        for idx, setting_name in enumerate(game_settings.keys()):
            current_y = start_y + (idx * spacing)
            game_settings[setting_name] = draw_check_box(
                screen, 
                screen_width//2 - 200, 
                current_y, 
                50, 
            game_settings[setting_name], 
            setting_name
            )
        # ------------------------------------------

        if game_settings["Dark Theme"]:
            BGCOLOR = (30,30,30)
            TEXT_COLOR = (200,200,200)
            BLUE = (0, 58, 112)
            GREEN = (0, 94, 24)
            settings_icon = dark_settings
            x_icon = dark_x
            play_icon = dark_play
            back_icon = dark_backarrow
        else:
            BGCOLOR = (255,255,255)
            TEXT_COLOR = (0,0,0)
            BLUE = (0, 195, 255)
            GREEN = (0, 200, 100)
            settings_icon = light_settings
            x_icon = light_x
            play_icon = light_play
            back_icon = light_backarrow
        if game_settings["Mute Sound"]:
            click_sound.set_volume(0)
            whoosh_sound.set_volume(0)
        else:
            click_sound.set_volume(0.2)
            whoosh_sound.set_volume(0.2)
            
        if textured_button(screen, 25,25, 75, 75, back_icon):
            if game_settings["Borderless Window"]:
                screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
                pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
            else:
                screen_width, screen_height = 1200, 900
                pygame.display.set_mode((screen_width, screen_height), screenflags(wm_info))
            save_settings(game_settings)
            scene = "main_menu"
    elif scene == "main_menu":
        screen.blit(logo, (screen_width // 2 - logo.get_width() // 2, 50))
        if game_settings["Dark Theme"]:
            BGCOLOR = (30,30,30)
            TEXT_COLOR = (200,200,200)
            BLUE = (0, 58, 112)
            GREEN = (0, 94, 24)
            settings_icon = dark_settings
            x_icon = dark_x
            play_icon = dark_play
            back_icon = dark_backarrow
        else:
            BGCOLOR = (255,255,255)
            TEXT_COLOR = (0,0,0)
            BLUE = (0, 195, 255)
            GREEN = (0, 200, 100)
            settings_icon = light_settings
            x_icon = light_x
            play_icon = light_play
            back_icon = light_backarrow
        if textured_button(screen, screen_width//2 - play_icon.get_width()//2, screen_height//2 - play_icon.get_height()//2, 200, 200, play_icon):
            scene = "selector"
        if textured_button(screen, screen_width//2 - settings_icon.get_width()//2 - 200, screen_height//2 - settings_icon.get_height()//2, 75,75, settings_icon):
            scene = "settings"
        if textured_button(screen, screen_width//2 - x_icon.get_width()//2 + 200, screen_height//2 - x_icon.get_height()//2, 75,75, x_icon):
            running = False
    if not pygame.mixer.music.get_busy() and not game_settings["Mute Music"] and music_list:
        next_music = random.choice(music_list)
        pygame.mixer.music.load(str(pathlib.Path(__file__).parent / "music" / next_music))
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)
    elif game_settings["Mute Music"]:
        pygame.mixer.music.stop()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
