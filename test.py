from player import *
from pivot import *



player1 = Player(195, 205)
pivot = Pivot(200, 200)
initial_angle = player1.angleToPivot(pivot)

player1.dx = 10
player1.dy = 10
player1.g = 10
angle = player1.highestAngle(pivot, 5 * (2**0.5))
print(math.degrees(angle))
amplitude = abs(math.degrees(angle) - (180 - math.degrees(angle)))/2

print(f'The player oscillates between {math.degrees(angle)} and {180 - math.degrees(angle)}, starting from {math.degrees(initial_angle)}, with an amplitude {amplitude}')