from lerobot.common.datasets.lerobot_dataset import LeRobotDataset


def main():
    ds = LeRobotDataset("bensprenger/pusht")
    print(len(ds))


if __name__ == "__main__":
    main()
