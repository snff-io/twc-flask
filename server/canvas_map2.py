import random

class CanvasGrid:
    def __init__(self, trigrams, colors, blending=False):
        self.trigrams = trigrams
        self.colors = colors
        self.blending = blending

    def get_cell(self, x, y, n):
        upper_trigram = random.choice(self.trigrams)
        lower_trigram = random.choice(self.trigrams)
        foreground_color = self.colors[upper_trigram]
        background_color = self.colors[lower_trigram]

        if self.blending:
            foreground_color = self.blend_colors(foreground_color, background_color)
            background_color = self.blend_colors(background_color, foreground_color)

        return {
            'x': x,
            'y': y,
            'n': n,
            'foreground_color': foreground_color,
            'background_color': background_color
        }

    def draw_cell(self, cell):
        # Draw the cell on the HTML canvas
        pass

    def blend_colors(self, color1, color2):
        # Blend two colors together
        pass
