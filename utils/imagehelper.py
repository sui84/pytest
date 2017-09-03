#encoding=utf-8
import exifread
import urllib2
import json
import shutil
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import pyexiv2 as ev


class ImageHelper(object):

    def __init__(self):
        self.font = ImageFont.truetype(r'C:\Windows\Fonts\mingliu.ttc', 14)
        self.infile = 'D:\\temp\\test.bmp'
        self.outfile = 'D:\\temp\\test2.bmp'
        pass

    def GenImageByText(self,text,size,outf):
        textsize =  self.font.getsize(text)
        im = Image.new("RGB", size, (255, 255, 255))
        dr = ImageDraw.Draw(im)
        w, h = dr.textsize(text, self.font)
        dr.text(textsize, text, font=self.font, fill="#000000")
        #print dr.textsize(text)
        im.save(outf)

    def PutTextOnImage(self,text):
        textsize =  self.font.getsize(text)
        im =Image.open(self.infile )
        dr = ImageDraw.Draw(im)
        w, h = dr.textsize(text, self.font)
        dr.text(textsize, text, font=self.font, fill="#000000")
        im.save(outf)

    def GetImageInfo(self,fpath,type=1):
        img=Image.open(fpath)
        print "format:%s,size:%s,mode:%s,dpi:%s,compression:%s" % (img.format, str(img.size), img.mode, img.info.get('dpi'), img.info.get('compression'))
        with open(fpath, 'rb') as f:
            tags = exifread.process_file(f)
            if type == 1:  #简单
                infostr = u"经度:%s,纬度:%s,照相机:%s,时间:%s" % (tags.get('GPS GPSLongitude'),tags.get('GPS GPSLatitude'),tags.get('Image Software'),tags.get('EXIF DateTimeOriginal'))
                print infostr
                return infostr
            elif type == 2: #全部
                for tag in tags.keys():
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                        print "Key: %s, value %s" % (tag, tags[tag])
                return None
            elif type == 3:
                print tags.get('GPS GPSLatitude'),tags.get('GPS GPSLongitude')
                wdu = self.ParseGps(str(tags.get('GPS GPSLatitude')).lstrip('[').rstrip(']'))
                jdu = self.ParseGps(str(tags.get('GPS GPSLongitude')).lstrip('[').rstrip(']'))
                return {"wdu":wdu,"jdu":jdu}

    def ParseGps(self,titude):
        first_number = titude.split(',')[0]
        second_number = titude.split(',')[1]
        third_number = titude.split(',')[2]
        third_number_parent = third_number.split('/')[0]
        third_number_child = third_number.split('/')[1]
        third_number_result = float(third_number_parent) / float(third_number_child)
        return float(first_number) + float(second_number)/60 + third_number_result/3600

    def fixed_size(self, width, height):
        """按照固定尺寸处理图片"""
        im = Image.open(self.infile)
        out = im.resize((width, height),Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_width(self, w_divide_h):
        """按照宽度进行所需比例缩放"""
        im = Image.open(self.infile)
        (x, y) = im.size
        x_s = x
        y_s = x/w_divide_h
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_height(self, w_divide_h):
        """按照高度进行所需比例缩放"""
        im = Image.open(self.infile)
        (x, y) = im.size
        x_s = y*w_divide_h
        y_s = y
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(self.outfile)

    def resize_by_size(self, size):
        """按照生成图片文件大小进行处理(单位KB)"""
        size *= 1024
        im = Image.open(self.infile)
        size_tmp = os.path.getsize(self.infile)
        q = 100
        while size_tmp > size and q > 0:
            print q
            out = im.resize(im.size, Image.ANTIALIAS)
            out.save(self.outfile, quality=q)
            size_tmp = os.path.getsize(self.outfile)
            q -= 5
        if q == 100:
            shutil.copy(self.infile, self.outfile)

    def cut_by_ratio(self, width, height):
        """按照图片长宽比进行分割"""
        im = Image.open(self.infile)
        width = float(width)
        height = float(height)
        (x, y) = im.size
        if width > height:
            region = (0, int((y-(y * (height / width)))/2), x, int((y+(y * (height / width)))/2))
        elif width < height:
            region = (int((x-(x * (width / height)))/2), 0, int((x+(x * (width / height)))/2), y)
        else:
            region = (0, 0, x, y)

        #裁切图片
        crop_img = im.crop(region)
        #保存裁切后的图片
        crop_img.save(self.outfile)

    def to_deg(self,value, loc):
        """convert decimal coordinates into degrees, munutes and seconds tuple

        Keyword arguments: value is float gps-value, loc is direction list ["S", "N"] or ["W", "E"]
        return: tuple like (25, 13, 48.343 ,'N')
        """
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)


    def set_gps_location(self,file_name, lat, lng):
        """Adds GPS position as EXIF metadata
        Keyword arguments:
        file_name -- image file
        lat -- latitude (as float)
        lng -- longitude (as float)

        """
        lat_deg = self.to_deg(lat, ["S", "N"])
        lng_deg = self.to_deg(lng, ["W", "E"])

        print lat_deg
        print lng_deg

        # class pyexiv2.utils.Rational(numerator, denominator) => convert decimal coordinates into degrees, munutes and seconds
        exiv_lat = (ev.Rational(lat_deg[0]*60+lat_deg[1],60),ev.Rational(lat_deg[2]*100,6000), ev.Rational(0, 1))
        exiv_lng = (ev.Rational(lng_deg[0]*60+lng_deg[1],60),ev.Rational(lng_deg[2]*100,6000), ev.Rational(0, 1))

        exiv_image = ev.ImageMetadata(file_name)
        exiv_image.read()

        # modify GPSInfo of image
        exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
        exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
        exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
        exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
        exiv_image["Exif.Image.GPSTag"] = 654
        exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
        exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 2 0 0'
        exiv_image.write()



    def create_validate_code(self,size=(120, 30),
                         chars="TEST",
                         img_type="GIF",
                         mode="RGB",
                         bg_color=(255, 255, 255),
                         fg_color=(0, 0, 255),
                         font_size=18,
                         font_type="C:\Windows\Fonts\mingliu.ttc",
                         length=4,
                         draw_lines=True,
                         n_line=(1, 2),
                         draw_points=True,
                         point_chance = 2):
        '''
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 30)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        '''

        _letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
        _upper_cases = _letter_cases.upper() # 大写字母
        _numbers = ''.join(map(str, range(3, 10))) # 数字
        init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

        width, height = size # 宽， 高
        img = Image.new(mode, size, bg_color) # 创建图形
        draw = ImageDraw.Draw(img) # 创建画笔

        def get_chars():
            '''生成给定长度的字符串，返回列表格式'''
            return random.sample(chars, length)

        def create_lines():
            '''绘制干扰线'''
            line_num = random.randint(*n_line) # 干扰线条数

            for i in range(line_num):
                # 起始点
                begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                #结束点
                end = (random.randint(0, size[0]), random.randint(0, size[1]))
                draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
            '''绘制干扰点'''
            chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]

            for w in xrange(width):
                for h in xrange(height):
                    tmp = random.randint(0, 100)
                    if tmp > 100 - chance:
                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
            '''绘制验证码字符'''
            c_chars = get_chars()
            strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开

            font = ImageFont.truetype(font_type, font_size)
            font_width, font_height = font.getsize(strs)

            draw.text(((width - font_width) / 3, (height - font_height) / 3),
                        strs, font=font, fill=fg_color)

            return ''.join(c_chars)

        if draw_lines:
            create_lines()
        if draw_points:
            create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

        return img#, strs


if __name__ == '__main__':
    text=u"您好"
    outf=r"d:\temp\test2.jpg"
    im=ImageHelper()
    #生成文字图片
    #im.GenImageByText(text,(300,50),outf)
    #获得图片信息，1 简单，2 详细，3 GPS
    im.GetImageInfo(outf,1)
    #im.cut_by_ratio(400,100)
    #把文字放图片上
    #im.PutTextOnImage(text)
    #生成验证码
    code_img = im.create_validate_code()
    code_img.save(r"d:\temp\validate2.gif", "GIF")
    #修改GPS信息
    im.set_gps_location(r"d:\temp\test2.jpg",22,113)
