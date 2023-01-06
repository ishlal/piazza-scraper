import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, LSTM, Dropout
from keras.utils import to_categorical
from random import randint
from tensorflow.keras.optimizers.legacy import Adam
import nltk
import tensorflow
import ssl
from nltk.tokenize import word_tokenize
import re
from keras.preprocessing.text import Tokenizer


def preprocess_text(sen):
    # remove punctuation and numbers
    # sentence = re.sub('[^a-zA-Z]', ' ', sen)
    
    # single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sen)

    # removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence.lower()

if __name__ == "__main__":
    text = open("ishaan.txt", "r").read()
    text = preprocess_text(text)
    # ishaan_words = word_tokenize(text)
    # ishaan_words = nltk.tokenize(text)
    ishaan_words = text.split()
    #print(ishaan_words)
    # ishaan_words = text
    n_words = len(ishaan_words)
    unique_words = len(set(ishaan_words))
    print(n_words)
    print(unique_words)
    # print(n_words)
    # print(unique_words)
    tokenizer = Tokenizer(num_words=unique_words+1)
    tokenizer.fit_on_texts(ishaan_words)
    # tokenizer.fit_on_sequences(ishaan_words)
    vocab_size = len(tokenizer.word_index) + 1
    # ISSUE: removes all mathematical stuff
    word_2_index = {}
    unique_words_set = set(ishaan_words)
    counter = 1
    for i in unique_words_set:
        word_2_index[i] = counter
        counter+=1
    # word_2_index = tokenizer.word_index
    print(word_2_index)

    input_sequence = []
    output_words = []
    input_seq_length = 100
    # print(ishaan_words)
    for i in range(0, n_words-input_seq_length, 1):
        in_seq=ishaan_words[i:i+input_seq_length]
        out_seq=ishaan_words[i+input_seq_length]
        input_sequence.append([word_2_index[word] for word in in_seq])
        output_words.append(word_2_index[out_seq])
    #print(input_sequence[0])
    X = np.reshape(input_sequence, (len(input_sequence), input_seq_length, 1))
    X = X / float(vocab_size)
    y = to_categorical(output_words)
    # print(X.shape)
    # print(y.shape)

    model = Sequential()
    model.add(LSTM(800, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(LSTM(800, return_sequences=True))
    model.add(LSTM(800))
    model.add(Dense(y.shape[1], activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', 
        optimizer=tensorflow.keras.optimizers.legacy.Adam())

    model.fit(X, y, batch_size=64, epochs=10, verbose=1)

    # making predictions
    random_seq_index = np.random.randint(0, len(input_sequence)-1)
    random_seq = input_sequence[random_seq_index]
    index_2_word = dict(map(reversed, word_2_index.items()))
    word_sequence = [index_2_word[value] for value in random_seq]

    for i in range(100):
        int_sample = np.reshape(random_seq, (1, len(random_seq), 1))
        int_sample = int_sample/float(vocab_size)

        predicted_word_index = model.predict(int_sample, verbose=0)
        predicted_word_id = np.argmax(predicted_word_index)
        seq_in = [index_2_word[index] for index in random_seq]

        word_sequence.append(index_2_word[predicted_word_id])

        random_seq.append(predicted_word_id)
        random_seq = random_seq[1:len(random_seq)]
    final_output = ""
    for word in word_sequence:
        final_output=final_output + " " + word
    print(final_output)


