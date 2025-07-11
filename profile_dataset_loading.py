#!/usr/bin/env python

import gc
import statistics
import time

import torch

from lerobot.common.datasets.lerobot_dataset import LeRobotDataset


def profile_dataset_loading(repo_id, num_runs=5):
    """Profile the loading time of a dataset."""
    loading_times = []

    for i in range(num_runs):
        print(f"Run {i + 1}/{num_runs} for {repo_id}")

        # Free memory before loading
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Measure loading time
        start_time = time.time()
        dataset = LeRobotDataset(repo_id=repo_id)
        end_time = time.time()

        loading_time = end_time - start_time
        loading_times.append(loading_time)

        print(f"  Loading time: {loading_time:.2f} seconds")

        # Access a few items to ensure everything is loaded
        for idx in [0, min(10, len(dataset) - 1), min(100, len(dataset) - 1)]:
            if idx < len(dataset):
                _ = dataset[idx]

        # Clean up
        del dataset
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

        # Short pause between runs
        time.sleep(1)

    return loading_times


def main():
    # Datasets to profile
    # datasets = ["bensprenger/aloha_mobile_cabinet", "bensprenger/aloha_mobile_cabinet2"]
    datasets = ["bensprenger/aloha_mobile_cabinet2"]

    num_runs = 5  # Number of runs per dataset
    results = {}

    print("Starting dataset loading profiling...")

    for repo_id in datasets:
        print(f"\nProfiling {repo_id}...")
        loading_times = profile_dataset_loading(repo_id, num_runs)
        results[repo_id] = loading_times

    # Print results
    print("\n" + "=" * 60)
    print("DATASET LOADING PROFILE RESULTS")
    print("=" * 60)

    for repo_id, times in results.items():
        avg_time = statistics.mean(times)
        if len(times) > 1:
            std_dev = statistics.stdev(times)
            print(f"{repo_id}:")
            print(f"  Runs: {len(times)}")
            print(f"  Average loading time: {avg_time:.2f} seconds")
            print(f"  Standard deviation: {std_dev:.2f} seconds")
            print(f"  Min: {min(times):.2f} seconds")
            print(f"  Max: {max(times):.2f} seconds")
        else:
            print(f"{repo_id}:")
            print(f"  Runs: {len(times)}")
            print(f"  Loading time: {avg_time:.2f} seconds")
        print("-" * 60)


if __name__ == "__main__":
    main()
