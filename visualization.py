"""
================================================
 CYBERBULLYING DETECTION — VISUALIZATION
 (6-Class Multiclass | Multilingual Dataset)
================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import glob

# ── Load Dataset ──────────────────────────────
print("Loading dataset...")
df = pd.read_csv('cyberguard_dataset.csv')
df = df.dropna(subset=['Text'])
df['Text'] = df['Text'].astype(str)

CATEGORY_COLORS = {
    'not_cyberbullying'  : '#2ecc71',
    'gender'             : '#9b59b6',
    'religion'           : '#e67e22',
    'other_cyberbullying': '#3498db',
    'age'                : '#e74c3c',
    'ethnicity'          : '#e91e63',
}

print(f"Total rows  : {len(df):,}")
print(f"\nClass Distribution:\n{df['category'].value_counts()}")
if 'language' in df.columns:
    print(f"\nLanguage Distribution:\n{df['language'].value_counts()}")

os.makedirs('outputs', exist_ok=True)


# ════════════════════════════════════════════
# FONT HELPER
# ════════════════════════════════════════════
def get_font_path():
    """
    Find a font that renders BOTH English (Latin) AND Nepali (Devanagari).
    First checks the project folder for NirmalaUI.ttf (extracted from Nirmala.ttc).
    """
    # ── PRIORITY 1: Project folder (manually extracted NirmalaUI.ttf) ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(script_dir, 'NirmalaUI.ttf')
    if os.path.exists(local_path):
        print(f"   Using font: {local_path}")
        return local_path

    # Also check current working directory
    if os.path.exists('NirmalaUI.ttf'):
        print(f"   Using font: NirmalaUI.ttf (cwd)")
        return 'NirmalaUI.ttf'

    # ── PRIORITY 2: Windows Fonts folder ──
    candidate_dirs = [
        r'C:\Windows\Fonts',
        r'C:\WINDOWS\Fonts',
        r'C:\windows\fonts',
        os.path.expandvars(r'%SystemRoot%\Fonts'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
    ]
    preferred = ['NirmalaUI.ttf', 'NirmalaB.ttf', 'Mangal.ttf', 'Arial.ttf']

    for font_name in preferred:
        for font_dir in candidate_dirs:
            path = os.path.join(font_dir, font_name)
            if os.path.exists(path):
                print(f"   Using font: {path}")
                return path

    # ── PRIORITY 3: Glob search ──
    for font_dir in candidate_dirs:
        if os.path.isdir(font_dir):
            for font_name in preferred:
                matches = glob.glob(os.path.join(font_dir, '**', font_name), recursive=True)
                if matches:
                    print(f"   Found font: {matches[0]}")
                    return matches[0]

    print("   WARNING: No Devanagari-compatible font found.")
    print("   FIX: Run this in PowerShell to extract NirmalaUI.ttf:")
    print("   python -c \"from fontTools.ttLib import TTCollection; TTCollection('C:/Windows/Fonts/Nirmala.ttc').fonts[0].save('NirmalaUI.ttf'); print('Done!')\"")
    return None


# ════════════════════════════════════════════
# 1. BAR CHART
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
                 f'{val:,}\n({pct:.1f}%)', ha='center', fontsize=10, fontweight='bold')

    plt.title('Cyberbullying Category — Tweet Count', fontsize=16, fontweight='bold')
    plt.xlabel('Category', fontsize=13)
    plt.ylabel('Number of Tweets', fontsize=13)
    plt.xticks(rotation=25, ha='right')
    plt.ylim(0, max(counts.values) * 1.18)
    plt.tight_layout()
    plt.savefig('outputs/bar_chart.png', dpi=150)
    plt.close()
    print("✅ Bar chart saved → outputs/bar_chart.png")


# ════════════════════════════════════════════
# 2. DATA DISTRIBUTION
# ════════════════════════════════════════════
def plot_data_distribution(df):
    counts = df['category'].value_counts()
    colors = [CATEGORY_COLORS.get(c, '#95a5a6') for c in counts.index]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Dataset Class Distribution', fontsize=16, fontweight='bold')

    axes[0].pie(counts.values, labels=counts.index, autopct='%1.1f%%',
                colors=colors, startangle=90,
                wedgeprops={'edgecolor': 'white', 'linewidth': 2},
                textprops={'fontsize': 11})
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
    plt.close()
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

    axes[0].pie(counts.values, labels=labels, autopct='%1.1f%%', colors=colors,
                startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
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
    plt.close()
    print("✅ Binary distribution saved → outputs/binary_distribution.png")


# ════════════════════════════════════════════
# 4. LANGUAGE DISTRIBUTION
# ════════════════════════════════════════════
def plot_language_distribution(df):
    if 'language' not in df.columns:
        print("Warning: No 'language' column found, skipping language chart.")
        return

    lang_counts = df['language'].value_counts()
    LANG_COLORS = {
        'english'           : '#3498db',
        'nepali_devanagari' : '#e74c3c',
        'romanized_nepali'  : '#e67e22',
        'nepali_mixed'      : '#9b59b6',
        'other'             : '#95a5a6',
    }
    colors = [LANG_COLORS.get(l, '#95a5a6') for l in lang_counts.index]
    lang_labels = {
        'english'           : 'English',
        'nepali_devanagari' : 'Nepali (Devanagari)',
        'romanized_nepali'  : 'Romanized Nepali',
        'nepali_mixed'      : 'Code-Mixed',
        'other'             : 'Other',
    }
    display_labels = [lang_labels.get(l, l) for l in lang_counts.index]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Language Distribution — Multilingual Dataset', fontsize=15, fontweight='bold')

    wedges, _, _ = axes[0].pie(
        lang_counts.values, labels=None,
        autopct=lambda p: f"{p:.1f}%" if p > 3 else "",
        colors=colors, startangle=90, pctdistance=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
        textprops={'fontsize': 11}
    )
    axes[0].legend(wedges, display_labels, loc='lower center',
                   bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=10, frameon=False)
    axes[0].set_title('Language Proportion', fontsize=13)

    bars = axes[1].barh(display_labels, lang_counts.values, color=colors, edgecolor='white')
    for bar, val in zip(bars, lang_counts.values):
        axes[1].text(val + 100, bar.get_y() + bar.get_height()/2,
                     f'{val:,}', va='center', fontsize=11)
    axes[1].set_title('Language Count', fontsize=13)
    axes[1].set_xlabel('Number of Rows', fontsize=12)
    axes[1].set_xlim(0, max(lang_counts.values) * 1.15)

    plt.tight_layout()
    plt.savefig('outputs/language_distribution.png', dpi=150)
    plt.close()
    print("✅ Language distribution saved → outputs/language_distribution.png")


# ════════════════════════════════════════════
# 5. WORD CLOUD — One per category
# ════════════════════════════════════════════
WORDCLOUD_COLORS = {
    'not_cyberbullying'  : 'Greens',
    'gender'             : 'Purples',
    'religion'           : 'Oranges',
    'other_cyberbullying': 'Blues',
    'age'                : 'Reds',
    'ethnicity'          : 'RdPu',
}

_FONT_PATH = None

def plot_wordcloud(df, category):
    global _FONT_PATH
    if _FONT_PATH is None:
        _FONT_PATH = get_font_path()

    sample = df[df['category'] == category]['Text'].dropna().astype(str)
    if len(sample) > 5000:
        sample = sample.sample(5000, random_state=42)
    text = ' '.join(sample)

    if not text.strip():
        print(f"Warning: No text for {category}, skipping.")
        return

    colormap = WORDCLOUD_COLORS.get(category, 'viridis')

    wordcloud = WordCloud(
        width=900, height=450,
        background_color='white',
        colormap=colormap,
        max_words=120,
        collocations=False,
        font_path=_FONT_PATH,
        regexp=r'[\w\u0900-\u097F]+',
    ).generate(text)

    plt.figure(figsize=(13, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Word Cloud — {category.replace("_", " ").title()}',
              fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    filename = f'outputs/wordcloud_{category}.png'
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"✅ Word cloud saved → {filename}")


# ── Run All ───────────────────────────────────
if __name__ == '__main__':
    plot_bar_chart(df)
    plot_data_distribution(df)
    plot_binary_distribution(df)
    plot_language_distribution(df)

    for category in df['category'].unique():
        plot_wordcloud(df, category)

    print("\n✅ All visualizations saved in outputs/ folder.")
    print("\nFiles saved:")
    for f in sorted(os.listdir('outputs')):
        print(f"  outputs/{f}")