with open(".fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
labels = []
total = 0
duplicates = 0

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    total += 1
    duplicate = False
    # sequences.append(seq)

    for s in sequences:
        if seq == s:
            duplicate = True
            duplicates += 1
            # sequences.remove(seq)


    # if duplicate == False:
    #     sequences.append(seq)
    #     labels.append(label)
    #     with open("testset01.fasta", "a") as g:
    #         g.write("\n>" + label)
    #         g.write("\n" + seq)

# print(sequences)
# print(labels)
# print(str(len(sequences)))
# print(str(len(labels)))
print(str(total))
print(str(duplicates))
