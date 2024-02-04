from flask import g

import random
import html

class HexagramGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[self._generate_hexagram() for _ in range(width)] for _ in range(height)]

    def _generate_hexagram(self):
        

        # Generate a random hexagram unicode character
        hexagram_code = random.choice(range(0x4DC0, 0x4DFF))
        hexagram = g.ic.Hexagram.from_unicode(chr(hexagram_code))

        return hexagram

    def get_cell(self, x, y, n):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None

        # Extract a section of the matrix centered at (x, y) with size n
        section = []
        for i in range(max(0, y - n), min(self.height, y + n + 1)):
            row = []
            for j in range(max(0, x - n), min(self.width, x + n + 1)):
                row.append(self.grid[i][j])
            section.append(row)

        return section

    def render(self):
        # Render the grid using HTML5 canvas object
        canvas = '<canvas id="hexagram-grid" width="{0}" height="{1}"></canvas>'.format(self.width * 20, self.height * 20)
        script = '''
        <script>
            var canvas = document.getElementById("hexagram-grid");
            var context = canvas.getContext("2d");
            var cellSize = 20;

            // Set up colors
            var colorMapping = {
                0: "white", 1: "brown", 2: "blue", 3: "red",
                4: "magenta", 5: "green", 6: "gray", 7: "orange"
            };

            // Render the grid
            
        </script>
        '''
        colorMapping = {
            0: "white", 1: "brown", 2: "blue", 3: "red",
            4: "magenta", 5: "green", 6: "gray", 7: "orange"
        }
        cellSize = 20
        draw_commands = []
        for y, row in enumerate(self.grid):
            for x, hx in enumerate(row):
                bgColor = hx.top_trigram.blend(hx.bottom_trigram)
                fgColor = hx.bottom_trigram.blend(hx.top_trigram)
                draw_commands.append('context.fillStyle = "{0}";'.format(bgColor))
                draw_commands.append('context.fillRect({0}, {1}, cellSize, cellSize);'.format(x * cellSize, y * cellSize))
                draw_commands.append('context.fillStyle = "{0}";'.format(fgColor))

                draw_commands.append('context.fillText("{0}", {1}, {2});'.format(html.escape(hx.character), x * cellSize, y * cellSize))

        return canvas + script + "<script> " + '\n'.join(draw_commands) + " </script>"