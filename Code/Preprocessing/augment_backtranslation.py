import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from tqdm import tqdm
import matplotlib.pyplot as plt


# === CONFIGURATION ===

INPUT_PATH = "<INPUT_FILE>.csv"        # e.g. "data/F_Private_dataset01.csv"
OUTPUT_PATH = "augmented_dataset.csv"  # Save location for the final augmented dataset

AUGMENT_COLUMN = "combined_text"
LABEL_COLUMN = "Issue Type"
SPLIT_COLUMN = "split"
AUGMENT_FLAG_COLUMN = "is_augmented"  # Flag augmented rows to avoid evaluating or validating on generated (non-original) data


# === LOAD DATA ===

df = pd.read_csv(INPUT_PATH, delimiter=';')

if SPLIT_COLUMN not in df.columns:
    df[SPLIT_COLUMN] = "train"
    df.loc[df.sample(frac=0.2, random_state=42).index, SPLIT_COLUMN] = "test"


# === LOAD MODELS ===

src_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-nl-en")
src_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-nl-en")

tgt_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-nl")
tgt_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-nl")


# === BACKTRANSLATION FUNCTION ===

def backtranslate(text, src_tok, src_mod, tgt_tok, tgt_mod):
    """
    Translates Dutch → English → Dutch to generate a paraphrased variant of the input.
    """
    try:
        # Dutch → English
        src_tokens = src_tok(text, return_tensors="pt", truncation=True, padding=True)
        src_translated = src_mod.generate(**src_tokens)
        english_text = src_tok.batch_decode(src_translated, skip_special_tokens=True)[0]

        # English → Dutch
        tgt_tokens = tgt_tok(english_text, return_tensors="pt", truncation=True, padding=True)
        tgt_translated = tgt_mod.generate(**tgt_tokens)
        backtranslated_text = tgt_tok.batch_decode(tgt_translated, skip_special_tokens=True)[0]

        return backtranslated_text
    except Exception as e:
        print(f"Error backtranslating: {e}")
        return text


# === CLASS DISTRIBUTION BEFORE ===

train_df = df[df[SPLIT_COLUMN] == "train"].copy()
print("Class distribution BEFORE augmentation:")
print(train_df[LABEL_COLUMN].value_counts())
print()

class_counts = train_df[LABEL_COLUMN].value_counts()
target_count = int(class_counts.median())
print(f"Balancing to median class size: {target_count}\n")


# === AUGMENTATION LOOP ===

aug_rows = []
for label, count in class_counts.items():
    if count >= target_count:
        continue

    needed = target_count - count
    if label == 'Overig':
        needed = 2 * count

    class_rows = train_df[train_df[LABEL_COLUMN] == label].sample(n=needed, replace=True, random_state=42)

    for _, row in tqdm(class_rows.iterrows(), total=needed, desc=f"Augmenting '{label}'"):
        original_text = row[AUGMENT_COLUMN]
        new_text = backtranslate(original_text, src_tokenizer, src_model, tgt_tokenizer, tgt_model)

        augmented_row = row.copy()
        augmented_row[AUGMENT_COLUMN] = new_text
        augmented_row[AUGMENT_FLAG_COLUMN] = True
        augmented_row[SPLIT_COLUMN] = "train"
        aug_rows.append(augmented_row)


# === FINALIZE OUTPUT ===

df[AUGMENT_FLAG_COLUMN] = False
aug_df = pd.DataFrame(aug_rows)
final_df = pd.concat([df, aug_df], ignore_index=True)


# === CLASS DISTRIBUTION AFTER ===

print("Class distribution AFTER augmentation:")
print(final_df[final_df[SPLIT_COLUMN] == "train"][LABEL_COLUMN].value_counts())


# === OPTIONAL PLOTTING ===

def plot_class_distribution(df, title):
    counts = df[LABEL_COLUMN].value_counts()
    counts.plot(kind="bar", title=title)
    plt.ylabel("Count")
    plt.xlabel("Class")
    plt.tight_layout()
    plt.show()

plot_class_distribution(train_df, "Before Augmentation")
plot_class_distribution(final_df[final_df[SPLIT_COLUMN] == "train"], "After Augmentation")


# === SAVE OUTPUT ===

final_df.to_csv(OUTPUT_PATH, index=False)
print(f"\nAugmented dataset saved to '{OUTPUT_PATH}'")
