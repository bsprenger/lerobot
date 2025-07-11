from lerobot.common.datasets.lerobot_dataset import LeRobotDataset


def main():
    # dataset = LeRobotDataset(
    #     repo_id="bensprenger/lerobot_ppo_pendulum_v1",
    #     local_files_only=False,
    # )

    # print("done")

    dataset = LeRobotDataset(
        repo_id="lerobot/pusht",
    )
    print("hello")
    # dataset.repo_id = "bensprenger/pusht"
    # dataset.meta.repo_id = "bensprenger/pusht"

    # dataset.push_to_hub()


if __name__ == "__main__":
    main()
