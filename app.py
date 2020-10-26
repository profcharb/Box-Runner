import pygame
import random

pygame.init()

# Setting up screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Box Runner")
SCREEN.fill((0, 0, 0))

home = True                 # For the home screen
start = True                # To (re)start the game
run = True                  # The main game loop
paused = False              # For pausing
game_over = False           # From main loop to game over screen
end = False                 # From game over screen to restart/quit
show_stat = False
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 171, 0)
RED = (255, 0, 0)
bound_height = 10
up_bound_y = SCREEN_HEIGHT//6
low_bound_y = (SCREEN_HEIGHT//6) * 5
GRAVITY = 2
J_VEL = -28
OBST_SPEED = 5
HIGHSCORE = 0

FPS = 60


class Thing:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.j_vel = 0
        self.vel = 5
        self.gravity = GRAVITY
        self.colour = colour
        self.is_flat = False
        self.isJump = True
        self.hitbox = (self.x, self.y, self.width, self.height)

    def reset(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.j_vel = 0
        self.gravity = GRAVITY
        self.isJump = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

    def display_prop(self, screen):
        font = pygame.font.SysFont("comicsansms", 20)
        text1 = font.render(f"Jump velocity: {self.j_vel}", True, (255, 255, 255))
        text2 = font.render(f"x: {self.x}", True, (255, 255, 255))
        text3 = font.render(f"y: {self.y}", True, (255, 255, 255))
        text4 = font.render(f"Flattened: {self.is_flat}", True, (255, 255, 255))
        screen.blit(text1, (550, 100))
        screen.blit(text2, (550, 120))
        screen.blit(text3, (550, 140))
        screen.blit(text4, (550, 160))

    def switch_col(self):
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def jump(self, j_vel):
        self.y = self.y + round(j_vel + 0.5 * self.gravity)
        self.j_vel = round(j_vel + self.gravity)

    def flatten(self):
        self.x -= self.width // 2
        self.y += self.height // 2
        self.height //= 2
        self.width *= 2
        self.is_flat = True

    def unflatten(self):
        self.x += self.width // 4
        self.y -= self.height
        self.height = 30
        self.width = 30
        self.is_flat = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.x - self.vel < 0:
                self.x = 0
            else:
                self.x -= self.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if (self.x + self.width) + self.vel > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.width
            else:
                box.x += box.vel
        # if keys[pygame.K_UP] or keys[pygame.K_w]:
        #     if self.y - self.vel < up_bound_y + bound_height:
        #         self.y = up_bound_y + bound_height
        #     else:
        #         self.y -= self.vel

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  #
            # print("Down")
            self.is_flat = True
            if self.height > 20:
                self.flatten()
        else:
            if self.is_flat:
                self.unflatten()

        if keys[pygame.K_c]:
            self.switch_col()

        if not self.isJump:
            self.gravity = 0
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                # self.switch_col()
                self.isJump = True
                self.j_vel = J_VEL
                self.gravity = GRAVITY
        else:
            self.jump(self.j_vel)
            if (self.y + self.height) + self.gravity > low_bound_y:  # Keeps above boundary
                self.y = low_bound_y - self.height
                self.j_vel = 0
                self.isJump = False

        self.hitbox = (self.x, self.y, self.width, self.height)


class Obstacle:
    def __init__(self, x, y, width, height, colour, typ):
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.typ = typ

    def reset(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def disp(self, screen):
        font = pygame.font.SysFont("comicsansms", 20)
        text1 = font.render(f"Obst_x: {self.x}", True, (255, 255, 255))
        screen.blit(text1, (550, 180))

    def upgrade_colour(self, speed, s1, s2, s3, s4, s5, s6):        # s = speed
        if s1 < speed <= s2:                # Lv1
            self.colour = (148, 255, 148)
        elif s2 < speed <= s3:              # Lv2
            self.colour = GREEN
        elif s3 < speed <= s4:              # Lv3
            self.colour = YELLOW
        elif s4 < speed <= s5:              # Lv4
            self.colour = ORANGE
        elif s5 < speed <= s6:              # Lv5
            self.colour = RED

    def move(self, speed):
        self.x -= OBST_SPEED
        self.hitbox = (self.x, self.y, self.width, self.height)

        if self.typ == 1 or self.typ == 2:
            self.upgrade_colour(speed, 7, 9, 11, 15, 18, 20)

    def is_collide(self, rect):
        #  rect is the hitbox of the player
        #  [1]       = top
        #  [1] + [3] = bottom
        #  [0]       = left
        #  [0] + [2] = right

        if self.hitbox[1] < rect[1] + rect[3] < self.hitbox[1] + self.hitbox[3] or self.hitbox[1] < rect[1] < \
                self.hitbox[1] + self.hitbox[3]:
            if (self.hitbox[0] < rect[0] < self.hitbox[0] + self.hitbox[2]) or (
                    self.hitbox[0] < rect[0] + rect[2] < self.hitbox[0] + self.hitbox[2]):
                return True
        return False

    def is_inside(self, rect):
        #  This method is used by the life force
        #  rect is the hitbox of the player
        #  [1]       = top
        #  [1] + [3] = bottom
        #  [0]       = left
        #  [0] + [2] = right

        if rect[1] < self.hitbox[1] + self.hitbox[3] < rect[1] + rect[3] or rect[1] < self.hitbox[1] < rect[1] + rect[3]:
            if (rect[0] < self.hitbox[0] < rect[0] + rect[2]) or (
                    rect[0] < self.hitbox[0] + self.hitbox[2] < rect[0] + rect[2]):
                return True
        return False


class Button:
    def __init__(self, x, y, width, height, bg_colour, text_colour, string, typ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_colour = bg_colour
        self.text_colour = text_colour
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.string = string
        self.text = 0
        self.typ = typ

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_colour, (self.x, self.y, self.width, self.height))

        self.text = self.font.render(self.string, True, self.text_colour)
        screen.blit(self.text, (self.x + self.width//2-self.text.get_width()//2, self.y + self.height//2-self.text.get_height()//2))

    def is_hover(self, mouse_x, mouse_y):
        if self.x < mouse_x < self.x + self.width:
            if self.y < mouse_y < self.y + self.height:
                return True
        return False

    def is_clicked(self, mouse_x, mouse_y):
        mouse_btns = pygame.mouse.get_pressed()
        if self.is_hover(mouse_x, mouse_y):
            if mouse_btns[0] == 1:
                return True
        return False

# ------- Game Functions -------


def print_score(score, screen):
    font = pygame.font.SysFont("comicsansms", 20)
    text1 = font.render(f"Score: {round(score)}", True, (255, 255, 255))
    text2 = font.render(f"High Score: {round(HIGHSCORE)}", True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))


def print_life(life, screen):
    font = pygame.font.SysFont("comicsansms", 20)
    text1 = font.render("Lives:", True, (255, 255, 255))
    screen.blit(text1, (630, 10))

    for i in range(0, life * 10, 10):
        pygame.draw.circle(screen, (255, 105, 180), (700 + 3*i, 25), 10)


def home_func(screen):
    global run
    global home
    global show_stat
    btn_stat_col = WHITE
    show_stat = False
    while home:
        screen.fill((0, 0, 0))

        font1 = pygame.font.SysFont("comicsansms", 70)
        font2 = pygame.font.SysFont("comicsansms", 30)
        font3 = pygame.font.SysFont("comicsansms", 20)
        text1 = font1.render("Box Runner", True, WHITE)
        text2 = font2.render("How to play", True, WHITE)
        text3 = font3.render("Press the 'left' and 'right' arrows to move in those directions", True, WHITE)
        text4 = font3.render("Press 'Space' or 'up' to jump over some obstacles", True, WHITE)
        text5 = font3.render("Hold down the 'down' arrow to flatten your character", True, WHITE)
        text6 = font3.render("You can press the 'Esc' or 'p' button to pause the game", True, WHITE)
        text7 = font3.render("When you are ready, press the big        button", True, WHITE)
        text8 = font3.render("RED", True, RED)
        text9 = font2.render("Options", True, WHITE)
        text10 = font3.render("Show Stats:", True, WHITE)
        if show_stat:
            text11 = font3.render("On", True, WHITE)
        else:
            text11 = font3.render("Off", True, WHITE)
        screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 15))
        screen.blit(text2, (30, 110))
        screen.blit(text3, (30, 160))
        screen.blit(text4, (30, 200))
        screen.blit(text5, (30, 240))
        screen.blit(text6, (30, 280))
        screen.blit(text7, (30, 320))
        screen.blit(text8, (360, 320))
        screen.blit(text9, (30, 370))
        screen.blit(text10, (30, 410))
        screen.blit(text11, (175, 410))

        btn_start = Button(630, 160, 150, 250, (170, 0, 0), WHITE, "Begin", 0)
        btn_stat = Button(153, 418, 14, 14, btn_stat_col, WHITE, "", 3)

        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        if btn_start.is_hover(mouse_x, mouse_y):
            btn_start.bg_colour = RED
        if btn_start.is_clicked(mouse_x, mouse_y):
            home = False
            run = True

        if btn_stat.is_hover(mouse_x, mouse_y) or show_stat:
            btn_stat_col = RED
        else:
            btn_stat_col = WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                home = False
                run = False
            if event.type == pygame.MOUSEBUTTONUP and btn_stat.is_hover(mouse_x, mouse_y):
                # The condition isn't exactly what I want because i can click and hold outside the button
                # and then release on the button
                btn_stat_col = RED
                if not show_stat:
                    show_stat = True
                else:
                    show_stat = False

        pygame.draw.rect(screen, WHITE, (150, 415, 20, 20))
        btn_start.draw(screen)
        btn_stat.draw(screen)
        pygame.display.update()


def pause_func(score, life, screen):
    global paused
    global show_stat
    btn_stat_col = WHITE
    while paused:
        screen.fill((75, 75, 75))
        col = get_col(OBST_SPEED, 7, 9, 11, 15, 18, 20)
        pygame.draw.rect(screen, col, (0, up_bound_y, SCREEN_WIDTH, bound_height))
        pygame.draw.rect(screen, col, (0, low_bound_y, SCREEN_WIDTH, bound_height))
        box.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        print_score(score, screen)
        print_life(life, screen)
        font = pygame.font.SysFont("comicsansms", 30)
        font2 = pygame.font.SysFont("comicsansms", 20)
        text1 = font.render("Press 'p' to continue...", True, (255, 255, 255))
        text2 = font2.render("Show Stats:", True, WHITE)
        if show_stat:
            text3 = font2.render("On", True, WHITE)
        else:
            text3 = font2.render("Off", True, WHITE)
        screen.blit(text1, (SCREEN_WIDTH // 2 - 170, 20))
        screen.blit(text2, (30, 420))
        screen.blit(text3, (175, 420))

        btn_stat = Button(153, 430, 14, 14, btn_stat_col, WHITE, "", 3)
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        if btn_stat.is_hover(mouse_x, mouse_y) or show_stat:
            btn_stat_col = RED
        else:
            btn_stat_col = WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
                global run
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = False
            if event.type == pygame.MOUSEBUTTONUP and btn_stat.is_hover(mouse_x, mouse_y):
                # The condition isn't exactly what I want because i can click and hold outside the button
                # and then release on the button
                btn_stat_col = RED
                if not show_stat:
                    show_stat = True
                else:
                    show_stat = False

        pygame.draw.rect(screen, WHITE, (150, 427, 20, 20))
        btn_stat.draw(screen)
        pygame.display.update()


def game_over_func(screen, score):
    global box
    del box     # First delete the box.
                # A new one will be made if the player wants to retry
    global end
    while not end:
        screen.fill((255, 0, 0))
        font = pygame.font.SysFont("comicsansms", 50)
        font2 = pygame.font.SysFont("comicsansms", 30)
        text1 = font.render("GAME OVER !", True, (255, 255, 255))
        text2 = font2.render("Would you like to try again?", True, (255, 255, 255))
        screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, SCREEN_HEIGHT // 2))
        print_score(score, screen)

        btn_yes = Button(SCREEN_WIDTH // 5, (SCREEN_HEIGHT // 3) * 2, 100, 50, BLACK, WHITE, "YES", 1)
        btn_no = Button((SCREEN_WIDTH // 5) * 4 - 50, (SCREEN_HEIGHT // 3) * 2, 100, 50, BLACK, WHITE, "NO", 2)
        # btn_yes.draw(screen)
        # btn_no.draw(screen)

        buttons = [btn_yes, btn_no]
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        # btn_yes.is_clicked(mouse_x, mouse_y) #
        for btn in buttons:
            if btn.is_hover(mouse_x, mouse_y):
                btn.bg_colour = (100, 100, 100)
                # print("Hovering")
            if btn.is_clicked(mouse_x, mouse_y):
                if btn.typ == 1:            # yes button
                    # reset the game
                    global run
                    global game_over
                    global start
                    run = True
                    game_over = False
                    start = True
                    end = True
                    # reset_game()
                elif btn.typ == 2:          # else the no button was pressed
                    end = True  # To get out of this loop after a btn is clicked

        btn_yes.draw(screen)
        btn_no.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True


def get_col(speed, s1, s2, s3, s4, s5, s6):
    if speed <= s1:
        return WHITE
    if s1 < speed <= s2:  # Lv1
        return (148, 255, 148)
    if s2 < speed <= s3:  # Lv2
        return GREEN
    if s3 < speed <= s4:  # Lv3
        return YELLOW
    if s4 < speed <= s5:  # Lv4
        return ORANGE
    if s5 < speed <= s6:  # Lv5
        return RED


def redraw_screen():
    if game_over:
        game_over_func(SCREEN, score_count)
    else:
        SCREEN.fill((0, 0, 0))
        col = get_col(OBST_SPEED, 7, 9, 11, 15, 18, 20)
        pygame.draw.rect(SCREEN, col, (0, up_bound_y, SCREEN_WIDTH, bound_height))
        pygame.draw.rect(SCREEN, col, (0, low_bound_y, SCREEN_WIDTH, bound_height))
        box.draw(SCREEN)

        for obstacle in obstacles:
            obstacle.draw(SCREEN)

        for life_force in life_forces:
            life_force.draw(SCREEN)

        # ----- Debug -----
        # font = pygame.font.SysFont("comicsansms", 20)
        # text1 = font.render(f"Obstacle Count: {obstacle_count}", True, (255, 255, 255))
        # text2 = font.render(f"x + width: {box.x + box.width}", True, (255, 255, 255))
        # text3 = font.render(f"Paused: {paused}", True, (255, 255, 255))
        # text4 = font.render(f"Life Force Count: {life_force_count}", True, (255, 255, 255))
        # screen.blit(text1, (200, 100))
        # screen.blit(text4, (200, 120))
        # screen.blit(text2, (550, 200))
        # screen.blit(text3, (550, 220))
        # -----       -----

        if show_stat:
            box.display_prop(SCREEN)
        print_score(score_count, SCREEN)
        print_life(life_count, SCREEN)

    pygame.display.update()


# ----------------------------

home_func(SCREEN)
while run:
    if start:
        # (Re)Setup
        score_count = 0
        life_count = 3
        box = Thing(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 30, 30, (255, 0, 0))
        obstacles = []
        obstacle_count = 0
        life_forces = []

        # User Events
        increase_obst_speed = pygame.USEREVENT + 1
        create_obst = pygame.USEREVENT + 2
        create_life = pygame.USEREVENT + 3
        pygame.time.set_timer(create_life, 40000)
        pygame.time.set_timer(increase_obst_speed, 8000)  # Every 8000ms, the 'increase_obst_speed' user event occurs
        S = int(((SCREEN_WIDTH / OBST_SPEED) / FPS) * 1000)  # S = time taken for obstacle to cross the screen in ms
        # I want the time it takes to create a new obstacle to be related to OBST_SPEED
        pygame.time.set_timer(create_obst, random.randrange(int(0.8 * S), S))

        # Loop
        clock = pygame.time.Clock()
        isJump = False
        start = False

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == increase_obst_speed:
            if OBST_SPEED < 20:
                OBST_SPEED += 1
                # Every time the speed increases, update the timer for the create_obst event
                # So the obstacles spawn faster as they move faster
                S = int(((SCREEN_WIDTH / OBST_SPEED) / FPS) * 1000)
                pygame.time.set_timer(create_obst, random.randrange(int(0.8 * S), S))
        if event.type == create_obst:
            obstacle_type = random.randint(1, 2)
            if obstacle_type == 1:
                obstacles.append(Obstacle(SCREEN_WIDTH, low_bound_y-60, 40, 60, WHITE, 1))
            elif obstacle_type == 2:
                obstacles.append(Obstacle(SCREEN_WIDTH, up_bound_y, 60, 311, WHITE, 2))
        if event.type == create_life:
            if life_count < 2:
                life_forces.append(Obstacle(SCREEN_WIDTH, low_bound_y - 20, 10, 10, (255, 105, 180), 3))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                paused = True
                pause_func(score_count, life_count, SCREEN)

    keys = pygame.key.get_pressed()

    box.move()

    # obstacle_count = len(obstacles)
    for obst in obstacles:
        obst.move(OBST_SPEED)

        # Delete obstacles when they leave the screen
        if obst.x + obst.width < 0:
            obstacles.pop(obstacles.index(obst))

        # Check for collisions
        if obst.is_collide(box.hitbox):
            life_count -= 1
            if life_count == 0:
                game_over = True
                run = False  #
                end = False  # So the game_over_func can actually execute
            pygame.time.delay(500)

            # Reset stuff if a collision occurs
            box.reset(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 30, 30, (255, 0, 0))
            OBST_SPEED //= 2
            if OBST_SPEED < 5:
                OBST_SPEED = 5
            S = int(((SCREEN_WIDTH / OBST_SPEED) / FPS) * 1000)
            pygame.time.set_timer(create_obst, random.randrange(int(0.8 * S), S))

            if obst.typ == 1:
                obst.reset(SCREEN_WIDTH, low_bound_y - 60, 40, 60)
            else:
                obst.reset(SCREEN_WIDTH, up_bound_y, 60, 311)
            obstacles.clear()

    # life_force_count = len(life_forces)
    for life_force in life_forces:
        life_force.move(OBST_SPEED)

        if life_force.is_inside(box.hitbox):
            life_count += 1
            life_forces.pop(life_forces.index(life_force))

        if life_force.x + life_force.width < 0:
            life_forces.pop(life_forces.index(life_force))

    score_count += 0.01 * OBST_SPEED
    if score_count > HIGHSCORE:
        HIGHSCORE = score_count

    redraw_screen()

pygame.quit()
