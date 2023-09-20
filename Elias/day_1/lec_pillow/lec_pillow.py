from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter

import os
from enum import Enum
from icecream import ic
from datetime import datetime

ic.configureOutput(includeContext=True)

class FILTER(Enum):
    BLUR = 0
    CONTOUR = 1
    DETAIL = 2
    EDGE_ENHANCE = 3
    EDGE_ENHANCE_MORE = 4
    EMBOSS = 5
    FIND_EDGES = 6
    SHARPEN = 7
    SMOOTH = 8
    SMOOTH_MORE = 9

class Pillow:
    ################################################
    # Get Image File Information
    ################################################
    def get_info(self, img_file_path):
        img = Image.open(img_file_path)
        return ({'FileName': img.filename,
                 'Format': img.format,
                 'Format Desc.': img.format_description,
                 'Width': img.width,
                 'Height': img.height,
                 'Mode': img.mode
                 })

    ###############################################################
    # Convert Image Format
    ###############################################################
    def convert_format(self, img_file_path, format):  # format: png, jpg, jpeg, bmp, ...
        img = Image.open(img_file_path)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        # images/buz.jpg --> images/buz.png
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> images/
        # absdir = os.path.abspath(img_file_path) # d:\source\lg_autotest_23_08\Elias.....
        file_name = os.path.basename(img_file_path)  # buz.jpg
        file_name = file_name.split('.')[0]  # buz.jpg -> buz
        file_name += '.' + format  # buz -> buz.png
        path = os.path.join(dir, file_name)  # ./images + buz.png --> ./images/buz.png
        img.save(path)
        return path

    ###############################################################
    # Make Thumb Image
    ###############################################################
    def make_thumbnail(self, img_file_path, width=300, height=300):
        img = Image.open(img_file_path)
        size = width, height
        img.thumbnail(size)
        dir = os.path.dirname(img_file_path)  # images/buz.jpg --> images/
        file_name = os.path.basename(img_file_path)
        path = os.path.join(dir, 'thumb_' + file_name)  # buz.jpg -> thumb_buz.jpg
        img.save(path)
        return path

    ###############################################################
    # Crop Image
    ###############################################################
    def crop_image(self, img_file_path, from_x, from_y, to_x, to_y):
        img = Image.open(img_file_path)
        img = img.crop((from_x, from_y, to_x, to_y))
        dir = os.path.dirname(img_file_path)  # images/buz.jpg --> images/
        file_name = os.path.basename(img_file_path)
        path = os.path.join(dir, 'crop_' + file_name)  # buz.jpg -> thumb_buz.jpg
        img.save(path)
        return path

    ###############################################################
    # Resize Image
    ###############################################################
    def resize_image(self, img_file_path, width, height):
        img = Image.open(img_file_path)
        img = img.resize((width, height))
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> images/
        file_name = os.path.basename(img_file_path)  # buz.jpg
        path = os.path.join(dir, 'resize_' + file_name)
        img.save(path)  # images/resize_buz.jpg
        return path

    ###############################################################
    # Rotate Image
    ###############################################################
    def rotate_image(self, img_file_path, degree, expand=True):
        img = Image.open(img_file_path)
        img = img.rotate(degree, expand=expand)
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> images/
        file_name = os.path.basename(img_file_path)  # buz.jpg
        path = os.path.join(dir, 'rotate_' + file_name)
        img.save(path)  # images/rotate_buz.jpg
        return path

    ###############################################################
    # Type Text on image
    ###############################################################
    def draw_text_on_image(self, img_file_path, xPos, yPos, text, size, color, font_name='arial.ttf'):
        img = Image.open(img_file_path)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_name, size)
        draw.text((xPos, yPos), text, color, font=font)
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> images/
        file_name = os.path.basename(img_file_path)  # buz.jpg
        path = os.path.join(dir, 'text_' + file_name)
        img.save(path)  # images/rotate_buz.jpg
        return path

    ###############################################################
    # Apply filter
    ###############################################################
    def apply_filter(self, img_file_path, filter):
        img = Image.open(img_file_path)

        if filter == FILTER.BLUR:
            filter = ImageFilter.BLUR
        elif filter == FILTER.CONTOUR:
            filter = ImageFilter.CONTOUR
        elif filter == FILTER.DETAIL:
            filter = ImageFilter.DETAIL
        elif filter == FILTER.EDGE_ENHANCE:
            filter = ImageFilter.EDGE_ENHANCE
        elif filter == FILTER.EDGE_ENHANCE_MORE:
            filter = ImageFilter.EDGE_ENHANCE_MORE
        elif filter == FILTER.EMBOSS:
            filter = ImageFilter.EMBOSS
        elif filter == FILTER.FIND_EDGES:
            filter = ImageFilter.FIND_EDGES
        elif filter == FILTER.SHARPEN:
            filter = ImageFilter.SHARPEN
        elif filter == FILTER.SMOOTH:
            filter = ImageFilter.SMOOTH
        elif filter == FILTER.SMOOTH_MORE:
            filter = ImageFilter.SMOOTH_MORE

        img = img.filter(filter)
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> imgaes/
        file_name = os.path.basename(img_file_path)  # buz.jpg
        path = os.path.join(dir, filter.name + '_' + file_name)
        img.save(path)  # images/blur_buz.jpg
        return path

    ###############################################################
    # 2x2
    # 1,2,3,4 --> one image
    ###############################################################

    ###############################################################
    # Create Canvas
    ###############################################################
    def merge_create_image(self, row, column, img_file_path):
        img = Image.open(img_file_path)
        new_image = Image.new('RGB', (img.width * column, img.height * row))
        return new_image

    ###############################################################
    # Paste Image
    ###############################################################
    def merge_paste_image(self, merge_image, row, column, img_file_path):
        img = Image.open(img_file_path)
        merge_image.paste(img, (img.width * column, img.height * row))

    ###############################################################
    # Save Image
    ###############################################################
    def merge_save(self, merge_image, img_file_path):
        dir = os.path.dirname(img_file_path)  # images/buz.jpg -> images/
        file_name = os.path.basename(img_file_path)  # buz.jpg
        path = os.path.join(dir, 'merge_' + file_name)
        merge_image.save(path)  # images/merge_buz.jpg
        return path


if __name__ == '__main__':
    img_file_path = './images/buz.jpg'
    pillow = Pillow()

    ################################################
    # 이미지 정보출력
    ################################################
    ic(pillow.get_info(img_file_path))

    ###############################################################
    # 이미지 포맷변경
    ###############################################################
    new_image = pillow.convert_format(img_file_path, 'png')
    img_info = pillow.get_info(new_image)
    ic(img_info)

    ###############################################################
    # 썸네일 이미지 만들기
    ###############################################################
    new_image = pillow.make_thumbnail(img_file_path)
    ic(new_image)
    ic(pillow.get_info(new_image))

    ###############################################################
    # 이미지 잘라내기(Crop)
    ###############################################################
    new_image = pillow.crop_image(img_file_path, 100, 100, 200, 200)
    ic(new_image)
    ic(pillow.get_info(new_image))

    ###############################################################
    # 이미지 크기변경
    ###############################################################
    new_image = pillow.resize_image(img_file_path, 300, 300)
    ic(new_image)

    ###############################################################
    # 이미지 회전
    ###############################################################
    # new_image = pillow.rotate_image(img_file_path, 90, True)
    new_image = pillow.rotate_image(img_file_path, 90, False)
    ic(new_image)

    ###############################################################
    # 이미지에 글쓰기
    ###############################################################
    new_image = pillow.draw_text_on_image(img_file_path, 500, 500, 'Hellow World', 30, 'red')
    ic(new_image)

    ###############################################################
    # 필터 적용
    ###############################################################
    filter_list = [FILTER.BLUR, FILTER.CONTOUR, FILTER.DETAIL,
                   FILTER.EDGE_ENHANCE, FILTER.EDGE_ENHANCE_MORE, FILTER.EMBOSS, FILTER.FIND_EDGES,
                   FILTER.SHARPEN, FILTER.SMOOTH, FILTER.SMOOTH_MORE]

    for filter in filter_list:
        new_image = pillow.apply_filter(img_file_path, filter)
        ic(new_image)

    ###############################################################
    # Merge Image
    ###############################################################
    row = 2
    column = 3

    # 빈 캔버스 이미지 객체 생성
    merge_image = pillow.merge_create_image(row, column, img_file_path)

    # 각 행/열의 이미지 복사
    for _row in range(row):  # 0, 1
        for _column in range(column):  # 0, 1, 2
            pillow.merge_paste_image(merge_image, _row, _column, img_file_path)

    # Merged된 이미지 파일 저장
    new_image = pillow.merge_save(merge_image, img_file_path)
    ic(new_image)