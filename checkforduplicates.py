with open("input1.fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
labels = []
duplicate_count = 0
unmatching_labels = 0

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    sequences.append(seq)
    labels.append(label)

with open("input2.fasta", "r") as f:
    data2 = f.read().split(">")

data2.remove(data2[0])

for d in data2:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    duplicate = False
    t = 0

    for s in sequences:
        if seq == s:
            duplicate = True
            duplicate_count += 1

            if label[-1] != labels[t][-1]:
                unmatching_labels += 1
            sequences.remove(s)
            labels.remove(labels[t])
        t += 1

with open("output.fasta", "a") as f:
    for i in range(len(sequences)):
        f.write("\n>" + labels[i])
        f.write("\n" + sequences[i])

print("Mismatch: " + str(unmatching_labels))
print("Duplicates: " + str(duplicate_count))
