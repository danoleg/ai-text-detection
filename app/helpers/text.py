import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter


def describe_text(text):
    char_count = len(text)

    word_count = len(word_tokenize(text))

    words = word_tokenize(text)
    avg_word_length = sum(len(word) for word in words) / word_count

    sentence_count = len(sent_tokenize(text))

    sentences = sent_tokenize(text)
    avg_sentence_length = sum(len(sentence) for sentence in sentences) / sentence_count

    words = [word.lower() for word in words if word.isalpha()]
    unique_word_count = len(set(words))

    stop_words = set(stopwords.words('english'))
    stop_word_count = len([word for word in words if word in stop_words])

    unique_word_ratio = unique_word_count / word_count

    punc_count = len([char for char in text if char in string.punctuation])

    punc_ratio = punc_count / char_count

    question_count = len([sentence for sentence in sentences if sentence.endswith('?')])

    exclamation_count = len([sentence for sentence in sentences if sentence.endswith('!')])

    digit_count = len([char for char in text if char.isdigit()])

    capital_count = len([char for char in text if char.isupper()])

    word_count_dict = Counter(words)
    repeat_word_count = len([word for word in word_count_dict if word_count_dict[word] > 1])

    bigrams = nltk.bigrams(words)
    unique_bigram_count = len(set(bigrams))

    trigrams = nltk.trigrams(words)
    unique_trigram_count = len(set(trigrams))

    fourgrams = nltk.ngrams(words, 4)
    unique_fourgram_count = len(set(fourgrams))

    return {
        'char_count': char_count,
        'word_count': word_count,
        'avg_word_length': avg_word_length,
        'sentence_count': sentence_count,
        'avg_sentence_length': avg_sentence_length,
        'unique_word_count': unique_word_count,
        'stop_word_count': stop_word_count,
        'unique_word_ratio': unique_word_ratio,
        'punc_count': punc_count,
        'punc_ratio': punc_ratio,
        'question_count': question_count,
        'exclamation_count': exclamation_count,
        'digit_count': digit_count,
        'capital_count': capital_count,
        'repeat_word_count': repeat_word_count,
        'unique_bigram_count': unique_bigram_count,
        'unique_trigram_count': unique_trigram_count,
        'unique_fourgram_count': unique_fourgram_count
    }