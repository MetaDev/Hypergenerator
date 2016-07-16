from loremipsum.generator import Generator

with open('data/sample.txt', 'r') as sample_txt:
    sample = sample_txt.read()
    with open('data/dictionary.txt', 'r') as dictionary_txt:
        dictionary = dictionary_txt.read().split()
    g = Generator(sample, dictionary)
    for i in range(10):
        print(list(g.generate_sentences(10)))
