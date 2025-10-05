import sys
import os
from services import pyocr_service

def get_files_info(directory):
    """获取目录下所有文件的信息字典"""
    files_info = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_info = {
                'filename': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath),
                'modified': os.path.getmtime(filepath)
            }
            files_info.append(file_info)
    return files_info

data_list = get_files_info('captchas')

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("usage: python test.py <ocr_type>")
        sys.exit(1)
    ocr_type = args[1]
    if ocr_type == 'default':
        read_img = pyocr_service.readimg
    else:
        print("Unknown ocr type.")
        sys.exit(1)
    
    total = len(data_list)
    accepted = 0
    for (index, i) in enumerate(data_list):
        ans = i['filename'][:-4]
        in_ans = read_img(i['filepath'])
        print(f"[{index + 1}] {"AC" if ans == in_ans else "WA"} {in_ans} / {ans}")
        if ans == in_ans:
            accepted = accepted + 1
    print(f"Total: {accepted}/{total} ({accepted / total * 100}%)")

