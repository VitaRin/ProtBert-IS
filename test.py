from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from sklearn.metrics import accuracy_score
import re
import json

model_name = ""
input_name = ""
output_name = ""
local = False

pipeline = TextClassificationPipeline(
    model=AutoModelForSequenceClassification.from_pretrained(model_name, local_files_only=local),
    tokenizer=AutoTokenizer.from_pretrained(model_name, local_files_only=local),
    device=0
)

with open(input_name, "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []
truths = []
predictions = []

for d in data:
    seq = d.split('\n', 1)[-1].replace('\n', '').replace('', ' ')
    sol = d.split('\n', 1)[0].replace('\n', '')[-1]
    name = d.split('\n', 1)[0].replace('\n', '')
    truths.append(sol)
    sequences.append(seq)

sequences = [re.sub(r"[UZOB]", "X", sequence) for sequence in sequences]

result = pipeline(sequences)

print(result)

outputfile = open(output_name, "a")

insoluble = 0
soluble = 0
t = 0

for a in result:
    outputfile.write(json.dumps(a) + ', ground truth: ' + truths[t] +'\n')
    t += 1

    if a['label'] == 'Insoluble':
        insoluble += 1
    elif a['label'] == 'Soluble':
        soluble += 1

    predictions.append(a['label'][0])

print("Insoluble " + str(insoluble))
print("Soluble " + str(soluble))

accuracy = accuracy_score(truths, predictions)
print("Accuracy " + str(accuracy))

outputfile.write("Insoluble " + str(insoluble) + '\n')
outputfile.write("Soluble " + str(soluble))
outputfile.write("\nAccuracy: " + str(accuracy))
outputfile.close()
