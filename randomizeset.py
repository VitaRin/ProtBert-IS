import random

with open("documents/final/insolnewtestset.fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
new_sequences = []
total = 0

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    total += 1

    sequences.append({label:seq})

new_size = 10

for i in range(new_size):
    sequence = random.choice(sequences)
    new_sequences.append(sequence)
    sequences.remove(sequence)


for s in new_sequences:
    for label, seq in s.items():
        with open("documents/final/insoltest10.fasta", "a") as f:
            print(label)
            print(seq)
            f.write("\n>" + label)
            f.write("\n" + seq)

# for s in sequences:
#     for label, seq in s.items():
#         with open("insoltest2.fasta", "a") as f:
#             f.write("\n>" + label)
#             f.write("\n" + seq)
