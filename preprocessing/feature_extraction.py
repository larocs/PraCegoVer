import os

import torch
import umap
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from torch import nn
from torchvision import transforms
from tqdm import tqdm
from nltk.corpus import stopwords
import numpy as np

class Dataset(torch.utils.data.Dataset):
    def __init__(self, dataset, images_dir):
        self.dataset = dataset
        self.images_dir = images_dir
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        filename = self.dataset[index]["filename"]
        filename = os.path.join(self.images_dir, filename)
        img = Image.open(filename)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        try:
            return self.transform(img)
        except:
            pass


def image_feature_extraction(dataset, images_dir):
    print('Extracting image features...')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pracegover_dataset = Dataset(dataset, images_dir=images_dir)
    dataloader = torch.utils.data.DataLoader(pracegover_dataset, shuffle=False,
                                             batch_size=1000,
                                             num_workers=10)
    model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v2', pretrained=True)
    model = model.to(device)
    model.eval()
    feature_list = []
    for batch in tqdm.tqdm_notebook(dataloader):
        batch = batch.to(device)
        with torch.no_grad():
            x = model.features(batch)
            x = nn.functional.adaptive_avg_pool2d(x, (1, 1))
            feature_list.append(torch.flatten(x, 1))

    features = torch.concat(feature_list, dim=0)

    print('Reducing dimensions of image features...')
    reducer = umap.UMAP(n_neighbors=80,
                        min_dist=0,
                        n_components=900,
                        random_state=42,
                        metric='correlation')

    features = reducer.fit_transform(features.cpu())
    np.save("image_features.npy", features)
    return features


def text_feature_extraction(dataset):
    texts = [example["caption"] for example in dataset]
    stop_words = list(stopwords.words('portuguese'))
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    return vectorizer.fit_transform(texts)
