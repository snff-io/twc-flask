from dataclasses import dataclass
from termios import TIOCPKT_START
from typing import Any, List
import math

#create domain -> color mapping

@dataclass
class Trigram:  
    number: int
    names: List[str]
    chineseName: str
    pinyinName: str
    character: str
    attribute: str
    images: List[str]
    chineseImage: str
    pinyinImage: str
    familyRelationship: str
    binary: str
    lines: List[int]

    @property
    def bin(self):
        return int(self.binary, 2)
    @property
    def domain(self):
        return self.images[0]
    
    @property 
    def color_hex(self):
        return self.bin << 5
    
    @staticmethod
    def color_domain_map():
        return {
            'heaven':   '#FFFFFF',
            'thunder':  '#FFFF00',
            'earth':    '#AAAAAA',
            'water':    '#00FFFF',
            'fire':     '#FF0000',
            'swamp':    '#008000',
            'mountain': '#FF00FF',
            'wind':     '#00FFFF',
        }

    #todo: add a property for the color of the trigram's domain
    @property
    def color_domain(self):
        mapping=Trigram.color_domain_map()

        return mapping[self.domain]

    @property
    def color_hex(self):
        return self.color_domain    


    def blend(self, other) -> str:
    
        self_color = self.color_domain
        other_color = other.color_domain

        # Blend the color domains by averaging the RGB values
        blended_color = '#'
        for i in range(1, 7, 2):
            self_rgb = int(self_color[i:i+2], 16)
            other_rgb = int(other_color[i:i+2], 16)
            blended_rgb = math.floor((self_rgb + other_rgb) / 2)
            blended_color += f'{blended_rgb:02x}'

        return blended_color
    
    @staticmethod
    def unicode_trigram_list():
        ret = []
        for i in range(0x2630, 0x2637 + 1):
            ret.append(chr(i))
        
@dataclass
class Hexagram:
    number: int
    names: List[str]
    chineseName: str
    pinyinName: str 
    character: str
    binary: str
    lines: List[int]    
    topTrigram: int
    bottomTrigram: int
    top_trigram: 'Trigram'
    bottom_trigram: 'Trigram'

    @property
    def color_hex(self):
        return self.top_trigram.blend(self.bottom_trigram)

    @staticmethod
    def unicode_hexagram_list(index=None):
        ret = []
        for i in range(0x4DC0, 0x4DFF + 1):
            ret.append(chr(i))

        if index is not None:
            return ret[index]   
        return ret

@dataclass
class Nonagram:
    number: int
    names: List[str]
    chineseName: str
    pinyinName: str 
    character: str
    binary: str
    lines: List[int]    
    topTrigram: int
    bottomTrigram: int
    top_trigram: 'Trigram'
    bottom_trigram: 'Trigram'
    middleTrigram: int
    middle_trigram: 'Trigram'    


    @property
    def color_hex(self):
        r = self.top_trigram.color_hex      #| self.top_trigram.bin
        g = self.middle_trigram.color_hex   #| self.middle_trigram.bin
        b = self.bottom_trigram.color_hex   #| self.bottom_trigram.bin
        return f'#{r:02x}{g:02x}{b:02x}'

__all__ = ['Trigram', 'Hexagram', 'Nonagram']
