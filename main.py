# main.py - Multi-Ball Bouncing Simulation
# Features: multiple balls, shadows, color change on bounce, horizontal throws

from physics import simulate
from scene import create_scene


def run():
    print("=" * 40)
    print("  Bouncing Balls Simulation")
    print("=" * 40)

    # Run physics
    all_positions, all_bounces = simulate()

    # Create animated USD
    create_scene("output/bouncing_balls.usda", all_positions, all_bounces)

    print("\n" + "=" * 40)
    print("  Done!")
    print("=" * 40)
    print("\n  Open with:")
    print("    usdview output/bouncing_balls.usda")
    print("    Press 4, then Play!")


if __name__ == "__main__":
    run()
