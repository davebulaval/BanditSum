# BanditSum
This repository contains the code for the EMNLP 2018 paper "[BanditSum: Extractive Summarization as a Contextual Bandit](https://arxiv.org/abs/1809.09672)". 

This implementation is python 3.7 fully fonctionnal and work fine with torch 1.0.

For question about the paper you can contact one of the [author](yue.dong2@mail.mcgill.ca).

Paper citation and code citation
```
@inproceedings{dong2018banditsum,
  title={BanditSum: Extractive Summarization as a Contextual Bandit},
  author={Dong, Yue and Shen, Yikang and Crawford, Eric and van Hoof, Herke and Cheung, Jackie Chi Kit},
  booktitle={Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
  pages={3739--3748},
  year={2018}
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
2. Download `CNN_STORIES_TOKENIZED` and `DM_STORIES_TOKENIZED` from [here](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail)
and move the data into `data/CNN_DM_stories` (next to the file `drop_data_stories_here.md`). After that you will 
have `data/CNN_DM_stories/folder 1` and `data/CNN_DM_stories/folder 2`.
3. Download the Glove 100d(glove.6B.zip) [vocab vectors](https://nlp.stanford.edu/projects/glove/), rename `glove.6B.100d.txt` 
to `vocab_100d.txt` and move it into `data/CNN_DM_pickle_data` (next to the file `drop_vocab_here.md`). 

After that, your repository should look like the content of `tree.md`.

## Run
1. From the repository directory run `pickle_glove.py` to parse and pickle the Glove vectors.
2. From the repository directory run `python pickle_data.py` to pickle the data.
3. From the repository directory run `python main.py` to train the model.

*10 epochs took about 4 days on a RTX 2080 ti. For paper replication you can drop the number of epochs down to 2. I would recommand this number.*

# Error Handling
If you get this error message
```
Cannot open exception db file for reading: /home/pythonrouge/pythonrouge/RELEASE-1.5.5/data/WordNet-2.0.exc.db
```

As stated in the following [solution](https://libraries.io/github/tagucci/pythonrouge) do the following

```
cd pythonrouge/RELEASE-1.5.5/data/
```
```
rm WordNet-2.0.exc.db
```
```
./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db
```
