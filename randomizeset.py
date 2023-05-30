import random

with open("input.fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
new_sequences = []

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    sequences.append({label:seq})

new_size = 10

for i in range(new_size):
    sequence = random.choice(sequences)
    new_sequences.append(sequence)
    sequences.remove(sequence)

for s in new_sequences:
    for label, seq in s.items():
        with open("output.fasta", "a") as f:
            f.write("\n>" + label)
            f.write("\n" + seq)

# for s in sequences:
#     for label, seq in s.items():
#         with open("output2.fasta", "a") as f:
#             f.write("\n>" + label)
#             f.write("\n" + seq)
