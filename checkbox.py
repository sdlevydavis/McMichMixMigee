import pygame


class Checkbox:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x+60, y+20, 15, 15)
        self.checked = False
        self.text = text
        self.select = 0

    def display(self, screen, font, mark_color=(0, 230, 0), box_color=(255, 255, 255)):
        pygame.draw.rect(screen, box_color, self.rect, 200)


        if self.checked:
            select_surface = font.render(str(self.select), True, (0, 0, 0))
            if self.select > 9:
                screen.blit(select_surface, (self.rect.left + 2, self.rect.top - 4))
            else:
                screen.blit(select_surface, (self.rect.left + 4, self.rect.top - 4))

        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.right + 10, self.rect.centery - 20 // 2))







