# BanditSum

This repository contains the code for the EMNLP 2018
paper "[BanditSum: Extractive Summarization as a Contextual Bandit](https://arxiv.org/abs/1809.09672)".

This implementation is python 3.7 fully fonctionnal and work fine with torch 1.0.

For question about the paper you can contact one of the [author](yue.dong2@mail.mcgill.ca).

Use the following to cite the original article and code

```
@inproceedings{dong2018banditsum,
  title={BanditSum: Extractive Summarization as a Contextual Bandit},
  author={Dong, Yue and Shen, Yikang and Crawford, Eric and van Hoof, Herke and Cheung, Jackie Chi Kit},
  booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
  pages={3739--3748},
  year={2018}
}
```

and the following if using this code implementation

```
@inproceedings{banditsumpython3,
  title={{A Python3 BandiSum Implementation}},
  author={Beauchemin, David and Godbout, Mathieu},
  url = {https://github.com/davebulaval/BanditSum}
}
```

## The Test Output:

https://drive.google.com/file/d/1tMiWuRzvDfHGwDILDXT2WFpyFcuHSK1n/view?usp=sharing

## The Pre-trained Model (of BanditSum):

Test data: https://drive.google.com/file/d/1PCl0VVfhlcEaz-eSc5alP_U8uaVQGc_P/view?usp=sharing

Pre-trained model: https://drive.google.com/file/d/13UB2GH_TT5SPQaYydnxYXYHClD4pbOIn/view?usp=sharing

The vocab file: https://drive.google.com/file/d/1W0QQkz5VNCk-YAnpSRc0ONFgR5SPGDA8/view?usp=sharing

## Installation and prerequisites

1. Install the requirements with `pip install -r requirements.txt`
2. Download nltk data with `python nltk_download.py`
2. Download `CNN_STORIES_TOKENIZED` and `DM_STORIES_TOKENIZED`
   from [here](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail)
   and move the data into `data/CNN_DM_stories` (next to the file `drop_data_stories_here.md`). After that you will
   have `data/CNN_DM_stories/folder 1` and `data/CNN_DM_stories/folder 2`.
3. Download the Glove 100d(glove.6B.zip) [vocab vectors](https://nlp.stanford.edu/projects/glove/),
   rename `glove.6B.100d.txt`
   to `vocab_100d.txt` and move it into `data/CNN_DM_pickle_data` (next to the file `drop_vocab_here.md`).

After that, your repository should look like the content of `tree.md`.

## Run

1. From the repository directory run `pickle_glove.py` to parse and pickle the Glove vectors.
2. From the repository directory run `python pickle_data.py` to pickle the data.
3. From the repository directory run `python main.py` to train the model.

*10 epochs took about 4 days on a RTX 2080 ti. For paper replication you can drop the number of epochs down to 2. I
would recommand this number.*

### Compute Rouge

The authors used Rouge155 implemented in Pearl for most of the computation of the Rouge scores, this implementation (and
the way they call the framework) take
**a lot** of time. We have achieved similar results (see section Our Results for more details) using
the [Python rouge](https://pypi.org/project/rouge/)
implementation. Using this version allows us to achieve similar results in about half the time.

# Error Handling

If you get this error message

```
Cannot open exception db file for reading: /home/pythonrouge/pythonrouge/RELEASE-1.5.5/data/WordNet-2.0.exc.db
```

As stated in the following [solution](https://libraries.io/github/tagucci/pythonrouge) do the following

```
cd data/SciSoft/ROUGE-1.5.5/data/
```

```
rm WordNet-2.0.exc.db
```

```
./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db
```

# Our Results

We were able to reproduce the article results using the Python Rouge implementation instead of the Pearl ROUGE155 one.
We trained the model for two epochs (same as the authors), using the same hyperparameters (learning rate, dropout,
embeddings, sample size). We could not batch due to memory constraints due to one document containing 156 sentences.

For our experiment, we trained five models using each time a different seed (123, 2, 3, 4 and 5) and report the
individual results in the next table. We can see that we obtain similar results as the reference article.

| Seed |           | ROUGE-1 (%) | ROUGE-2 (%) | ROUGE-L (%) |
|:----:|:---------:|:-----------:|:-----------:|:-----------:|
|  123 | BanditSum |    42.3    |    18.4    |    36.2    |
|  123 |   Lead3   |    40.7    |    16.9    |    33.9    |
|   2  | BanditSum |    42.2    |    18.3    |    36.1    |
|   2  |   Lead3   |    40.7    |    16.9    |    33.9    |
|   3  | BanditSum |    42.2    |    18.3    |    36.1    |
|   3  |   Lead3   |    40.7    |    16.9    |    33.9    |
|   4  | BanditSum |    42.4    |    18.4    |    36.2    |
|   4  |   Lead3   |    40.7    |    16.9    |    33.9    |
|   5  | BanditSum |    39.5    |    17.8    |    38.6    |
|   5  |   Lead3   |    38.3    |    16.7    |    37.0    |

In the next table, we report the mean of the five previous results plus a standard deviation over and under the results and the
reference results.

|                  |   ROUGE-1 (%)   |   ROUGE-2 (%)   |   ROUGE-L (%)   |
|:----------------:|:---------------:|:---------------:|:---------------:|
|     BanditSum    |       41.5      |       18.7      |       37.6      |
|       Lead3      |        40       |       17.5      |       36.2      |
| BanditSum (ours) |  41.7 $\pm$ 1.3 | 18.2 $\pm$ 0.3 | 36.6 $\pm$ 1.1 |
|   Lead3 (ours)   | 40.2 $\pm$ 1.1 | 16.9 $\pm$ 0.1 | 34.5 $\pm$ 1.4 |