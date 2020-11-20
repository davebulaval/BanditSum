.
├── data
│ ├── CNN_DM_pickle_data
│ │ ├── pickled
│ │ └── vocab_100d.txt
│ ├── CNN_DM_stories
│ │ ├── cnn_stories_tokenized
│ │ │ ├── cnn_stories_tokenized *with a lot of .stories files here*
│ │ │ └── dm_stories_tokenized *with a lot of .stories files here*
│ ├── SciSoft
│ │ ├── README.md
│ │ └── ROUGE-1.5.5
│ │     ├── data
│ │     │ ├── smart_common_words.txt
│ │     │ ├── WordNet-1.6-Exceptions
│ │     │ │ ├── adj.exc
│ │     │ │ ├── adv.exc
│ │     │ │ ├── buildExeptionDB.pl
│ │     │ │ ├── noun.exc
│ │     │ │ └── verb.exc
│ │     │ ├── WordNet-2.0.exc.db
│ │     │ └── WordNet-2.0-Exceptions
│ │     │     ├── adj.exc
│ │     │     ├── adv.exc
│ │     │     ├── buildExeptionDB.pl
│ │     │     ├── noun.exc
│ │     │     └── verb.exc
│ │     ├── README.txt
│ │     ├── RELEASE-NOTE.txt
│ │     ├── ROUGE-1.5.5.pl
│ │     ├── runROUGE-test.pl
│ │     └── XML
│ │         ├── DOM
│ │         │ ├── AttDef.pod
│ │         │ ├── AttlistDecl.pod
│ │         │ ├── Attr.pod
│ │         │ ├── CDATASection.pod
│ │         │ ├── CharacterData.pod
│ │         │ ├── Comment.pod
│ │         │ ├── DocumentFragment.pod
│ │         │ ├── Document.pod
│ │         │ ├── DocumentType.pod
│ │         │ ├── DOMException.pm
│ │         │ ├── DOMImplementation.pod
│ │         │ ├── ElementDecl.pod
│ │         │ ├── Element.pod
│ │         │ ├── Entity.pod
│ │         │ ├── EntityReference.pod
│ │         │ ├── NamedNodeMap.pm
│ │         │ ├── NamedNodeMap.pod
│ │         │ ├── NodeList.pm
│ │         │ ├── NodeList.pod
│ │         │ ├── Node.pod
│ │         │ ├── Notation.pod
│ │         │ ├── Parser.pod
│ │         │ ├── PerlSAX.pm
│ │         │ ├── ProcessingInstruction.pod
│ │         │ ├── Text.pod
│ │         │ └── XMLDecl.pod
│ │         ├── DOM.pm
│ │         ├── Handler
│ │         │ └── BuildDOM.pm
│ │         └── RegExp.pm
│ └── url_lists
│     ├── all_test.txt
│     ├── all_train.txt
│     ├── all_val.txt
│     ├── cnn_wayback_test_urls.txt
│     ├── cnn_wayback_training_urls.txt
│     ├── cnn_wayback_validation_urls.txt
│     ├── dailymail_wayback_test_urls.txt
│     ├── dailymail_wayback_training_urls.txt
│     ├── dailymail_wayback_validation_urls.txt
│     └── README.md
├── src
│ ├── dataLoader.py
│ ├── evaluate.py
│ ├── experiments.py
│ ├── helper.py
│ ├── reinforce.py
│ └── rougefonc.py
├── log
├── main.py
├── model
├── model.py
├── nltk_download.py
├── pickle_data.py
├── pickle_glove.py
├── pickle_vocab.py
├── README.md
├── requirements.txt
├── result
│ ├── lead
│ └── rl
└── tree.md
