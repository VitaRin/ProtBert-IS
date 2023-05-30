import random

sequences1 = []
sequences2 = []
output_name = "output.fasta"

with open("input1.fasta", "r") as f:
    data1 = f.read().split(">")

data1.remove(data1[0])

for d in data1:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    sequences1.append({label:seq})

with open("input2.fasta", "r") as f:
    data2  = f.read().split(">")

data2.remove(data2[0])

for d in data2:
    seq = d.split('\n', 1)[-1].replace('\n', '')
    label = d.split('\n', 1)[0]
    sequences2.append({label:seq})

while(len(sequences1 + sequences2) != 0):
    choice = random.choice([0, 1])

    if choice == 0 and len(sequences1) != 0:
        sequence = random.choice(sequences1)
        sequences1.remove(sequence)

        with open(output_name, "a") as f:
            for label, seq in sequence.items():
                f.write("\n>" + label)
                f.write("\n" + seq)

    elif len(sequences2) != 0:
        sequence = random.choice(sequences2)
        sequences2.remove(sequence)
        with open(output_name, "a") as f:
            for label, seq in sequence.items():
                f.write("\n>" + label)
                f.write("\n" + seq)
