# config.py - Bouncing Ball Settings

# Multiple balls
NUM_BALLS = 5
BALL_RADIUS = 0.25

# Ball starting positions and velocities
# Each ball: (start_x, start_height, start_z, vel_x, vel_z)
BALLS = [
    (0.0,  6.0, 0.0,  0.0,  0.0),    # center, straight drop
    (-2.0, 8.0, 0.0,  1.5,  0.0),    # left, thrown right
    (2.0,  7.0, 0.0, -1.0,  0.5),    # right, thrown left
    (0.0,  5.0, 2.0,  0.5, -1.0),    # back, thrown forward
    (-1.0, 9.0, -1.0, 0.8,  0.8),    # high throw diagonal
]

# Ball colors (will change on bounce)
BALL_COLORS = [
    (0.9, 0.1, 0.1),   # red
    (0.1, 0.9, 0.1),   # green
    (0.1, 0.1, 0.9),   # blue
    (0.9, 0.9, 0.1),   # yellow
    (0.9, 0.1, 0.9),   # purple
    (0.1, 0.9, 0.9),   # cyan
    (1.0, 0.5, 0.0),   # orange
    (1.0, 1.0, 1.0),   # white
]

# Floor
FLOOR_SIZE = 8.0
FLOOR_COLOR = (0.3, 0.3, 0.3)

# Physics
GRAVITY = -9.81
BOUNCE_FACTOR = 0.75
TIME_STEP = 1.0 / 60.0

# Animation
TOTAL_FRAMES = 360
FPS = 60
