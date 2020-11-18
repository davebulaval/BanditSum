import pickle

from dataLoader import Document, Dataset, read_text_file, get_url_hashes, fix_missing_period


def get_art_abs(story_file):
    lines = read_text_file(story_file)

    # Lowercase everything
    lines = [line.lower() for line in lines]

    # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
    lines = [fix_missing_period(line) for line in lines]

    # Separate out article and abstract sentences
    article_lines = []
    highlights = []
    next_is_highlight = False
    for idx, line in enumerate(lines):
        if line == "":
            continue  # empty line
        elif line.startswith("@highlight"):
            next_is_highlight = True
        elif next_is_highlight:
            highlights.append(line)
        else:
            article_lines.append(line)

    # Make article into a single string
    article = ' '.join(article_lines)

    # Make abstract into a signle string, putting <s> and </s> tags around the sentences
    abstract = ' '.join(["%s %s %s" % ('<s>', sent, '</s>') for sent in highlights])

    return article.split(' '), abstract.split(' ')


def write_to_pickle(url_file, out_file, chunk_size=1000):
    url_list = read_text_file(url_file)
    url_hashes = get_url_hashes(url_list)
    url = zip(url_list, url_hashes)
    story_fnames = ["./data/CNN_DM_stories/cnn_stories_tokenized/" + s + ".story"
                    if u.find(
        'cnn.com') >= 0 else "./data/CNN_DM_stories/dm_stories_tokenized/" + s + ".story"
                    for u, s in url]

    print(f"Pickling the {url_file.split('/')[-1].split('.')[0]} data")
    new_lines = []
    for i, filename in enumerate(story_fnames):
        if i % chunk_size == 0 and i > 0:
            pickle.dump(Dataset(new_lines), open(out_file % (i / chunk_size), "wb"),
                        protocol=pickle.HIGHEST_PROTOCOL)
            new_lines = []

        try:
            art, abs = get_art_abs(filename)
        except:
            print(f"Pickling of file {filename} did not worked.")
            continue
        new_lines.append(Document(art, abs))

    if new_lines != []:
        pickle.dump(Dataset(new_lines), open(out_file % (i / chunk_size + 1), "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Finished pickling the {url_file.split('/')[-1].split('.')[0]} data")


def main():
    train_urls = "./data/url_lists/all_train.txt"
    val_urls = "./data/url_lists/all_val.txt"
    test_urls = "./data/url_lists/all_test.txt"

    write_to_pickle(test_urls, "./data/CNN_DM_pickle_data/pickled/test_%03d.bin.p", chunk_size=100000000)
    write_to_pickle(val_urls, "./data/CNN_DM_pickle_data/pickled/val_%03d.bin.p", chunk_size=100000000)
    write_to_pickle(train_urls, "./data/CNN_DM_pickle_data/pickled/train_%03d.bin.p")


if __name__ == "__main__":
    main()
