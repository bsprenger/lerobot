import sys
from dataclasses import dataclass

import numpy as np
import torch
from gym_pybullet_drones.control.DSLPIDControl import DSLPIDControl
from gym_pybullet_drones.utils.enums import DroneModel

import lerobot.configs.parser as parser
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
from lerobot.common.envs.configs import EnvConfig
from lerobot.common.envs.factory import make_env

sys.path.insert(0, "/home/bensprenger/lerobot/lerobot")

# TODO make it rain rubber ducks
# TODO make it follow a smooth trajectory


@dataclass
class CreateDatasetConfig:
    env: EnvConfig
    num_episodes: int = 1000
    seed: int = 42
    target_tolerance: float = 0.01
    velocity_tolerance: float = 0.01
    waypoint_distance: float = 0.05  # Distance between trajectory waypoints


def generate_smooth_trajectory(start_pos, end_pos, max_accel, dt=0.01):
    """
    Generate a smooth trajectory with constant acceleration/deceleration profile
    using proper kinematics equations.

    Args:
        start_pos: Starting position (numpy array)
        end_pos: Ending position (numpy array)
        max_accel: Maximum acceleration magnitude (constant positive in first half, negative in second)
        dt: Time step for trajectory points (default: 0.01s)

    Returns:
        pos: List of position waypoints
        vel: List of velocities at each waypoint
        acc: List of accelerations at each waypoint
    """
    # Calculate displacement vector
    displacement = end_pos - start_pos
    total_distance = np.linalg.norm(displacement)

    # Handle zero distance case
    if total_distance < 1e-6:
        return [start_pos], [np.zeros_like(start_pos)], [np.zeros_like(start_pos)]

    # Unit direction vector
    direction = displacement / total_distance

    # Calculate time needed for each phase (accelerate/decelerate)
    # Using s = 0.5*a*t² -> t = sqrt(2*s/a) for each half
    half_distance = total_distance / 2
    half_time = np.sqrt(2 * half_distance / max_accel)
    total_time = 2 * half_time

    # Calculate peak velocity (reached at midpoint)
    peak_velocity = max_accel * half_time

    # Calculate number of steps needed
    num_steps = max(int(np.ceil(total_time / dt)), 2)

    pos = []
    vel = []
    acc = []

    for i in range(num_steps):
        # Current time
        t = i * total_time / (num_steps - 1) if num_steps > 1 else total_time

        # Determine phase (acceleration or deceleration)
        if t <= half_time:
            # First half: constant positive acceleration
            # Position equation: x = x₀ + 0.5 * a * t²
            # Velocity equation: v = a * t
            current_acc = max_accel * direction
            current_vel = max_accel * t * direction
            current_pos = start_pos + 0.5 * max_accel * t * t * direction
        else:
            # Second half: constant negative acceleration
            # Adjust time relative to the start of second phase
            t2 = t - half_time

            # Use equations of motion with initial velocity = peak_velocity
            # Position: x = x_mid + v_peak*t - 0.5*a*t²
            # Velocity: v = v_peak - a*t
            current_acc = -max_accel * direction
            current_vel = (peak_velocity - max_accel * t2) * direction

            # Position at midpoint
            mid_pos = start_pos + half_distance * direction

            # Position equation for second half
            current_pos = mid_pos + peak_velocity * t2 * direction - 0.5 * max_accel * t2 * t2 * direction

        pos.append(current_pos)
        vel.append(current_vel)
        acc.append(current_acc)

    return pos, vel, acc


@parser.wrap()
def main(cfg: CreateDatasetConfig):
    np.random.seed(cfg.seed)

    env = make_env(cfg.env, n_envs=1)

    dataset = LeRobotDataset.create(
        "bensprenger/gym_pybullet_drones",
        fps=cfg.env.fps,
        features={
            "action": {"dtype": "float32", "shape": cfg.env.features["action"].shape},  # RPMs
            "observation.state": {"dtype": "float32", "shape": cfg.env.features["state"].shape},
            "next.success": {"dtype": "bool", "shape": (1,)},
            "observation.images.camera": {
                "dtype": "video",
                "shape": (3, 480, 640),
                "names": ["channel", "height", "width"],
            },
        },
    )

    for episode in range(cfg.num_episodes):
        ctrl = DSLPIDControl(drone_model=DroneModel.CF2X)
        obs, _ = env.reset()

        # Get starting position
        start_position = obs["agent_pos"][0, :3]

        # Generate a random target position within reasonable bounds
        end_position = np.random.uniform(low=[-1.5, -1.5, 0.1125], high=[1.5, 1.5, 1.6125], size=(3,))
        print(f"Episode {episode + 1}/{cfg.num_episodes}: Start: {start_position}, End: {end_position}")

        # Generate trajectory
        # Generate base trajectory
        pos, vel, acc = generate_smooth_trajectory(start_position, end_position, 3.0, 1 / cfg.env.fps)

        # Extend trajectories by 50 steps (you can make this configurable)
        extra_steps = 50
        final_pos = pos[-1]
        pos.extend([final_pos] * extra_steps)
        vel.extend([np.zeros_like(vel[0])] * extra_steps)
        acc.extend([np.zeros_like(acc[0])] * extra_steps)

        final_target_reached = False

        for p, v, _ in zip(pos, vel, acc, strict=True):
            action, _, _ = ctrl.computeControlFromState(
                control_timestep=1 / cfg.env.fps,
                state=obs["agent_pos"][0],
                target_pos=p,
                target_vel=v,
            )

            obs, reward, done, truncated, info = env.step(action.reshape(1, -1))

            if (
                np.linalg.norm(obs["agent_pos"][0, :3] - end_position) < cfg.target_tolerance
                and np.linalg.norm(obs["agent_pos"][0, 10:13]) < cfg.velocity_tolerance
            ):
                final_target_reached = True

            drone_view = env.envs[0].render()
            drone_view = np.transpose(drone_view, (2, 0, 1))

            frame = {
                "action": torch.tensor(action, dtype=torch.float32),
                "observation.state": torch.tensor(
                    np.concatenate([end_position - obs["agent_pos"][0, :3], obs["agent_pos"][0, 3:]]),
                    dtype=torch.float32,
                ),
                "next.success": torch.tensor([final_target_reached], dtype=torch.bool),
                "observation.images.camera": torch.tensor(drone_view, dtype=torch.uint8),
                "task": f"follow trajectory from {start_position} to {end_position}",
            }
            dataset.add_frame(frame)

            if final_target_reached or done or truncated:
                break

        dataset.save_episode()


if __name__ == "__main__":
    main()
