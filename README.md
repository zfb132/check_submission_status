# 使用说明
本程序会自动登录`Scholar One`投稿系统，获取当前稿件的状态，并将状态（若状态发生变化）发送到指定邮箱  
可以配合`crontab`或者`timer`定时运行，实现自动化检测稿件状态的功能  

## 1. 安装谷歌浏览器
Windows直接下载安装`exe`文件即可  
Linux系统下，直接下载`deb`文件安装即可

## 2. 安装谷歌浏览器驱动
[点击这里下载](https://chromedriver.chromium.org/downloads)  
根据提示下载对应版本的驱动（注意谷歌浏览器版本号、操作系统类型必须匹配）压缩包，解压出可执行文件`chromedriver(.exe)`

## 3. 检测是否安装成功
```bash
chromedriver --version

# ChromeDriver 115.0.5790.170 (cc0d30c2ca5577520c8646671513241faa0bc105-refs/branch-heads/5790@{#1923})
```

## 4. 安装依赖
```bash
pip install bs4 splinter selenium lxml
```

## 5. 修改配置
重命名`config.py`文件为`config.example.py`文件，修改其中的配置项

## 6. 运行
```bash
python3 main.py
```