import pygame


class Checkbox:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.checked = False
        self.text = text

    def display(self, screen, font, mark_color=(0, 230, 0), box_color=(255, 255, 255)):
        pygame.draw.rect(screen, box_color, self.rect, 200)
        if self.checked:
            pygame.draw.line(screen, mark_color, self.rect.topleft, self.rect.bottomright)
            pygame.draw.line(screen, mark_color, self.rect.topright, self.rect.bottomleft)

        text_surface = font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.right + 10, self.rect.centery - 20 // 2))
