import argparse
import logging
import pickle
import time

import torch
from src.evaluate import ext_model_eval
from src.tools import bool_parse

if __name__ == '__main__':
    # kill the ROUGE155 logger
    logging.getLogger('global').disabled = True

    torch.manual_seed(233)
    parser = argparse.ArgumentParser()

    parser.add_argument('--vocab_file', type=str, default='./data/CNN_DM_pickle_data/vocab_100d.p')
    parser.add_argument('--data_dir', type=str, default='./data/CNN_DM_pickle_data/')
    parser.add_argument('model_file', type=str)

    parser.add_argument('--device', type=int, default=0,
                        help='select GPU')
    parser.add_argument('--std_rouge', type=bool_parse)

    parser.add_argument('--oracle_length', type=int, default=3,
                        help='-1 for giving actual oracle number of sentences'
                             'otherwise choose a fixed number of sentences')
    parser.add_argument('--rouge_metric', type=str, default='all')
    parser.add_argument('--rl_baseline_method', type=str, default="greedy",
                        help='greedy, global_avg,batch_avg,or none')
    parser.add_argument('--length_limit', type=int, default=-1,
                        help='length limit output')

    args = parser.parse_args()

    torch.cuda.set_device(args.device)

    print('generate config')
    with open(args.vocab_file, "rb") as f:
        vocab = pickle.load(f)
    print(vocab)

    print("loading existing model%s" % args.model_file)
    extract_net = torch.load(args.model_file, map_location=lambda storage, loc: storage)
    extract_net.cuda()
    print("finish loading and evaluate model %s" % args.model_file)

    start_time = time.time()
    ext_model_eval(extract_net, vocab, args, eval_data="test")
    print('Test time:', time.time() - start_time)
