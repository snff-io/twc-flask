from ast import Tuple
import random
import select
from attr import dataclass
import yaml
import yaml
import numpy as np
from matplotlib.pyplot import plot
from scipy.spatial import Delaunay
from db_iching_class import IChing, Trigram, Hexagram

class DelaunayArea:
    def __init__(self, size=None, points=None, tri=None, barycenters=None):
        self.size = None
        self.points = None
        self.tri = None
        self.barycenters = None

    def calculate_delauanay(self, size):
        self.size = size
        self.points = np.random.rand(self.size, 2) * self.size
        self.tri = Delaunay(self.points)
        self.barycenters = self.calculate_barycenters()

    def calculate_barycenters(self):
        barycenters = np.mean(self.points[self.tri.simplices], axis=1)
        distances = np.linalg.norm(barycenters, axis=1)
        sorted_indices = np.argsort(distances)
        return barycenters[sorted_indices]

    def get_neighbors(self, barycenter, num_neighbors):
        distances = np.linalg.norm(self.barycenters - barycenter, axis=1)
        sorted_indices = np.argsort(distances)
        return self.barycenters[sorted_indices[1:num_neighbors+1]]

    def resolve_xy(self, x, y):# -> Any:
        point = np.array([x, y])
        distances = np.linalg.norm(self.barycenters - point, axis=1)
        closest_index = np.argmin(distances)
        return self.barycenters[closest_index]

    def get_area(self, barycenter, area_size):
        distances = np.linalg.norm(self.barycenters - barycenter, axis=1)
        sorted_indices = np.argsort(distances)
        return self.barycenters[sorted_indices[:area_size]]

    def to_yaml(self, filepath):
        data = {
            'size': self.size,
            'points': self.points.tolist(),
            'tri': self.tri.simplices.tolist(),
            'barycenters': self.barycenters.tolist()
        }
        with open(filepath, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def from_yaml(filepath):
        with open(filepath, 'r') as file:
            data = yaml.load(file, Loader=yaml.Loader)
        delaunay_area = DelaunayArea()
        delaunay_area.size = data['size']
        delaunay_area.points = np.array(data['points'])
        delaunay_area.tri = Delaunay(np.array(data['tri']))
        delaunay_area.barycenters = np.array(data['barycenters'])
        return delaunay_area

@dataclass
class EnergyPoint:
    x:int = None
    y:int = None
    h:Hexagram = None

    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
   


class EnergyMap:

    energy_points = {}

    def __init__(self, points):
        self.points = points
        
    def seed_energy(self):
        ic = IChing()
        i = 0
        for p in self.points:
            h = random.choice(ic.hexagrams).color_hex
            self.energy_points[i] = EnergyPoint(p[0], p[1], h)
            i += 1

    def get_seed_energy(self, point):
        i = self.points.index(point)
        return self.energy_points[i]
    
__all__ = ['DelaunayArea', 'EnergyMap', EnergyPoint]