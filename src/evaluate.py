from __future__ import print_function

import os

import numpy as np
import torch

from src import helper
from src.dataLoader import PickleReader, BatchDataLoader
from src.helper import tokens_to_sentences
from src.reinforce import return_summary_index
from src.rougefonc import from_summary_index_generate_hyp_ref, RougeTest_pyrouge, RougeTest_rouge

np.set_printoptions(precision=4, suppress=True)


def reinforce_loss(probs, doc, id=0,
                   max_num_of_sents=3, max_num_of_bytes=-1,
                   std_rouge=False, rouge_metric="all", compute_score=True):
    # sample sentences
    probs_numpy = probs.data.cpu().numpy()
    probs_numpy = np.reshape(probs_numpy, len(probs_numpy))
    max_num_of_sents = min(len(probs_numpy), max_num_of_sents)  # max of sents# in doc and sents# in summary

    rl_baseline_summary_index, _ = return_summary_index(probs_numpy, probs,
                                                        sample_method="greedy", max_num_of_sents=max_num_of_sents)
    rl_baseline_summary_index = sorted(rl_baseline_summary_index)
    rl_baseline_hyp, rl_baseline_ref = from_summary_index_generate_hyp_ref(doc, rl_baseline_summary_index)

    lead3_hyp, lead3_ref = from_summary_index_generate_hyp_ref(doc, range(max_num_of_sents))
    if std_rouge:
        rl_baseline_reward = RougeTest_pyrouge(rl_baseline_ref, rl_baseline_hyp, id=id, rouge_metric=rouge_metric,
                                               compute_score=compute_score, path=os.path.join('./result/rl'))
        lead3_reward = RougeTest_pyrouge(lead3_ref, lead3_hyp, id=id, rouge_metric=rouge_metric,
                                         compute_score=compute_score, path=os.path.join('./result/lead'))
    else:
        try:
            rl_baseline_reward = RougeTest_rouge(rl_baseline_ref, rl_baseline_hyp, rouge_metric,
                                                 max_num_of_bytes=max_num_of_bytes)
            lead3_reward = RougeTest_rouge(lead3_ref, lead3_hyp, rouge_metric, max_num_of_bytes=max_num_of_bytes)
        except AssertionError as e:  # doest not work when len of doc.sum and _hyp are different.
            rl_baseline_reward = 0
            lead3_reward = 0
        except ValueError as e:  # cases where a predicted document is only a "." so the cutting make it an empty doc
            rl_baseline_reward = 0
            lead3_reward = 0

    return rl_baseline_reward, lead3_reward


def ext_model_eval(model, vocab, args, eval_data="test"):
    print("loading data %s" % eval_data)

    model.eval()

    data_loader = PickleReader(args.data_dir)
    eval_rewards, lead3_rewards = [], []
    data_iter = data_loader.chunked_data_reader(eval_data)
    print("doing model evaluation on %s" % eval_data)

    for phase, dataset in enumerate(data_iter):
        for step, docs in enumerate(BatchDataLoader(dataset, shuffle=False)):
            print("Done %2d chunck, %4d/%4d doc\r" % (phase + 1, step + 1, len(dataset)), end='')

            doc = docs[0]
            doc.content = tokens_to_sentences(doc.content)
            doc.summary = tokens_to_sentences(doc.summary)
            if len(doc.content) == 0 or len(doc.summary) == 0:
                continue

            if args.oracle_length == -1:  # use true oracle length
                oracle_summary_sent_num = len(doc.summary)
            else:
                oracle_summary_sent_num = args.oracle_length

            x = helper.prepare_data(doc, vocab)
            if min(x.shape) == 0:
                continue
            sents = torch.autograd.Variable(torch.from_numpy(x)).cuda()

            outputs = model(sents)

            compute_score = (step == len(dataset) - 1) or (args.std_rouge is False)
            if eval_data == "test":
                reward, lead3_r = reinforce_loss(outputs, doc, id=phase * 1000 + step,
                                                 max_num_of_sents=oracle_summary_sent_num,
                                                 max_num_of_bytes=args.length_limit,
                                                 std_rouge=args.std_rouge, rouge_metric="all",
                                                 compute_score=compute_score)
            else:
                reward, lead3_r = reinforce_loss(outputs, doc, id=phase * 1000 + step,
                                                 max_num_of_sents=oracle_summary_sent_num,
                                                 max_num_of_bytes=args.length_limit,
                                                 std_rouge=args.std_rouge, rouge_metric=args.rouge_metric,
                                                 compute_score=compute_score)

            if compute_score:
                if reward == 0:
                    reward = [0] * 9
                elif isinstance(reward, tuple):
                    reward = list(reward)
                eval_rewards.append(reward)

                if lead3_r == 0:
                    lead3_r = [0] * 9
                elif isinstance(lead3_r, tuple):
                    lead3_r = list(lead3_r)
                lead3_rewards.append(lead3_r)

    avg_eval_r = np.mean(eval_rewards, axis=0)
    avg_lead3_r = np.mean(lead3_rewards, axis=0)
    print('model %s reward in %s:' % (args.rouge_metric, eval_data))
    print(avg_eval_r)
    print(avg_lead3_r)
    return avg_eval_r, avg_lead3_r
