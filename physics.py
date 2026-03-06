# physics.py - Multi-ball physics with Warp
# Each ball has 3D position and velocity
# Balls bounce off floor and change color

import warp as wp
import numpy as np
import config

wp.init()

@wp.kernel
def update_balls(
    positions: wp.array(dtype=wp.vec3),
    velocities: wp.array(dtype=wp.vec3),
    bounce_counts: wp.array(dtype=int),
    gravity: float,
    dt: float,
    floor_y: float,
    ball_radius: float,
    bounce_factor: float,
):
    """Update each ball: apply gravity, move, check floor bounce."""
    i = wp.tid()

    pos = positions[i]
    vel = velocities[i]

    # Apply gravity (only Y axis)
    vel = wp.vec3(vel[0], vel[1] + gravity * dt, vel[2])

    # Move ball in 3D
    new_pos = pos + vel * dt

    # Floor bounce
    if new_pos[1] - ball_radius < floor_y:
        new_pos = wp.vec3(new_pos[0], floor_y + ball_radius, new_pos[2])
        vel = wp.vec3(vel[0] * 0.98, -vel[1] * bounce_factor, vel[2] * 0.98)
        bounce_counts[i] = bounce_counts[i] + 1

    positions[i] = new_pos
    velocities[i] = vel


def simulate():
    """Run simulation for all balls.
    Returns: positions[frame][ball] and bounce_counts[frame][ball]"""
    device = "cpu"
    n = config.NUM_BALLS

    # Initialize positions and velocities from config
    init_pos = []
    init_vel = []
    for b in config.BALLS:
        init_pos.append(wp.vec3(b[0], b[1], b[2]))
        init_vel.append(wp.vec3(b[3], 0.0, b[4]))

    positions = wp.array(init_pos, dtype=wp.vec3, device=device)
    velocities = wp.array(init_vel, dtype=wp.vec3, device=device)
    bounce_counts = wp.zeros(n, dtype=int, device=device)

    all_positions = []
    all_bounces = []

    print(f"Simulating {n} balls for {config.TOTAL_FRAMES} frames...")
    for frame in range(config.TOTAL_FRAMES):
        # Save state
        pos_np = positions.numpy()
        bounce_np = bounce_counts.numpy()

        frame_pos = []
        frame_bounces = []
        for i in range(n):
            p = pos_np[i]
            frame_pos.append((float(p[0]), float(p[1]), float(p[2])))
            frame_bounces.append(int(bounce_np[i]))

        all_positions.append(frame_pos)
        all_bounces.append(frame_bounces)

        # Update physics
        wp.launch(update_balls, dim=n,
                  inputs=[positions, velocities, bounce_counts,
                          config.GRAVITY, config.TIME_STEP,
                          0.0, config.BALL_RADIUS, config.BOUNCE_FACTOR],
                  device=device)
        wp.synchronize()

        if (frame + 1) % 60 == 0:
            print(f"  Frame {frame+1}/{config.TOTAL_FRAMES}")

    return all_positions, all_bounces
