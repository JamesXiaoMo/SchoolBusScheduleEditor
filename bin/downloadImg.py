import os
import requests


def download_image(url, save_dir, filename=None):
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, filename)

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"图片已保存：{save_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"下载出错：{e}")
