import os
import requests

KEY1 = os.environ["COMPUTER_VISION_API_KEY1"]

endpoint = 'https://mottyan-solution.cognitiveservices.azure.com/'

def translate_eng_image_to_ja(image_url=None, image=None):
    print("translate_eng_image_to_ja : in")

    if image_url is None and image is None:
        return '必要な情報が足りません'

    params = {'visualFeatures': 'Categories,Description,Color'}

    if image_url:
        headers = {
            'Ocp-Apim-Subscription-Key': KEY1,
            'Content-Type': 'application/json',
        }
        data = {'url': image_url}
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            json=data
        )

    elif image is not None:
        headers = {
            'Ocp-Apim-Subscription-Key': KEY1,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(
            endpoint,
            headers=headers,
            params=params,
            data=image,
        )

    status = response.status_code
    data = response.json()

    print(data)

    if status != 200:

        if data['code'] == 'InvalidImageSize':
            text = '画像のサイズが大きすぎます'

        elif data['code'] == 'InvalidImageUrl':
            text = 'この画像URLからは取得できません'

        elif data['code'] == 'InvalidImageFormat':
            text = '対応していない画像形式です'

        else:
            text = 'エラーが発生しました'

        print(status, data)
        return text

    text = ''
    for region in data['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word.get('text', '')
                if data['language'] != 'en':
                    text += ' '
        text += '\n'

    if len(text) == 0:
        text += '文字が検出できませんでした'

    print('text:', text)
    return text


if __name__ == "__main__":
    get_text_by_ms(image_url)