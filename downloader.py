import os
import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import simpledialog

def download_captcha(url):
    """下载验证码GIF并返回PIL Image对象"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"下载验证码失败: {e}")
        return None

def extract_first_frame(gif_image):
    """从GIF中提取第一帧并转换为PNG格式"""
    try:
        gif_image.seek(0)  # 定位到第一帧
        return gif_image.copy()  # 返回第一帧的副本
    except Exception as e:
        print(f"提取第一帧失败: {e}")
        return gif_image  # 如果不是GIF，返回原图

def show_captcha_and_get_input(image):
    """显示验证码图片并获取用户输入"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 创建临时窗口显示验证码
    plt.figure(figsize=(5, 3))
    plt.imshow(image)
    plt.axis('off')
    plt.title("请输入验证码")
    plt.show(block=False)
    
    # 获取用户输入
    captcha_text = simpledialog.askstring("验证码输入", "请输入验证码:")
    
    plt.close()
    root.destroy()
    return captcha_text

def save_captcha(image, text, save_folder='captchas'):
    """以验证码文本为文件名保存PNG图片"""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    if text:  # 只有当用户输入了验证码才保存
        filename = f"{save_folder}/{text}.png"
        image.save(filename, "PNG")
        print(f"验证码已保存为: {filename}")
    else:
        print("未输入验证码，图片未保存")

def main():
    # 配置参数
    captcha_url = "http://10.62.106.112/Ashx/CheckCode.ashx?t=0.29911677684547566"  # 替换为实际的验证码URL
    save_folder = "captchas"
    
    while True:
        print("\n正在下载验证码...")
        gif_img = download_captcha(captcha_url)
        
        if gif_img:
            # 提取第一帧并转换为PNG
            png_img = extract_first_frame(gif_img)
            
            # 显示并获取输入
            captcha_text = show_captcha_and_get_input(png_img)
            
            # 保存图片
            save_captcha(png_img, captcha_text, save_folder)

if __name__ == "__main__":
    # 检查并创建保存目录
    if not os.path.exists("captchas"):
        os.makedirs("captchas")
    
    # 检查依赖
    try:
        import matplotlib.pyplot as plt
        from PIL import Image
        import tkinter as tk
    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install pillow matplotlib requests")
        exit(1)
    
    main()