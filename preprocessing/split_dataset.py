import random
from collections import defaultdict


def group_by_user(dataset):
    groups = defaultdict(lambda: [])
    for example in dataset:
        user = example['user']
        groups[user].append(example)

    return groups


def split_dataset(dataset, train_size=0.6, test_size=0.2):
    total_size = len(dataset)
    groups = group_by_user(dataset)
    save_dataset = {"train": [],
                    "validation": [],
                    "test": []}

    while len(save_dataset["train"]) / total_size < train_size and len(groups) > 0:
        examples = groups.pop(random.choice(list(groups.keys())))
        save_dataset["train"].extend(examples)

    while len(save_dataset["test"]) / total_size < test_size and len(groups) > 0:
        examples = groups.pop(random.choice(list(groups.keys())))
        save_dataset["test"].extend(examples)

    while len(groups) > 0:
        _, examples = groups.popitem()
        save_dataset["validation"].extend(examples)
