with open("input.fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
labels = []
duplicates = 0

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    duplicate = False

    for s in sequences:
        if seq == s:
            duplicate = True
            duplicates += 1

    if duplicate == False:
        sequences.append(seq)
        labels.append(label)
        with open("output.fasta", "a") as g:
            g.write("\n>" + label)
            g.write("\n" + seq)

print("Duplicates: " + str(duplicates))
