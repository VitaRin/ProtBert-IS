from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import re

model_name = ""

pipeline = TextClassificationPipeline(
    model=AutoModelForSequenceClassification.from_pretrained(model_name),
    tokenizer=AutoTokenizer.from_pretrained(model_name),
    device=0
)

with open("input.fasta", "r") as f:
    data = f.read().split(">")

data.remove(data[0])
sequences = []

for d in data:
    d = d.split('\n', 1)[-1].replace('\n', '').replace('', ' ')
    sequences.append(d)

sequences = [re.sub(r"[UZOB]", "X", sequence) for sequence in sequences]
print(pipeline(sequences))
