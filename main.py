#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片批量加水印工具
支持文字水印，可设置位置、透明度、旋转角度
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def add_watermark(input_path, output_path, text, position="bottom-right",
                  opacity=128, font_size=36, angle=0, color=(255, 255, 255)):
    """添加文字水印"""
    with Image.open(input_path) as img:
        img = img.convert("RGBA")
        w, h = img.size

        # 创建透明图层
        watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        # 尝试加载字体
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

        # 计算文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # 计算位置
        margin = 20
        positions = {
            "top-left": (margin, margin),
            "top-right": (w - text_w - margin, margin),
            "bottom-left": (margin, h - text_h - margin),
            "bottom-right": (w - text_w - margin, h - text_h - margin),
            "center": ((w - text_w) // 2, (h - text_h) // 2),
        }
        x, y = positions.get(position, positions["bottom-right"])

        # 绘制文字
        draw.text((x, y), text, fill=color + (opacity,), font=font)

        # 旋转水印图层
        if angle != 0:
            watermark_layer = watermark_layer.rotate(angle, expand=False)

        # 合并图层
        result = Image.alpha_composite(img, watermark_layer)
        result = result.convert("RGB")
        result.save(output_path)


def batch_watermark(folder, output_folder, text, **kwargs):
    """批量添加水印"""
    folder = Path(folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    supported = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    count = 0

    for f in folder.iterdir():
        if not f.is_file() or f.suffix.lower() not in supported:
            continue
        out_path = output_folder / f.name
        try:
            add_watermark(f, out_path, text, **kwargs)
            print(f"[完成] {f.name}")
            count += 1
        except Exception as e:
            print(f"[失败] {f.name}: {e}")

    print(f"\n共处理 {count} 张图片")


def main():
    parser = argparse.ArgumentParser(description="图片批量加水印工具")
    parser.add_argument("folder", help="图片所在文件夹")
    parser.add_argument("-o", "--output", default="output", help="输出文件夹")
    parser.add_argument("--text", required=True, help="水印文字")
    parser.add_argument("--position", default="bottom-right",
                        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                        help="水印位置")
    parser.add_argument("--opacity", type=int, default=128, help="透明度 (0-255)")
    parser.add_argument("--font-size", type=int, default=36, help="字体大小")
    parser.add_argument("--angle", type=int, default=0, help="旋转角度")
    args = parser.parse_args()

    batch_watermark(
        args.folder, args.output, args.text,
        position=args.position,
        opacity=args.opacity,
        font_size=args.font_size,
        angle=args.angle,
    )


if __name__ == "__main__":
    main()
