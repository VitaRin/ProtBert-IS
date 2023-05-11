with open(".fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
labels = []
total = 0
total1 = 0
duplicate_count = 0
unmatching_labels = 0

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    total += 1
    sequences.append(seq)
    labels.append(label)

with open(".fasta", "r") as f:
    data2 = f.read().split(">")

data2.remove(data2[0])

for d in data2:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    duplicate = False
    total1 += 1
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

# with open("imretard.fasta", "a") as f:
#     for i in range(len(sequences)):
#         f.write("\n>" + labels[i])
#         f.write("\n" + sequences[i])

print("mismatch: " + str(unmatching_labels))
print("duplicates: " + str(duplicate_count))
print(str(total))
print(str(total1))
