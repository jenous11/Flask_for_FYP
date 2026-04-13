"""
================================================
 CYBERBULLYING DETECTION — VISUALIZATION
 (6-Class Multiclass Dataset)
================================================
 Dataset columns:
   - Text             : cleaned tweet text
   - category         : original label name
   - binary_label     : 0 = Not Bullying, 1 = Bullying
   - multiclass_label : 0-5 numeric class

 Visualizations:
   1. Bar Chart        — count per class
   2. Data Distribution — pie + horizontal bar
   3. Word Cloud       — one per category
   4. Binary Distribution — bullying vs safe
================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# ── Load Dataset ──────────────────────────────
print("Loading dataset...")
df = pd.read_csv('dataset_cleaned.csv')
df = df.dropna(subset=['Text'])
df['Text'] = df['Text'].astype(str)

# Color for each category
CATEGORY_COLORS = {
    'not_cyberbullying'  : '#2ecc71',
    'gender'             : '#9b59b6',
    'religion'           : '#e67e22',
    'other_cyberbullying': '#3498db',
    'age'                : '#e74c3c',
    'ethnicity'          : '#e91e63',
}

print(f"Total rows  : {len(df)}")
print(f"\nClass Distribution:\n{df['category'].value_counts()}")

os.makedirs('outputs', exist_ok=True)


# ════════════════════════════════════════════
# 1. BAR CHART — Count per category
# ════════════════════════════════════════════
def plot_bar_chart(df):
    counts = df['category'].value_counts()
    colors = [CATEGORY_COLORS.get(c, '#95a5a6') for c in counts.index]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(counts.index, counts.values, color=colors, edgecolor='white', linewidth=1.5)

    total = len(df)
    for bar, val in zip(bars, counts.values):
        pct = val / total * 100
        plt.text(bar.get_x() + bar.get_width()/2, val + 100,
                 f'{val:,}\n({pct:.1f}%)',
                 ha='center', fontsize=10, fontweight='bold')

    plt.title('Cyberbullying Category — Tweet Count', fontsize=16, fontweight='bold')
    plt.xlabel('Category', fontsize=13)
    plt.ylabel('Number of Tweets', fontsize=13)
    plt.xticks(rotation=25, ha='right')
    plt.ylim(0, max(counts.values) * 1.18)
    plt.tight_layout()
    plt.savefig('outputs/bar_chart.png', dpi=150)
    plt.show()
    print("✅ Bar chart saved → outputs/bar_chart.png")


# ════════════════════════════════════════════
# 2. DATA DISTRIBUTION — Pie + Horizontal Bar
# ════════════════════════════════════════════
def plot_data_distribution(df):
    counts = df['category'].value_counts()
    colors = [CATEGORY_COLORS.get(c, '#95a5a6') for c in counts.index]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Dataset Class Distribution', fontsize=16, fontweight='bold')

    axes[0].pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 11}
    )
    axes[0].set_title('Class Proportion', fontsize=13)

    bars = axes[1].barh(counts.index, counts.values, color=colors, edgecolor='white')
    for bar, val in zip(bars, counts.values):
        axes[1].text(val + 100, bar.get_y() + bar.get_height()/2,
                     f'{val:,}', va='center', fontsize=11)
    axes[1].set_title('Class Count', fontsize=13)
    axes[1].set_xlabel('Number of Tweets', fontsize=12)
    axes[1].set_xlim(0, max(counts.values) * 1.12)

    plt.tight_layout()
    plt.savefig('outputs/data_distribution.png', dpi=150)
    plt.show()
    print("✅ Data distribution saved → outputs/data_distribution.png")


# ════════════════════════════════════════════
# 3. BINARY DISTRIBUTION
# ════════════════════════════════════════════
def plot_binary_distribution(df):
    counts = df['binary_label'].value_counts().sort_index()
    labels = ['Not Bullying', 'Bullying']
    colors = ['#2ecc71', '#e74c3c']

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Binary Label Distribution', fontsize=15, fontweight='bold')

    axes[0].pie(counts.values, labels=labels, autopct='%1.1f%%',
                colors=colors, startangle=90,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[0].set_title('Proportion', fontsize=13)

    bars = axes[1].bar(labels, counts.values, color=colors, edgecolor='white', width=0.5)
    total = len(df)
    for bar, val in zip(bars, counts.values):
        pct = val / total * 100
        axes[1].text(bar.get_x() + bar.get_width()/2, val + 200,
                     f'{val:,}\n({pct:.1f}%)', ha='center', fontsize=11, fontweight='bold')
    axes[1].set_title('Count', fontsize=13)
    axes[1].set_ylabel('Number of Tweets', fontsize=12)
    axes[1].set_ylim(0, max(counts.values) * 1.15)

    plt.tight_layout()
    plt.savefig('outputs/binary_distribution.png', dpi=150)
    plt.show()
    print("✅ Binary distribution saved → outputs/binary_distribution.png")


# ════════════════════════════════════════════
# 4. WORD CLOUD — One per category
# ════════════════════════════════════════════
WORDCLOUD_COLORS = {
    'not_cyberbullying'  : 'Greens',
    'gender'             : 'Purples',
    'religion'           : 'Oranges',
    'other_cyberbullying': 'Blues',
    'age'                : 'Reds',
    'ethnicity'          : 'RdPu',
}

def plot_wordcloud(df, category):
    sample = df[df['category'] == category]['Text'].dropna().astype(str)
    if len(sample) > 5000:
        sample = sample.sample(5000, random_state=42)
    text = ' '.join(sample)

    if not text.strip():
        print(f"⚠️ No text for {category}, skipping.")
        return

    colormap = WORDCLOUD_COLORS.get(category, 'viridis')
    wordcloud = WordCloud(
        width=900, height=450,
        background_color='white',
        colormap=colormap,
        max_words=120,
        collocations=False
    ).generate(text)

    plt.figure(figsize=(13, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud — {category.replace("_", " ").title()}',
              fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    filename = f'outputs/wordcloud_{category}.png'
    plt.savefig(filename, dpi=150)
    plt.show()
    print(f"✅ Word cloud saved → {filename}")


# ── Run All ───────────────────────────────────
if __name__ == '__main__':
    plot_bar_chart(df)
    plot_data_distribution(df)
    plot_binary_distribution(df)

    for category in df['category'].unique():
        plot_wordcloud(df, category)

    print("\n🎉 All visualizations saved in outputs/ folder.")
    print("\nFiles saved:")
    for f in sorted(os.listdir('outputs')):
        print(f"  📊 outputs/{f}")
