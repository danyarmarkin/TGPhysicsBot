from math import *

class Ballistics:
    # g = 10
    # alpha = 0
    # startSpeed = 0
    # startHeight = 0
    def __init__(self, startSpeed, startHeight, alpha, g):
        try:
            self.startSpeed = startSpeed
            self.startHeight = startHeight
            self.alpha = alpha
            self.g = g
            self.sinAlpha = sin(radians(self.alpha))
            self.sin2Alpha = sin(radians(2 * self.alpha))
            self.cosAlpha = cos(radians(self.alpha))
            self.maxHeight = self.startHeight + (self.startSpeed**2 * self.sinAlpha * self.sinAlpha) / (2 * self.g)
            self.time = ((self.startSpeed * self.sinAlpha) / self.g + sqrt((2 * self.maxHeight) / self.g))
            if self.alpha == 90 or self.alpha == 270:
                self.len = 0
            else:
                self.len = ((self.startSpeed**2 * self.sin2Alpha) / (2 * g) + self.startSpeed * self.cosAlpha * sqrt((2 * self.maxHeight) / self.g))

            self.endSpeed = sqrt((self.startSpeed * self.cosAlpha) * (self.startSpeed * self.cosAlpha) + (self.g * sqrt((2 * self.maxHeight) / self.g)) * (self.g * sqrt((2 * self.maxHeight) / self.g)))
            self.phi = degrees(atan((self.g * sqrt((2 * self.maxHeight) / self.g)) / (self.startSpeed * self.cosAlpha)))

            self.phi = round(self.phi, 3)
            self.endSpeed = round(self.endSpeed, 3)
            self.maxHeight = round(self.maxHeight, 3)
            self.len = round(self.len, 3)
            self.time = round(self.time, 3)
        except OverflowError:
            self.phi = 0
            self.endSpeed = 0
            self.maxHeight = 0
            self.len = 0
            self.time = 0

