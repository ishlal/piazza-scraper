
import csv

if __name__ == "__main__":
    f = open("ishaan_f22.txt", "r")
    lines = f.readlines()
    chunks = []
    tmp = []
    for line in lines:
        if line == "\n":
            chunks.append(tmp)
            tmp = []
        else:
            tmp.append(line)
    chunks.append(tmp)
    f.close()
    condensed_chunks = []
    for chunk in chunks:
        question = ""
        answer = ""
        curr_q = True
        inx = 0
        for line in chunk:
            if line == "\n":
                continue
            if curr_q:
                if len(line) >= 6:
                    if line[0:6] == "ANSWER":
                        curr_q = False
                        answer += line
                    else:
                        question += line
                else: 
                    question += line
            else:
                answer += line
        cond = []

        cond.append(question)
        cond.append(answer)
        condensed_chunks.append(cond)
    # for i in condensed_chunks[1:10]:
    #     print(i)
    print(condensed_chunks[110][1])

    with open('ishaan_f22.csv', 'w', newline='') as csvfile:
        fieldnames = ['question', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for chunk in condensed_chunks:
            writer.writerow({'question': chunk[0], 'answer': chunk[1]})
    



