import torch
from transformers import AutoTokenizer, Trainer, TrainingArguments, AutoModelForSequenceClassification
from torch.utils.data import Dataset
import os
import pandas as pd
import requests
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import re


model_name = 'Rostlab/prot_bert_bfd'

class DeepLocDataset(Dataset):

    def __init__(self, split="train", tokenizer_name='Rostlab/prot_bert_bfd', max_length=1024):
        self.datasetFolderPath = 'dataset/'
        self.trainFilePath = os.path.join(self.datasetFolderPath, 'deeploc_per_protein_train.csv')
        self.testFilePath = os.path.join(self.datasetFolderPath, 'deeploc_per_protein_test.csv')

        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, do_lower_case=False)

        if split=="train":
          self.seqs, self.labels = self.load_dataset(self.trainFilePath)
        else:
          self.seqs, self.labels = self.load_dataset(self.testFilePath)

        self.max_length = max_length


    def load_dataset(self,path):
        df = pd.read_csv(path,names=['input','loc','membrane'],skiprows=1)
        df = df.loc[df['membrane'].isin(["M","S"])]
        self.labels_dic = {0:'Soluble',
                           1:'Insoluble'}

        df['labels'] = np.where(df['membrane']=='M', 1, 0)

        seq = list(df['input'])
        label = list(df['labels'])

        assert len(seq) == len(label)
        return seq, label

    def __len__(self):
        return len(self.labels)


    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        seq = " ".join("".join(self.seqs[idx].split()))
        seq = re.sub(r"[UZOB]", "X", seq)

        seq_ids = self.tokenizer(seq, truncation=True, padding='max_length', max_length=self.max_length)

        sample = {key: torch.tensor(val) for key, val in seq_ids.items()}
        sample['labels'] = torch.tensor(self.labels[idx])

        return sample


train_dataset = DeepLocDataset(split="train", tokenizer_name=model_name, max_length=256)
val_dataset = DeepLocDataset(split="valid", tokenizer_name=model_name, max_length=256)
test_dataset = DeepLocDataset(split="test", tokenizer_name=model_name, max_length=256)


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def model_init():
  return AutoModelForSequenceClassification.from_pretrained(model_name)


training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=10,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
    do_train=True,
    do_eval=True,
    evaluation_strategy="epoch",
    gradient_accumulation_steps=64,
    run_name="ProBert-BFD-IS",
    seed=3
)

trainer = Trainer(
    model_init=model_init,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics = compute_metrics,
)

trainer.train()

trainer.save_model('models/')

predictions, label_ids, metrics = trainer.predict(test_dataset)

idx = 0
sample_ground_truth = test_dataset.labels_dic[int(test_dataset[idx]['labels'])]
sample_predictions =  test_dataset.labels_dic[np.argmax(predictions[idx], axis=0)]
sample_sequence = test_dataset.tokenizer.decode(test_dataset[idx]['input_ids'], skip_special_tokens=True)


print("Sequence: {} \nGround Truth is: {}\nprediction is: {}".format(sample_sequence,
                                                                      sample_ground_truth,
                                                                      sample_predictions))
