from pathlib import Path

import pyarrow.dataset as ds
from datasets import Dataset, load_dataset

from lerobot.common.datasets.lerobot_dataset import LeRobotDataset


def gen_from_parquet(path, partition_format="hive"):
    # Create PyArrow dataset from parquet files
    pa_dataset = ds.dataset(path, format="parquet", partitioning=partition_format)

    # Iterate through batches
    # idx = 0
    for batch in pa_dataset.to_batches():
        # Convert batch to list of dictionaries
        records = batch.to_pylist()
        yield from records


# # Create a map-style Hugging Face dataset
# dataset = Dataset.from_generator(
#     gen_from_parquet, gen_kwargs={"dataset_path": "dataset_name/", "partition_format": "hive"}
# )


def main():
    # Load dataset normally
    path = Path("/home/bsprenge/.cache/huggingface/lerobot/bensprenger/my_partitioned_dataset")
    dataset = load_dataset("parquet", data_dir=path, split="train")

    # Load dataset from parquet files
    partitioned_dataset = Dataset.from_generator(
        gen_from_parquet,
        gen_kwargs={"path": path, "partition_format": "hive"},
    )
    print(partitioned_dataset)


def load_lerobot_dataset(path, episodes):
    dataset = LeRobotDataset(path, episodes=episodes)
    return dataset


if __name__ == "__main__":
    # main()
    load_lerobot_dataset("bensprenger/pusht", episodes=[1, 2, 3])
