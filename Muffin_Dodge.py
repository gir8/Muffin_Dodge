import pygame
from sys import exit
from random import randrange


class Muffin_Maker_2000:
    score = 0

    def __init__(self):
        self.muffin_xpos = randrange(850, 1300, 50)
        self.muffin_ypos = randrange(40, 300, 20)
        self.muffin_rotating = randrange(1, 46)
        self.muffin_flight_speed_velocity = randrange(2, 6)
        self.muffin = pygame.image.load(f"graphics/muffin/muffin_{self.muffin_rotating}.png").convert_alpha()
        self.muffin_rectangle = self.muffin.get_rect(midbottom=(self.muffin_xpos, self.muffin_ypos))

    def muffin_movement(self):
        if self.muffin_xpos > -22:
            self.muffin_rotating += 1
            if self.muffin_rotating > 46:
                self.muffin_rotating = 1
            self.muffin_xpos -= self.muffin_flight_speed_velocity
            self.muffin = pygame.image.load(f"graphics/muffin/muffin_{self.muffin_rotating}.png").convert_alpha()
        if self.muffin_xpos <= -22:
            Muffin_Maker_2000.score += 1
            self.muffin_xpos = randrange(850, 1300, 50)
            self.muffin_ypos = randrange(40, 300, 20)
            self.muffin_flight_speed_velocity = randrange(2, 6)
        self.muffin_rectangle = self.muffin.get_rect(midbottom=(self.muffin_xpos, self.muffin_ypos))


class Player:
    def __init__(self):
        self.player_gravity = 0
        self.jump_toggle = 0
        self.jump_force = 14
        self.player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
        self.player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        self.player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [self.player_walk_1, self.player_walk_2, self.player_walk_1, self.player_stand, self.player_stand]
        self.player_walk_index = 0
        self.player_crouch = pygame.image.load("graphics/player/player_crouch.png").convert_alpha()
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_rectangle = self.player_stand.get_rect(midbottom=(50, 300))

    def move(self, coord, key=None):
        if self.player_rectangle.bottom >= 300 and key is None:
            self.player_walk_index = 0
            self.player_rectangle = self.player_stand.get_rect(midbottom=coord)
        elif key == "K_Left":
            self.player_walk_index -= 0.04
            if self.player_walk_index < -0.5:
                self.player_walk_index = 4
            self.player_rectangle = self.player_walk[int(self.player_walk_index)].get_rect(midbottom=coord)
        elif key == "K_Right":
            self.player_walk_index += 0.05
            if self.player_walk_index > 4.4:
                self.player_walk_index = 0
            self.player_rectangle = self.player_walk[int(self.player_walk_index)].get_rect(midbottom=coord)
        elif key == "K_Down":
            self.player_walk_index = 0
            self.player_rectangle = self.player_crouch.get_rect(midbottom=coord)
        elif self.player_rectangle.bottom < 300 and key == "K_Space":
            self.player_walk_index = 0
            self.player_rectangle = self.player_jump.get_rect(midbottom=coord)


class Muffin_Dodge:
    def __init__(self):
        # setup
        pygame.init()
        pygame.display.set_caption("Muffin Dodge")
        self.screen = pygame.display.set_mode((800, 400))
        self.clock = pygame.time.Clock()
        self.game_active = 1

        # text setup
        self.title = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.game_menu_txt = pygame.font.Font("font/Pixeltype.ttf", 100)
        self.text_surface = self.title.render("Muffin Dodge", False, "#00DD22")
        self.text_surface_rectangle = self.text_surface.get_rect(midtop=(400, 0))
        self.game_over = self.game_menu_txt.render("Game Over", False, "#FF0000")
        self.game_over_rectangle = self.game_over.get_rect(midtop=(400, 75))
        self.new_game = self.title.render("Press Enter", False, "#FF0000")
        self.new_game_rectangle = self.new_game.get_rect(midtop=(400, 200))

        # stage setup
        self.sky = pygame.image.load("graphics/sky.png").convert_alpha()
        self.ground = pygame.image.load("graphics/ground.png").convert_alpha()

        # object creation
        self.muffin_1 = Muffin_Maker_2000()
        self.muffin_2 = Muffin_Maker_2000()
        self.muffin_3 = Muffin_Maker_2000()
        self.player = Player()

        # Game
        self.start()

    def score_chart(self):
        score = Muffin_Maker_2000.score
        if self.game_active:
            game_score = self.title.render(f"{score}", False, "#000000")
            game_score_rectangle = game_score.get_rect(midtop=(400, 50))
        else:
            game_score = self.title.render(f"Score: {score}", False, "#FF0000")
            game_score_rectangle = game_score.get_rect(midtop=(400, 300))
        self.screen.blit(game_score, game_score_rectangle)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    # prevents pressing space while in air
                    if event.key == pygame.K_SPACE:
                        self.player.jump_toggle += 1
                    # start again
                    if self.game_active == 0 and event.key == pygame.K_RETURN:
                        Muffin_Maker_2000.score = 0
                        self.game_active = 1
                        self.muffin_1 = Muffin_Maker_2000()
                        self.muffin_2 = Muffin_Maker_2000()
                        self.muffin_3 = Muffin_Maker_2000()
                        self.player = Player()
            if self.game_active:
                # drawing stage
                self.screen.blit(self.sky, (0, 0))
                self.screen.blit(self.ground, (0, 300))

                # drawing text
                self.screen.blit(self.text_surface, (300, 20))

                # player moving
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    if self.player.player_rectangle.bottom < 300 or (
                            self.player.player_rectangle.bottom >= 300 and (not keys[pygame.K_DOWN])):
                        if (self.player.player_rectangle.left - 5) > 0:
                            self.player.player_rectangle.left -= 5
                        else:
                            self.player.player_rectangle.left = 0
                        if self.player.player_rectangle.bottom >= 300:
                            self.player.move(self.player.player_rectangle.midbottom, key="K_Left")
                            self.screen.blit(self.player.player_walk[int(self.player.player_walk_index)],
                                             self.player.player_rectangle)

                if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    if self.player.player_rectangle.bottom < 300 or (
                            self.player.player_rectangle.bottom >= 300 and (not keys[pygame.K_DOWN])):
                        if (self.player.player_rectangle.right + 5) < 800:
                            self.player.player_rectangle.x += 5
                        else:
                            self.player.player_rectangle.right = 800
                        if self.player.player_rectangle.bottom >= 300:
                            self.player.move(self.player.player_rectangle.midbottom, key="K_Right")
                            self.screen.blit(self.player.player_walk[int(self.player.player_walk_index)],
                                             self.player.player_rectangle)

                if keys[pygame.K_SPACE] and self.player.jump_toggle == 1:
                    # player jumping
                    if (self.player.player_rectangle.bottom - self.player.jump_force) < 300 and (
                            self.player.jump_force - .4) >= 0:
                        self.player.player_gravity = 0
                        self.player.player_rectangle.bottom -= self.player.jump_force
                        self.player.jump_force -= .4
                        if not keys[pygame.K_DOWN]:
                            self.player.move(self.player.player_rectangle.midbottom, key="K_Space")
                            self.screen.blit(self.player.player_jump, self.player.player_rectangle)
                    # player gravity
                    elif (self.player.player_rectangle.bottom + (self.player.player_gravity + 0.4)) < 300:
                        self.player.player_gravity += 0.4
                        self.player.player_rectangle.bottom += self.player.player_gravity
                        if not keys[pygame.K_DOWN]:
                            self.player.move(self.player.player_rectangle.midbottom, key="K_Space")
                            self.screen.blit(self.player.player_jump, self.player.player_rectangle)
                    # player lands
                    elif (self.player.player_rectangle.bottom + (self.player.player_gravity + 0.4)) >= 300:
                        self.player.player_rectangle.bottom = 300
                        self.player.player_gravity = 0
                        self.player.jump_force = 14
                        if not keys[pygame.K_DOWN]:
                            self.player.move(self.player.player_rectangle.midbottom, key=None)
                            self.screen.blit(self.player.player_jump, self.player.player_rectangle)

                # player crouching
                if keys[pygame.K_DOWN]:
                    self.player.move(self.player.player_rectangle.midbottom, key="K_Down")
                    self.screen.blit(self.player.player_crouch, self.player.player_rectangle)

                # player gravity
                if (self.player.player_rectangle.bottom + (self.player.player_gravity + 0.4)) < 300:
                    self.player.player_gravity += 0.4
                    self.player.player_rectangle.bottom += self.player.player_gravity
                    if not keys[pygame.K_DOWN]:
                        self.player.move(self.player.player_rectangle.midbottom, key="K_Space")
                        self.screen.blit(self.player.player_jump, self.player.player_rectangle)

                # player lands
                if ((self.player.player_rectangle.bottom + (self.player.player_gravity + 0.4)) >= 300) or (self.player.player_rectangle.bottom >= 300):
                    self.player.player_rectangle.bottom = 300
                    self.player.player_gravity = 0
                    self.player.jump_force = 14
                    self.player.jump_toggle = 0
                    if (not keys[pygame.K_DOWN]) and (not keys[pygame.K_LEFT]) and (not keys[pygame.K_RIGHT]):
                        self.player.move(self.player.player_rectangle.midbottom, key=None)
                        self.screen.blit(self.player.player_stand, self.player.player_rectangle)
                    elif keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                        self.player.move(self.player.player_rectangle.midbottom, key=None)
                        self.screen.blit(self.player.player_stand, self.player.player_rectangle)

                # drawing enemies
                self.screen.blit(self.muffin_1.muffin, self.muffin_1.muffin_rectangle)
                self.screen.blit(self.muffin_2.muffin, self.muffin_2.muffin_rectangle)
                self.screen.blit(self.muffin_3.muffin, self.muffin_3.muffin_rectangle)
                self.muffin_1.muffin_movement()
                self.muffin_2.muffin_movement()
                self.muffin_3.muffin_movement()

                # score
                self.score_chart()

                # collisions
                if self.player.player_rectangle.colliderect(
                        self.muffin_1.muffin_rectangle) or self.player.player_rectangle.colliderect(
                        self.muffin_2.muffin_rectangle) or self.player.player_rectangle.colliderect(
                        self.muffin_3.muffin_rectangle):
                    self.game_active = 0
            else:
                # Game Over
                self.screen.fill("#440000")
                self.screen.blit(self.game_over, self.game_over_rectangle)
                self.screen.blit(self.new_game, self.new_game_rectangle)
                self.score_chart()

            pygame.display.update()
            self.clock.tick(60)


play_game = Muffin_Dodge()
