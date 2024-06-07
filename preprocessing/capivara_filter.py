import os

import open_clip
import torch
import tqdm
from PIL import Image


class CapivaraDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, images_dir, text_tokenizer, vision_processor):
        self.dataset = dataset
        self.images_dir = images_dir
        self.text_tokenizer = text_tokenizer
        self.vision_processor = vision_processor

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        example = self.dataset[index]
        filename = example["filename"]
        filename = os.path.join(self.images_dir, filename)
        img = Image.open(filename)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        try:
            return self.vision_processor(img), self.text_tokenizer(example["caption"]), example
        except:
            pass


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

    capivara_dataset = CapivaraDataset(dataset, images_dir=images_dir,
                                       text_tokenizer=text_tokenizer,
                                       vision_processor=vision_processor)

    dataloader = torch.utils.data.DataLoader(capivara_dataset, shuffle=False,
                                             batch_size=200,
                                             num_workers=10)

    output_data = []
    for image_input, text_input, example_list in tqdm.tqdm(dataloader, desc="Capivara Filter"):
        batch = image_input, text_input
        similarities = compute_capivara_similarity(model, batch, device)
        for example, sim in zip(example_list, similarities):
            if sim >= clip_thr:
                output_data.append(example)

    del model
    return output_data
