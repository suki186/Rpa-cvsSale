# generate_wordcloud.py

from wordcloudf import WordCloud
import matplotlib.pyplot as plt


def generate_wordcloud_from_frequencies(frequencies: dict, title: str = '', font_path: str = 'THELeft.ttf', output_file: str = None):
    """
    워드클라우드 생성 및 시각화
    - frequencies: {단어: 빈도} 형태의 딕셔너리
    """
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        width=800,
        height=400
    ).generate_from_frequencies(frequencies)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    if title:
        plt.title(title, fontsize=18)
    if output_file:
        plt.savefig(output_file, bbox_inches='tight')
    plt.show()
