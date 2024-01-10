import openai
import random


def doStuff():
    openai.api_key = "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"
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    model_engine = "davinci"

    with open("ishaan.txt", "r") as f:
        corpus = f.read()

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=corpus,
        max_tokens=30000,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )


    print(completion.text)

def markov():
    with open("ishaan.txt", "r") as f:
        corpus = f.read()
    words = corpus.split()
    markov_chain = {}
    for i, word in enumerate(words):
        if word not in markov_chain:
            markov_chain[word] = []
        if i < len(words) - 1:
            markov_chain[word].append(words[i+1])
    current_word = random.choice(list(markov_chain.keys()))
    sentence = current_word.capitalize()
    while current_word[-1] not in ".?!":
        next_word = random.choice(markov_chain[current_word])
        sentence += " " + next_word
        current_word = next_word
    print(sentence)


#doStuff()
markov()