import pygame, sys

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))

    def loop_with_logic(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                    or event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
            self.screen.fill((0, 0, 0))

if __name__ == "__main__":
    game = Game()
    game.loop_with_logic()