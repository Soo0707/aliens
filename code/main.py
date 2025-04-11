import pygame
from pytmx.util_pygame import load_pygame


class game():
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
    
    def setup(self):
        # TODO: load map textures, create player bla bla.
        pass

    def run(self):
        while self.running:
            # quits elegantly, never use this for player input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            pygame.display.flip() # draws

            dt = self.clock.tick(60) / 1000 # limits fps, dt can be used for fps independent physics

        pygame.quit()

if __name__ == "__main__":
    gaem = game()
    gaem.run()
