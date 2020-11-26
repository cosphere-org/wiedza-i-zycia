#!/bin/bash

export REQUEST_LAG_SECONDS=0.5

export MAIN_URL=https://www.wiz.pl/

export EDITION_LIST_PAGE=https://www.wiz.pl/18.html

folder='/wiedza_i_zycie/data'
curent_dir=`pwd`

export CORPUS_PATH=$curent_dir$folder'/corpus.pickle'

export DICTIONARY_PATH=$curent_dir$folder'/dictionary.pickle'

export LDA_PATH=$curent_dir$folder'/lda.pickle'

export TOKENIZED_PATH=$curent_dir$folder'/tokenized_text_df.pickle'

export TRAINED_DF_PATH=$curent_dir$folder'/trained_df.pickle'

export MALLET_PATH=$curent_dir$folder'/mallet-2.0.8/bin/mallet'

export PYDAVIS_VIS_FILE=$curent_dir$folder'/pyLDAvisVis.html'

export HISTOGRAM_PATH=$curent_dir$folder'/histogram_of_lengths.png'

export COHERENCE_VALUES_PATH=$curent_dir$folder'/coherence_values.pickle'

export MODEL_LIST_PATH=$curent_dir$folder'/model_list.pickle'
