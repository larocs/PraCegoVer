import argparse
import json
import os
from collections import defaultdict
import tqdm
import open_clip
import torch
import PIL
from preprocessing.feature_extraction import image_feature_extraction, text_feature_extraction
from preprocessing.duplication_handler import get_clusters, deduplicate


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", help="Path to dataset.json")
    parser.add_argument("--image-folder", help="Path to image folder")
    parser.add_argument("--gpu", help="GPU", )
    parser.add_argument("--clip-thr", type=float, default=0.2)

    return parser.parse_args()

def remove_duplicated_captions(dataset):
    d = defaultdict(lambda: [])
    for example in tdqm.tqdm(dataset, desc="Removing duplicated captions"):
        d[example["caption"].lower()].append(example)

    return [v[0] for v in d.values() if len(v[0]["caption"].split()) > 3]


def compute_capivara_similarity(model, batch, device):
    image_input, text_input = batch
    image_input = image_input.to(device)
    text_input = text_input.to(device)

    img_features = model.encode_image(image_input)
    txt_features = model.encode_text(text_input)

    norm_img_features = img_features / img_features.norm(dim=1, keepdim=True)
    norm_txt_features = txt_features / txt_features.norm(dim=1, keepdim=True)

    sim = norm_txt_features @ norm_img_features.T

    return sim.diag()  # similarity between corresponding texts and images


def capivara_filter(dataset, images_dir, clip_thr, device):
    print(">>>> Loading model")
    model, _, vision_processor = open_clip.create_model_and_transforms("hf-hub:hiaac-nlp/CAPIVARA")
    text_tokenizer = open_clip.get_tokenizer("hf-hub:hiaac-nlp/CAPIVARA")
    model.to(device)
    model.eval()

    example_list = []
    text_batch = []
    image_batch = []
    output_data = []
    for example in tdqm.tqdm(dataset, desc="Capivara Filter"):
        text_input = text_tokenizer(example["caption"])
        try:
            image = PIL.Image.open(os.path.join(images_dir, example["filename"])).convert('RGB')
            image_input = vision_processor(image)
        except:
            continue

        if len(example_list) < 100:
            text_batch.append(text_input)
            image_batch.append(image_input)
            example_list.append(example)
        else:
            # filter the examples whose image and caption don't match
            text_batch = torch.stack(text_batch, dim=0).reshape((-1, 77))
            image_batch = torch.stack(image_batch, dim=0)
            batch = image_batch, text_batch

            similarities = compute_capivara_similarity(model, batch, device)
            for example, sim in zip(example_list, similarities):
                if sim >= clip_thr:
                    output_data.append(example)

            text_batch = []
            image_batch = []
            example_list = []

    if len(example_list) > 0:
        text_batch = torch.stack(text_batch, dim=0).reshape((-1, 77))
        image_batch = torch.stack(image_batch, dim=0)
        batch = image_batch, text_batch
        similarities = compute_capivara_similarity(model, batch, device)
        for example, sim in zip(example_list, similarities):
            if sim >= args.threshold:
                output_data.append(example)

    del model
    return output_data

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

    print("Extracting image features...")
    image_features = image_feature_extraction(dataset, images_dir=args.image_folder, device=device)
    print("Extracting text features...")
    text_features = text_feature_extraction(dataset)

    print("Computing clusters...")
    clusters = get_clusters(image_features)
    print("Finding duplicates...")
    dedup_indices = deduplicate(image_features, text_features, clusters)
    dataset = [dataset[index] for index in dedup_indices]

    with open("clean_dataset.json") as file:
        json.dump(dataset, file)

