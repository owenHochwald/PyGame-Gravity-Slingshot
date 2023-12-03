import pygame, sys
from pygame.locals import *
import math
from button import Button


# init steps
pygame.init()

WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitional Slingshot Effect")

PLANET_MASS = 100 
SHIP_MASS = 5
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 100

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

# background
SPACE_BG = pygame.transform.scale(pygame.image.load(r"images/space_background.jpg"), (WIDTH,HEIGHT))
GRAY_BG = pygame.transform.scale(pygame.image.load(r"images/graybackground.jpg"), (WIDTH,HEIGHT))

# planets
EARTH = pygame.transform.scale(pygame.image.load(r"images/earth_cartoon.png"), (PLANET_SIZE *2, PLANET_SIZE *2))
MOON = pygame.transform.scale(pygame.image.load(r"images/moon_cartoon.png"), (PLANET_SIZE *1.25, PLANET_SIZE *1.25))
JUPITER = pygame.transform.scale(pygame.image.load(r"images/jupiter_cartoon.png"), (PLANET_SIZE *5, PLANET_SIZE *5))
BLACK_HOLE = pygame.transform.scale(pygame.image.load(r"images/black_hole_cartoon.png"), (PLANET_SIZE *5, PLANET_SIZE *5))

# planet size factor
EARTH_SIZE_FACTOR = 1
MOON_SIZE_FACTOR = 0.75
JUPITER_SIZE_FACTOR = 2.5
BLACK_HOLE_SIZE_FACTOR = JUPITER_SIZE_FACTOR

# planet gravitys
EARTH_G = 9.8
MOON_G = 1.6
JUPITER_G = 24
BLACK_HOLE_G = 10000


# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# setting global variables
global PLANET
PLANET = EARTH
global G 
G = EARTH_G
global BG
BG = SPACE_BG
global selected_color
selected_color = GREEN
global SIZE_FACTOR
SIZE_FACTOR = EARTH_SIZE_FACTOR



# making main menu
def main_menu():
    while True:
        win.blit(BG, (0,0))


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("G.S. SIM", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        win.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
def options():
    global selected_color
    global BG
    global PLANET
    global G
    global SIZE_FACTOR
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        win.fill("gray")


        OPTIONS_TEXT = get_font(35).render("Select your Configurations.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 30))
        win.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # ship color configuration buttons
        COLOR_TEXT = get_font(25).render("Ship Color Options.", True, "Black")
        COLOR_RECT = COLOR_TEXT.get_rect(center=(640, 90))
        win.blit(COLOR_TEXT, COLOR_RECT)
        # green
        OPTION_SELECT_GREEN = Button(image=None, pos=(240, 160),
                               text_input="GREEN", font=get_font(30), base_color="Black", hovering_color="Green")        
        OPTION_SELECT_GREEN.changeColor(OPTIONS_MOUSE_POS)
        OPTION_SELECT_GREEN.update(win)
        # red
        OPTION_SELECT_RED = Button(image=None, pos=(640, 160),
                               text_input="RED", font=get_font(30), base_color="Black", hovering_color="Red")        
        OPTION_SELECT_RED.changeColor(OPTIONS_MOUSE_POS)
        OPTION_SELECT_RED.update(win)
        # blue
        OPTION_SELECT_BLUE = Button(image=None, pos=(940, 160),
                               text_input="BLUE", font=get_font(30), base_color="Black", hovering_color="Blue")        
        OPTION_SELECT_BLUE.changeColor(OPTIONS_MOUSE_POS)
        OPTION_SELECT_BLUE.update(win)
        
        # background selector
        BACKGROUND_TEXT = get_font(25).render("Background Options.", True, "Black")
        BACKGROUND_RECT = BACKGROUND_TEXT.get_rect(center=(640, 230))
        win.blit(BACKGROUND_TEXT, BACKGROUND_RECT)
        # space background
        BACKGROUND_SELECT_SPACE = Button(image=None, pos=(340, 280),
                               text_input="Space", font=get_font(30), base_color="Black", hovering_color="#d7fcd4")        
        BACKGROUND_SELECT_SPACE.changeColor(OPTIONS_MOUSE_POS)
        BACKGROUND_SELECT_SPACE.update(win)
        # white background
        BACKGROUND_SELECT_GRAY = Button(image=None, pos=(840, 280),
                               text_input="Blank", font=get_font(30), base_color="Black", hovering_color="#d7fcd4")        
        BACKGROUND_SELECT_GRAY.changeColor(OPTIONS_MOUSE_POS)
        BACKGROUND_SELECT_GRAY.update(win)
        
        
        # planet selector
        PLANET_TEXT = get_font(25).render("Planet Selector.", True, "Black")
        PLANET_RECT = PLANET_TEXT.get_rect(center=(640, 325))
        win.blit(PLANET_TEXT, PLANET_RECT)
        # earth planet
        PLANET_SELECT_EARTH = Button(image=None, pos=(140, 370),
                               text_input="Earth", font=get_font(30), base_color="Black", hovering_color="#d7fcd4")        
        PLANET_SELECT_EARTH.changeColor(OPTIONS_MOUSE_POS)
        PLANET_SELECT_EARTH.update(win)
        # jupiter planet
        PLANET_SELECT_JUPITER = Button(image=None, pos=(420, 370),
                               text_input="Jupyter", font=get_font(30), base_color="Black", hovering_color="#d7fcd4")        
        PLANET_SELECT_JUPITER.changeColor(OPTIONS_MOUSE_POS)
        PLANET_SELECT_JUPITER.update(win)
        # moon planet
        PLANET_SELECT_MOON = Button(image=None, pos=(690, 370),
                               text_input="Moon", font=get_font(30), base_color="Black", hovering_color="#d7fcd4")     
        PLANET_SELECT_MOON.changeColor(OPTIONS_MOUSE_POS)
        PLANET_SELECT_MOON.update(win)
        # black hole planet
        PLANET_SELECT_BLACK_HOLE = Button(image=None, pos=(1000, 370),
                               text_input="Black Hole", font=get_font(30), base_color="Black", hovering_color="Purple")     
        PLANET_SELECT_BLACK_HOLE.changeColor(OPTIONS_MOUSE_POS)
        PLANET_SELECT_BLACK_HOLE.update(win)
        

        
        
        # back return button
        OPTIONS_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(55), base_color="Black", hovering_color="#d7fcd4")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTION_SELECT_GREEN.checkForInput(OPTIONS_MOUSE_POS):
                    selected_color = GREEN
                if OPTION_SELECT_BLUE.checkForInput(OPTIONS_MOUSE_POS):
                    selected_color = BLUE
                if OPTION_SELECT_RED.checkForInput(OPTIONS_MOUSE_POS):
                    selected_color = RED
                if BACKGROUND_SELECT_SPACE.checkForInput(OPTIONS_MOUSE_POS):
                    BG = SPACE_BG
                if BACKGROUND_SELECT_GRAY.checkForInput(OPTIONS_MOUSE_POS):
                    BG = GRAY_BG
                if PLANET_SELECT_EARTH.checkForInput(OPTIONS_MOUSE_POS):
                    PLANET = EARTH
                    G = EARTH_G
                    SIZE_FACTOR = EARTH_SIZE_FACTOR
                if PLANET_SELECT_JUPITER.checkForInput(OPTIONS_MOUSE_POS):
                    PLANET = JUPITER
                    G = JUPITER_G
                    SIZE_FACTOR = JUPITER_SIZE_FACTOR
                if PLANET_SELECT_MOON.checkForInput(OPTIONS_MOUSE_POS):
                    PLANET = MOON
                    G = MOON_G
                    SIZE_FACTOR = MOON_SIZE_FACTOR
                if PLANET_SELECT_BLACK_HOLE.checkForInput(OPTIONS_MOUSE_POS):
                    PLANET = BLACK_HOLE
                    G = BLACK_HOLE_G
                    SIZE_FACTOR = BLACK_HOLE_SIZE_FACTOR
                    
                    

        pygame.display.update()

def play():
    
    # planet class
    class Planet:
        def __init__(self, x,y,mass):
            self.x = x
            self.y = y
            self.mass = mass
        
        def draw(self):
            win.blit(PLANET, (self.x - PLANET_SIZE * SIZE_FACTOR, self.y - PLANET_SIZE * SIZE_FACTOR))


    # spacecraft class and logic
    class Spacecraft:
        def __init__(self, x, y, vel_x, vel_y, mass, size):
            self.x = x
            self.y = y
            self.vel_x = vel_x
            self.vel_y = vel_y
            self.mass = SHIP_MASS + mass
            self.size = OBJ_SIZE + size
        
        def move(self, planet=None):
            distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
            force = (G * self.mass * planet.mass) / (distance**2)

            acceleration = force / self.mass
            angle = math.atan2(planet.y - self.y, planet.x - self.x)
            
            # getting directional components
            acceleration_x = math.cos(angle) * acceleration
            acceleration_y = math.sin(angle) * acceleration
            
            self.vel_x += acceleration_x
            self.vel_y += acceleration_y
            
            self.x += self.vel_x
            self.y += self.vel_y
            
        def change_mass(self, amount):
            self.mass += amount
        def change_size(self, amount):
            self.size += amount
        def draw(self, planet=None):
            pygame.draw.rect(win, selected_color, pygame.Rect((int(self.x), int(self.y)), (self.size*2, self.size*2)))

            
    # function to create Spacecraft classes for us
    def create_ship(location, mouse, mass, size):
        t_x, t_y = location
        m_x, m_y = mouse
        vel_x = (m_x - t_x) / VEL_SCALE
        vel_y = (m_y - t_y) / VEL_SCALE
        obj = Spacecraft(t_x, t_y, vel_x, vel_y, mass, size)
        return obj

    # pygame funcationality
    def main():
        running = True
        clock = pygame.time.Clock()
        
        planet = Planet(WIDTH //2, HEIGHT //2, PLANET_MASS)
        planet_loc_x, planet_loc_y = planet.x - PLANET_SIZE * SIZE_FACTOR, planet.y - PLANET_SIZE * SIZE_FACTOR
        objects = []
        temp_obj_pos = None
        angle = 0
        action = False
        global temp_ship_mass
        global temp_obj_size
        temp_ship_mass = 0
        temp_obj_size = 0
        
        while running:
            clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            # drawing background
            win.blit(BG, (0,0))
            
            # drawing back button to return to the main menu
            PLAY_BACK = Button(image=pygame.image.load("images/Play Back.png"), pos=(90, 40), 
                            text_input="BACK", font=get_font(35), base_color="WHITE", hovering_color="#d7fcd4")
            # QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(640, 550), 
            #                 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            PLAY_BACK.changeColor(mouse_pos)
            PLAY_BACK.update(win)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # if mouse has been clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # implementing hold feature
                    action = True
                    if PLAY_BACK.checkForInput(mouse_pos):
                        main_menu()
                    
                    if not temp_obj_pos:
                        temp_obj_pos = mouse_pos
                        # variable here
                        action = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if temp_obj_pos:
                        t_x, t_y = temp_obj_pos
                        obj = create_ship(temp_obj_pos, mouse_pos, temp_ship_mass, temp_obj_size)
                        objects.append(obj)
                        temp_obj_pos = None
                        temp_ship_mass =0
                        temp_obj_size =0

            # draw ship when mouse is held down
            if temp_obj_pos:
                temp_ship_mass += 10
                temp_obj_size += 0.05
                rect_center = (temp_obj_pos[0] + OBJ_SIZE+temp_obj_size, temp_obj_pos[1] + OBJ_SIZE+temp_obj_size)
                pygame.draw.line(win, WHITE, rect_center, mouse_pos, 2)
                pygame.draw.rect(win, selected_color, pygame.Rect(temp_obj_pos, ((OBJ_SIZE+temp_obj_size)*2, (OBJ_SIZE+temp_obj_size)*2)))
            
            # using objects[:] to make a copy of the list and doesnt affect iteration
            for obj in objects[:]:
                obj.draw(planet)
                obj.move(planet)
                off_screen = obj.x < -(WIDTH*3) or obj.x > WIDTH*3 or obj.y < -(HEIGHT*3) or obj.y > HEIGHT*3
                collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE * SIZE_FACTOR
                if off_screen or collided:
                    objects.remove(obj)
            #  CHANGING THIS PART
            # planet.draw()
            
            angle -= 1
            angle %= 360
            rotated = pygame.transform.rotate(PLANET, angle)
            planet_rotated_rect = rotated.get_rect(center = (planet_loc_x, planet_loc_y))
            win.blit(rotated, planet_rotated_rect)
            # -----------------------
            pygame.display.update()
        
        pygame.quit()
    main()

if __name__ == "__main__":
    main_menu()
