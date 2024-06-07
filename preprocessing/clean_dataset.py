import argparse
import json
from collections import defaultdict

import torch
import tqdm

from preprocessing.capivara_filter import capivara_filter
from preprocessing.duplication_handler import get_clusters, deduplicate
from preprocessing.feature_extraction import image_feature_extraction, text_feature_extraction


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", help="Path to dataset.json")
    parser.add_argument("--image-folder", help="Path to image folder")
    parser.add_argument("--gpu", help="GPU", )
    parser.add_argument("--clip-thr", type=float, default=0.2)

    return parser.parse_args()

def remove_duplicated_captions(dataset):
    d = defaultdict(lambda: [])
    for example in tqdm.tqdm(dataset, desc="Removing duplicated captions"):
        d[example["caption"].lower()].append(example)

    return [v[0] for v in d.values() if len(v[0]["caption"].split()) > 3]

if __name__ == "__main__":
    args = parse_args()
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    print("Device: ", device)
    print(args)

    with open(args.dataset_path) as file:
        dataset = json.load(file)

    dataset = remove_duplicated_captions(dataset)
    print("After dedup captions - size: ", len(dataset))
    dataset = capivara_filter(dataset, images_dir=args.image_folder, clip_thr=args.clip_thr,
                              device=device)
    print("After CAPIVARA Filter - size: ", len(dataset))
    with open("dataset_capivara.json", "w") as file:
        json.dump(dataset, file)


    print("Extracting image features...")
    image_features = image_feature_extraction(dataset, images_dir=args.image_folder, device=device)
    print("Extracting text features...")
    text_features = text_feature_extraction(dataset)

    print("Computing clusters...")
    clusters = get_clusters(image_features)
    print("Finding duplicates...")
    dedup_indices = deduplicate(image_features, text_features, clusters)
    dataset = [dataset[index] for index in dedup_indices]

    with open("clean_dataset.json", "w") as file:
        json.dump(dataset, file)

