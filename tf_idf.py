
import math
import pandas as pd

from nltk import (
    sent_tokenize, 
    word_tokenize, 
    PorterStemmer
)
from nltk.corpus import stopwords

df = pd.read_csv("url_metin.csv")

df = df[df["Metin"].str.contains("a")==True]
df = df.reset_index()
df.drop(columns = ['index'],inplace=True)
haberler = df["Metin"].tolist()
#%%

# Cümlelerdeki kelimelerin frekansları and generate matrix

def _create_frequency_matrix(sentences):
    frequency_matrix = {}

    for sent in sentences:
        freq_table = {}
        words = word_tokenize(sent)
        for word in words:
            word = word.lower()
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        frequency_matrix[sent] = freq_table

    return frequency_matrix



#Calculate tf and generate matrix
def _create_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def _create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table



def _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def _create_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, tf), (word2, idf) in zip(f_table1.items(),
                                                    f_table2.items()):  # here, keys are the same in both the table
            tf_idf_table[word1] = float(tf * idf)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix



def _score_sentences(tf_idf_matrix) -> dict:
    """
    score a sentence by its word's TF
    Basic algorithm: adding the TF frequency of every non-stop word in a sentence divided by total no of words in a sentence.
    :rtype: dict
    """

    sentenceValue = {}

    for sent, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0

        count_words_in_sentence = len(f_table)
        for word, tf_idf in f_table.items():
            total_score_per_sentence += tf_idf

        sentenceValue[sent] = total_score_per_sentence / count_words_in_sentence

    return sentenceValue



def _find_average_score(sentenceValue) -> int:
    """
    Find the average score from the sentence value dictionary
    :rtype: int
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original summary_text
    
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence in sentenceValue and sentenceValue[sentence] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary, sentence_count


summaries = []

for data in haberler:
    
  sentences = sent_tokenize(data)
  total_documents = len(sentences)
  freq_matrix = _create_frequency_matrix(sentences)
  tf_matrix = _create_tf_matrix(freq_matrix)
  count_doc_per_words = _create_documents_per_words(freq_matrix)
  idf_matrix = _create_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
  tf_idf_matrix = _create_tf_idf_matrix(tf_matrix, idf_matrix)
  sentence_scores = _score_sentences(tf_idf_matrix)
  threshold = _find_average_score(sentence_scores)
  summary, sentence_count = _generate_summary(sentences, sentence_scores,threshold)
  summaries.append([summary, sentence_count])

#%%

ozet_cumle_sayisi = pd.DataFrame(summaries, columns = ['Özet','Cümle_Sayisi'])
frames = [df, ozet_cumle_sayisi]
result = pd.concat(frames,axis=1, join='inner')
result.to_csv("metin_ozetleme.csv",index=False)


#import pandas as pd
#metin_ozetleme = pd.read_csv("metin_ozetleme.csv")