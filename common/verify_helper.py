#!/usr/bin/evn python
# coding=utf-8

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from common import random_helper

def create_verify_code(length = 4, size=(100, 40), img_type='jpg',
                        mode='RGB', bg_color=(255, 255, 255), fg_color=(0, 0, 255),
                        font_size=19, font_type='arial.ttf',
                        draw_lines=True, n_line=(2, 5),
                        draw_points=True, point_chance=5):
    """
    生成验证码图片
    :param length: 生成验证码数量
    :param size: 生成图片的宽和高
    :param img_type: 生成图片类型
    :param mode: 图片模式
    :param bg_color: 背景颜色
    :param fg_color: 字体颜色
    :param font_size: 字体大小
    :param font_type: 验证码字体，linux系统里需要绝对路径
    :param draw_lines: 是否绘制干扰线
    :param n_line: 干扰线数量
    :param draw_points: 是否绘制干扰点
    :param point_chance: 干扰点数量
    :return:
    """
    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    def create_line():
        line_num = random_helper.get_number_for_range(n_line[0], n_line[1])

        for i in range(line_num):
            begin = (random_helper.get_number_for_range(0, size[0]), random_helper.get_number_for_range(0, size[1]))
            end = (random_helper.get_number_for_range(0, size[0]), random_helper.get_number_for_range(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random_helper.get_number_for_range(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        c_chars = random_helper.get_string(length)
        strs = ' %s ' % ' '.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    if draw_lines:
        create_line()
    if draw_points:
        create_points()
    strs = create_strs()

    params = [1 - float(random_helper.get_number_for_range(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random_helper.get_number_for_range(1, 10)) / 100,
              float(random_helper.get_number_for_range(1, 2)) / 500,
              0.001,
              float(random_helper.get_number_for_range(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, strs

# if __name__ == '__main__':
#     code_img,capacha_code= create_verify_code()
#     code_img.save('xx_' + random_helper.get_string(3) + '.jpg','JPEG')