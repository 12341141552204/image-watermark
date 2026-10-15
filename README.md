# 图片批量加水印工具 (image-watermark)

为图片批量添加文字水印。

## 功能

- 自定义水印文字
- 5 种位置（四角 + 居中）
- 可调节透明度、字体大小、旋转角度

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
# 右下角添加水印
python main.py ./images --text "My Watermark"

# 居中、半透明、30度旋转
python main.py ./images --text "CONFIDENTIAL" --position center --opacity 80 --angle 30
```

## 依赖

- Pillow
