# Captcha Service

用于识别验证码的服务

目前只有大物实验平台需要用到该服务来识别其登录验证码。

`captchas` 目前为大物实验平台的验证码的数据，用于配合 `test.py` 脚本测试验证码识别的成功率。

`downloader.py` 是验证码下载器，运行和将自动从大物实验平台下载验证码图片，然后需要人工去输入验证码，通过这样的方式得到 `captchas` 中的测试数据。

该项目使用 `uv` 作为包管理工具。

## 使用

```bash
# 构建 docker 镜像
docker build . -t captcha_service
# 创建容器
docker create --name captcha_service -p 5000:5000 captcha_service
# 启动容器
docker start captcha_service
# 关闭容器
docker stop captcha_service
# 删除容器
docker rm captcha_service
```