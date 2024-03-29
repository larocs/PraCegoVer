# \#PraCegoVer

**\#PraCegoVer** is a multi-modal dataset containing images associated to Portuguese captions based on posts from
Instagram.

## Download

The **\#PraCegoVer** dataset is available upon request for **non-commercial purposes only**. It can be requested and
downloaded on our data repository on [Zenodo](https://zenodo.org/record/7548638).

The dataset is composed of the main file _dataset.json_ and a collection of compressed files containing the images. The
file _dataset.json_ comprehends a list of json objects with the attributes: _user_, _filename_, _raw_caption_, _caption_
and _date_. These attributes represent, respectively, the anonymized user that made the post, the image file name, the
raw caption, the clean caption, and the post date. Each instance in _dataset.json_ is associated with exactly one image
in the images directory whose filename is pointed by the attribute
_filename_. The instances have the following structure:

![Instance](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/instance.png)

#### New Release
- **18/Jan/2023** - [Download](https://zenodo.org/record/7548638)

We release ***pracegover_400k.json*** which contains 403,337 examples from the original ***dataset.json***  after preprocessing and duplication removal. It is split into train, validation, and test with 242036, 80628, and 80673 examples, respectively.

## Motivation

Automatically describing images using natural sentences is an essential task to visually impaired people's inclusion on
the Internet. Although there are many datasets in the literature, most of them contain only English captions, whereas
datasets with captions described in other languages are scarce. Then, inspired by
the [PraCegoVer](https://mwpt.com.br/criadora-do-projeto-pracegover-incentiva-descricao-de-imagens-na-web/) moviment, we
introduce the \#PraCegoVer dataset.

\#PraCegoVer has more than 500 thousand pairs with images and captions described in Portuguese collected from more than
14 thousand different profiles. Also, the mean caption length in \#PraCegoVer is 39.3 words and standard deviation is
29.7, whereas the captions in [MS COCO Captions](http://cocodataset.org/) 10.5 words on average and standard deviation
of 2.2. These chacteristics make our dataset more challenging than MS COCO.

## Dataset Description

In Figure 1, we show the growth of \#PraCegoVer dataset compared to the number of total posts tagging  *\#PraCegoVer* on
Instagram over time. Currently, \#PraCegoVer dataset contains about 30\% of all public posts tagging  *\#PraCegoVer*.

![The total number of posts tagging \#PraCegoVer (dashed line) and \#PraCegoVer dataset size (solid line) throughout the time.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/dataset_size_over_time.png)

Figure 1: The total number of posts tagging *\#PraCegoVer* (dashed line) and \#PraCegoVer dataset size (solid line)
throughout the time.

After a thorough exploratory analysis, we extracted some relevant topics from the captions in \#PraCegoVer dataset, as
illustrated in Figure 2. We also found well-formed clusters that represent images of advertisements, birds and
airplanes (Figures 3, 4 and 5, respectively).

![Relevant topics found within the captions in \#PraCegoVer dataset.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/caption_topics.png)

Figure 2: Relevant topics found within the captions in \#PraCegoVer dataset.

![Images sampled from a cluster with advertisements.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/cluster_ads.png)

Figure 3: Images sampled from a cluster with advertisements.

![Images sampled from a cluster with birds.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/cluster_birds.png)

Figure 4: Images sampled from a cluster with birds.

![Images sampled from a cluster with airplanes.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/cluster_airplanes.png)

Figure 5: Images sampled from a cluster with airplanes.

## \#PraCegoVer *vs* MS COCO

Figure 6 shows the distribution of captions by length in \#PraCegoVer and MS COCO Captions datasets. \#PraCegoVer's
captions have on average 40 words, while MS COCO Captions has only about 10. Also, it can be seen that the variance in
\#PraCegoVer is considerably higher than in MS COCO.

![Histogram illustrating the distribuition of caption length in terms of number of words.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/joint_histogram_posts_by_text_length.png)

Figure 6: Histogram illustrating the distribuition of caption length in terms of number of words.

Figure 7 shows the distribution of words by frequency, *i.e.*, the number of occurrences of that word, for \#PraCegoVer
and MS COCO Captions. On the x-axis, we show ranges of word frequency, and on the y-axis, we show the number of words
whose frequency is within that band. \#PraCegoVer has by far more words occurring five or fewer times within the
captions than MS COCO.

![Histogram illustrating the distribuition of words with respect to the frequency.](https://github.com/gabrielsantosrv/PraCegoVer/blob/main/assets/joint_plot_word_frequency.png)

Figure 7: Histogram illustrating the distribuition of words with respect to the frequency

These characteristics make \#PraCegoVer more challenging than MS COCO Captions.

## Authors

Gabriel Oliveira ([@gabrielsantosrv](https://github.com/gabrielsantosrv)), Esther
Colombini ([@estherlc](https://github.com/estherlc)) and Sandra Avila ([@sandraavila](https://github.com/sandraavila)). 

## Citation
If you use our code or dataset, please cite as:

```
@Article{pracegover2022,
AUTHOR = {dos Santos, Gabriel Oliveira and Colombini, Esther Luna and Avila, Sandra},
TITLE = {#PraCegoVer: A Large Dataset for Image Captioning in Portuguese},
JOURNAL = {Data},
VOLUME = {7},
YEAR = {2022},
NUMBER = {2},
ARTICLE-NUMBER = {13},
URL = {https://www.mdpi.com/2306-5729/7/2/13},
ISSN = {2306-5729},
DOI = {10.3390/data7020013}
}
```
