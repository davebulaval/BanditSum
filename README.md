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

## CNN/DailyMail Dataset
Instructions to download our preprocessed CNN/DailyMail Dataset can be found here.
https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail

## The Test Output:
https://drive.google.com/file/d/1tMiWuRzvDfHGwDILDXT2WFpyFcuHSK1n/view?usp=sharing

## The Pre-trained Model:

Test data: https://drive.google.com/file/d/1PCl0VVfhlcEaz-eSc5alP_U8uaVQGc_P/view?usp=sharing

Pre-trained model: https://drive.google.com/file/d/13UB2GH_TT5SPQaYydnxYXYHClD4pbOIn/view?usp=sharing

The vocab file: https://drive.google.com/file/d/1W0QQkz5VNCk-YAnpSRc0ONFgR5SPGDA8/view?usp=sharing

### Installation

1. Install the requirements with `pip install -r requirements.txt`
2. Download nltk data with `python nltk_download.py`
1. Download the [url_lists dataset](https://github.com/abisee/cnn-dailymail)
2. Download the [chunked dataset](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail)
3. Download the Glove 100d(glove.6B.zip) [vocab](https://nlp.stanford.edu/projects/glove/)
4. Rename the `glove.6B.100d.txt` to `vocab_100d.txt`
4. Create a data directory at the same level of the BanditSum repository and place the datasets as the following (also note where the vectors should be)
```bash
.
├── BanditSum
│   ├── dataLoader.py
│   ├── evaluate.py
│   ├── experiments.py
│   ├── helper.py
│   ├── log
│   │   └── placeholder
│   ├── main.py
│   ├── model
│   │   └── placeholder
│   ├── model.py
│   ├── pickle_glove.py
│   ├── README.md
│   ├── reinforce.py
│   ├── result 
│   │   ├── rl/
│   │   └── lead/
│   └── rougefonc.py
└── data *outside of the Git repository*
        ├── SciSoft 
        │   └── *Place to drop the ROUGE-1.5.5 files*
        ├── CNN_DM_stories
        │   └── A lot of stories files
        ├── CNN_DM_pickle_data
        │   ├── chunked
        │   │   ├── test_000.bin
        │   │   ├── ...
        │   │   ├── train_287.bin
        │   │   ├── val_000.bin
        │   │   ├── ...
        │   │   └── val_287.bin
        │   ├── pickled/ *create this repository*
        │   ├── vocab_100d.txt *move vectors here*
        |   └── vocab
        └── url_lists
                ├── all_test.txt
                ├── all_train.txt
                ├── all_val.txt
                ├── cnn_wayback_test_urls.txt
                ├── cnn_wayback_training_urls.txt
                ├── cnn_wayback_validation_urls.txt
                ├── dailymail_wayback_test_urls.txt
                ├── dailymail_wayback_training_urls.txt
                ├── dailymail_wayback_validation_urls.txt
                └── readme
```
5. From the repository directory run `pickle_glove.py` to parse and pickle the Glove vectors.
5. Download the [ROUGE-1.5.5](https://github.com/andersjo/pyrouge) repository
   
   5.1 Move the ROUGE-1.5.5 repository from pyrouge/tools (the tools directory) into data/Scisoft
   
   5.2 You will now have `data/SciSoft/ROUGE-1.5.5/{bunch of files}`

> Be sure to have created the approprieted folders names

3. From the repository directory run `python pickle_data.py` to pickle the data.
4. From the repository directory run `python main.py` to train the model

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
