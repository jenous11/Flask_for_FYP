"""
================================================
 CYBERBULLYING DETECTION — DISTILBERT TRAIN & SAVE
 (6-Class Multiclass Classification)
================================================
 Dataset columns used:
   - Text             : cleaned tweet text
   - multiclass_label : 0-5 numeric class

 Classes:
   0 → Not Cyberbullying
   1 → Gender
   2 → Religion
   3 → Other Cyberbullying
   4 → Age
   5 → Ethnicity

 Install:
   pip install transformers torch scikit-learn pandas
================================================
"""

import os
import pickle
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
import seaborn as sns

# ════════════════════════════════════════════
#  CONFIGURATION
# ════════════════════════════════════════════
MODEL_NAME = 'distilbert-base-uncased'
MAX_LEN    = 128
BATCH_SIZE = 16
EPOCHS     = 4
LR         = 2e-5
SAVE_DIR   = 'saved_model'
DATA_PATH  = 'dataset_cleaned.csv'

ID2LABEL = {
    0: 'Not Cyberbullying',
    1: 'Gender',
    2: 'Religion',
    3: 'Other Cyberbullying',
    4: 'Age',
    5: 'Ethnicity'
}
LABEL2ID = {v: k for k, v in ID2LABEL.items()}

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


# ════════════════════════════════════════════
#  STEP 1 — LOAD & CLEAN DATA
# ════════════════════════════════════════════
print("\n[1/6] Loading dataset...")
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=['Text'])
df['Text'] = df['Text'].astype(str).str.strip().str.lower()
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Total rows     : {len(df)}")
print(f"\nClass distribution:")
print(df['category'].value_counts())


# ════════════════════════════════════════════
#  STEP 2 — CLASS WEIGHTS
# ════════════════════════════════════════════
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.array([0, 1, 2, 3, 4, 5]),
    y=df['multiclass_label'].values
)
class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)
print(f"\nClass weights: {class_weights}")


# ════════════════════════════════════════════
#  STEP 3 — TRAIN / TEST SPLIT
# ════════════════════════════════════════════
X_train, X_test, y_train, y_test = train_test_split(
    df['Text'].values,
    df['multiclass_label'].values,
    test_size=0.2,
    random_state=42,
    stratify=df['multiclass_label'].values
)
print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")


# ════════════════════════════════════════════
#  STEP 4 — TOKENIZER & DATASET
# ════════════════════════════════════════════
print("\n[2/6] Loading DistilBERT tokenizer...")
tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)


class CyberbullyingDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts     = texts
        self.labels    = labels
        self.tokenizer = tokenizer
        self.max_len   = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            str(self.texts[idx]),
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids':      encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'label':          torch.tensor(self.labels[idx], dtype=torch.long)
        }


train_dataset = CyberbullyingDataset(X_train, y_train, tokenizer, MAX_LEN)
test_dataset  = CyberbullyingDataset(X_test,  y_test,  tokenizer, MAX_LEN)
train_loader  = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader   = DataLoader(test_dataset,  batch_size=BATCH_SIZE)


# ════════════════════════════════════════════
#  STEP 5 — DISTILBERT MODEL
# ════════════════════════════════════════════
print("\n[3/6] Loading DistilBERT model...")
model = DistilBertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=6,
    id2label=ID2LABEL,
    label2id=LABEL2ID
)
model = model.to(device)

optimizer   = AdamW(model.parameters(), lr=LR)
total_steps = len(train_loader) * EPOCHS
scheduler   = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=0,
    num_training_steps=total_steps
)
loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights_tensor)


# ════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════
def train_epoch(model, loader):
    model.train()
    total_loss = 0
    for step, batch in enumerate(loader):
        input_ids      = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels         = batch['label'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss    = loss_fn(outputs.logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        total_loss += loss.item()

        if (step + 1) % 100 == 0:
            print(f"  Step {step+1}/{len(loader)} Loss: {loss.item():.4f}")

    return total_loss / len(loader)


def evaluate(model, loader):
    model.eval()
    preds, truths = [], []
    with torch.no_grad():
        for batch in loader:
            input_ids      = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            p = torch.argmax(outputs.logits, dim=1)
            preds.extend(p.cpu().numpy())
            truths.extend(batch['label'].numpy())
    return preds, truths


# ════════════════════════════════════════════
#  STEP 6 — TRAINING LOOP
# ════════════════════════════════════════════
print(f"\n[4/6] Training for {EPOCHS} epochs...\n")

for epoch in range(EPOCHS):
    print(f"━━━ Epoch {epoch+1}/{EPOCHS} ━━━")
    loss        = train_epoch(model, train_loader)
    preds, true = evaluate(model, test_loader)
    acc         = accuracy_score(true, preds)
    print(f"Loss: {loss:.4f} | Accuracy: {acc*100:.2f}%\n")


# ════════════════════════════════════════════
#  STEP 7 — FINAL EVALUATION
# ════════════════════════════════════════════
print("[5/6] Final Evaluation Report:")
preds, true = evaluate(model, test_loader)
print(classification_report(
    true, preds,
    target_names=list(ID2LABEL.values())
))


# ════════════════════════════════════════════
#  STEP 8 — CONFUSION MATRIX
# ════════════════════════════════════════════
print("Generating confusion matrix...")
cm = confusion_matrix(true, preds)

plt.figure(figsize=(10, 8))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=list(ID2LABEL.values()),
    yticklabels=list(ID2LABEL.values())
)
plt.title('Confusion Matrix — DistilBERT 6-Class', fontsize=15, fontweight='bold')
plt.ylabel('Actual Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.show()
print("✅ Confusion matrix saved → confusion_matrix.png")


# ════════════════════════════════════════════
#  STEP 9 — SAVE MODEL
# ════════════════════════════════════════════
print(f"\n[6/6] Saving model to '{SAVE_DIR}/'...")
os.makedirs(SAVE_DIR, exist_ok=True)
model.save_pretrained(SAVE_DIR)
tokenizer.save_pretrained(SAVE_DIR)

label_info = {'id2label': ID2LABEL, 'label2id': LABEL2ID}
with open(f'{SAVE_DIR}/label_info.pkl', 'wb') as f:
    pickle.dump(label_info, f)

print(f"""
✅ Saved to '{SAVE_DIR}/':
   ├── config.json
   ├── model.safetensors
   ├── tokenizer_config.json
   ├── vocab.txt
   └── label_info.pkl

🎉 Training complete! Run app.py to start the Flask API.
""")