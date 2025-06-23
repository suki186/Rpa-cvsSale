from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def visualize_wordclouds_comparison(freq_dict1, freq_dict2, label1='GS25', label2='CU', font_path='THELeft.ttf', return_fig=False):
    """
    두 워드클라우드를 나란히 시각화하거나 Streamlit에서 사용할 수 있도록 fig 객체 반환
    - freq_dict: {단어: 빈도} 형태의 딕셔너리
    """
    mask_image = np.array(Image.open('assets/mask.png'))

    wc1 = WordCloud(
        font_path=font_path,
        background_color='black',
        width=1000,
        height=700,
        colormap='Blues',
        mask=mask_image,
    ).generate_from_frequencies(freq_dict1)

    wc2 = WordCloud(
        font_path=font_path,
        background_color='black',
        width=1000,
        height=700,
        colormap='PiYG',
        mask=mask_image
    ).generate_from_frequencies(freq_dict2)

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    axs[0].imshow(wc1, interpolation='bilinear')
    axs[0].set_title(label1, fontsize=16)
    axs[0].axis('off')

    axs[1].imshow(wc2, interpolation='bilinear')
    axs[1].set_title(label2, fontsize=16)
    axs[1].axis('off')

    plt.tight_layout()

    if return_fig:
        return fig
    else:
        plt.show()
