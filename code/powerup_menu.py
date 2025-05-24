import pygame
import random

class Powerup_Menu:
    def __init__(self, powerup_list, powerups, powerup_timers, powerup_definitions): #add powerup as attribute when done
        pygame.font.init()
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 40)
        self.left = 215
        self.top = 85
        
        #control
        self.powerup_list = powerup_list
        self.powerups = powerups
        self.powerup_timers = powerup_timers
        self.powerup_definitions = powerup_definitions
        self.general_options = random.sample(self.powerup_list, 3)
        self.general_index = {'col': 0, 'row': 0}
        
    def input(self):
        #The codes below are for knowing which "button" we are on
        keys = pygame.key.get_just_pressed()
        self.general_index['row'] = (self.general_index['row'] + int(keys[pygame.K_s]) - int(keys[pygame.K_w])) % 3
        self.general_index['col'] = (self.general_index['col'] + int(keys[pygame.K_d]) - int(keys[pygame.K_a])) % 1
        if keys[pygame.K_SPACE]:
            powerup = self.general_options[self.general_index['row']] # this equation will change depending on the equation for index
            self.apply_powerups(powerup=powerup)
            
        
    def general(self):
        #background
        bg = pygame.Surface((1280,720))
        bg.set_alpha(128)
        bg.fill((0, 0, 0))
        self.display_surface.blit(bg, (0,0))
        rect = pygame.FRect(self.left, self.top, 850, 550)
        pygame.draw.rect(self.display_surface, 'light gray', rect, 0, 4)
        pygame.draw.rect(self.display_surface, 'gray', rect, 4, 4)
        
        #menu
        cols, rows = 1, 3
        for col in range(cols):
            for row in range(rows):
                x = rect.left + rect.width / 5
                y = rect.top + (rect.height / 4) + (rect.height / 4) * row
                i = row     #the equation for i/index will change depending on the amount of rows and columns
                a = rect.left + 3.7 * rect.width / 5
                if col == self.general_index['col'] and row == self.general_index['row']: 
                    color = pygame.Color(190, 190, 190, 255)
                else: 
                    color = pygame.Color(0, 0, 0, 255),
                
                text_surf = self.font.render(self.general_options[i], True, color)
                #desc powerups surface
                powerup_name = self.general_options[i]
                desc = self.powerup_definitions[powerup_name]
                desc_surf = self.font.render(desc, True, (0, 0, 0, 255)) #<---- need to change font color
                
                text_rect = text_surf.get_frect(center = (x,y))
                #desc powerups rect
                desc_rect = desc_surf.get_frect(center = (a,y))
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(desc_surf, desc_rect)
                
    def update(self):
        self.input()
        if self.powerups["done"]: 
            self.general_options = random.sample(self.powerup_list, 3)

    def apply_powerups(self, powerup):
        if powerup in self.powerups:
            if powerup == "Milk":
                self.powerup_timers["Milk"] = pygame.time.get_ticks() + 100000
            elif powerup == "Lazers":
                self.powerups["Lazers"][0] += 1 # width
                if self.powerups["Lazers"][1] - 100 > 0:
                    self.powerups["Lazers"][1] -= 100 # cooldown
            elif powerup == "Projectiles":
                self.powerups["Projectiles"][0] += 100 # speed
                if self.powerups["Projectiles"][1] - 10 > 0:
                    self.powerups["Projectiles"][1] -= 100 # cooldown
            elif powerup == "Buckshot":
                self.powerups["Buckshot"] += 1
            elif powerup == "Greenbull":
                self.powerup_timers["Greenbull"] = pygame.time.get_ticks() + 100000
            elif powerup == "Magnetism":
                self.powerup_timers["Magnetism"] = pygame.time.get_ticks() + 100000
            elif powerup == "Aura":
                self.powerups["Aura"][0] += 200
                self.powerups["Aura"][1] += 200
            elif powerup == "Block Breaker":
                self.powerup_timers = pygame.time.get_ticks() + 5000
            else:
                self.powerups[powerup] += 1
        else:
            if powerup == "Blood Sacrifice":
                self.powerups["Blood Sacrifice"] = 0
                self.powerup_timers["Blood Sacrifice"] = pygame.time.get_ticks() + 1000
            elif powerup == "Greenbull":
                self.powerups["Greenbull"] = 0
                self.powerup_timers["Greenbull"] = pygame.time.get_ticks() + 100000
            elif powerup == "Milk":
                self.powerups["Milk"] = 0
                self.powerup_timers["Milk"] = pygame.time.get_ticks() + 100000
                
                if "Drunk" in self.powerups:
                    del self.powerups["Drunk"]

                if "Aussie" in self.powerups:
                    del self.powerups["Aussie"]
                
                if "Poison" in self.powerups:
                    del self.powerups["Poison"]
            elif powerup == "Magnetism":
                self.powerups["Magnetism"] = 0
                self.powerup_timers["Magnetism"] = pygame.time.get_ticks() + 100000
            elif powerup == "Block Breaker":
                self.powerups["Block Breaker"] = 0
                self.powerup_timers = pygame.time.get_ticks() + 5000
            else:
                self.powerups[powerup] = 0

        self.powerups["done"] = 1



