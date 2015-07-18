__author__ = 'Charles'
from StringIO import StringIO
from imghdr import what
from hashlib import md5
import os
from subprocess import *
import logging
import sys
import subprocess
from PIL import Image
from ssim import compute_ssim
from webm import handlers
from webm import decode
import time
import shutil
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def image_pixel_type_detection(width, height):
    if width * height < 5000:
        return 'Tiny'
    elif (5000 <= width * height < 50000) or (width * height >= 5000 and (width <= 150 or height <= 150)):
        return 'Small'
    elif (50000 <= width * height < 250000) and (width >= 150 and height >= 150):
        return 'Middle'
    elif width * height >= 250000 and width >= 150 and height >= 150:
        return 'Large'
    else:
        return 'Unknown'


def image_type_detection(body):
    """Reture Real Type of body
    """
    common_type = 'unknown'

    if not body:
        return '-'
    image_fp = StringIO(body)

    common_type = what(image_fp)
    if common_type:
        return common_type
    else:
        try:
            data = image_fp.read()
            width, height = decode.GetInfo(data)

            ob = handlers.WebPHandler(bytearray(data), width, height)
            if ob.is_valid:
                common_type = 'webp'
        except Exception as e:
            pass
        finally:
            return common_type


def get_image_info(real_image_type, body):
    """ only in webp, gif, png, jpeg, bmp
    """
    image_fp = StringIO(body)

    if real_image_type == 'webp':
        data = image_fp.read()
        width, height = decode.GetInfo(data)
        image_pix_count = int(width) * int(height)
    else:
        image = Image.open(image_fp)
        width, height = image.size
        image_pix_count = width * height

    image_fp.seek(0)
    md5_code = md5(image_fp.read()).hexdigest()
    return md5_code, width, height, image_pix_count


def compress_image_by_webp(body, image_type, quality):
    """ Compress image and return runtime
    """
    try:
        with open("cal_image."+image_type, 'w') as w:
            w.write(body)
        # FNULL = open(os.devnull, 'w')
        start = time.clock()
        subprocess.call("cwebp -q {} cal_image.{} -o zip_image.webp".format(quality,image_type), shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        # print rc.stdout.readline()
        # print rc.stderr.readline()
        end = time.clock()
        zip_size = os.stat("zip_image.webp").st_size
        md5_code = md5(open("zip_image.webp").read()).hexdigest()

        run_time = end - start
    except Exception as e:
        logging.info("error {} type:{}".format(e, image_type))
        zip_size = '-'
        md5_code = '-'
        run_time = '-'
    return md5_code, zip_size, run_time


def convert_webp_to_png():
    """
    convert image by
    """
    try:
        FNULL = open(os.devnull, 'w')
        start = time.clock()
        subprocess.call(["dwebp", "zip_image.webp", "-o", "web2png.png"], stdout=FNULL,
                        stderr=subprocess.STDOUT)
        end = time.clock()
        run_time = end - start
    except Exception as e:
        run_time = '-'
    return run_time


def ziprxoy_zip():
    """
    convert image by ziproxy
    """
    try:
        FNULL = open(os.devnull, 'w')
        start = time.clock()
        subprocess.call("./demo/demo -f cal_image -o ziproxy_image", shell=True, stdout=FNULL,
                        stderr=subprocess.STDOUT)
        end = time.clock()
        run_time = end - start
    except Exception as e:
        run_time = '-'
    return run_time


def cal_ssim(body):
    """ Compress image and return runtime
    """
    high_ssim, median_ssim, low_ssim = '-', '-', '-'
    high_size, median_size, low_size = '-', '-', '-'

    try:
        with open("ssim_ori_image", 'w') as w:
            w.write(body)
        FNULL = open(os.devnull, 'w')
        subprocess.call("./demo_high/demo -f ssim_ori_image -o ssim_high", shell=True,stdout=FNULL,
                        stderr=subprocess.STDOUT)

        subprocess.call("./demo_median/demo -f ssim_ori_image -o ssim_median", shell=True, stdout=FNULL,
                        stderr=subprocess.STDOUT)

        subprocess.call("./demo_low/demo -f ssim_ori_image -o ssim_low", shell=True, stdout=FNULL,
                        stderr=subprocess.STDOUT)

        high_size = os.stat("ssim_high").st_size
        median_size = os.stat("ssim_median").st_size
        low_size = os.stat("ssim_low").st_size

        high_ssim = compute_ssim("ssim_ori_image", "ssim_high")
        median_ssim = compute_ssim("ssim_ori_image", "ssim_median")
        low_ssim = compute_ssim("ssim_ori_image", "ssim_low")

        # if what("ssim_ori_image") == 'png' and high_ssim < 0.1:
        #     shutil.copyfile("ssim_ori_image", "save_ori_image")
        #     shutil.copyfile("ssim_high", "save_high_image")
        #     shutil.copyfile("ssim_median", "save_median_image")
        #     shutil.copyfile("ssim_low", "save_low_image")
        #     print high_ssim, median_ssim, low_ssim
        #     exit()

    except Exception as e:
        logging.info("error {} ".format(e))
    return high_ssim, median_ssim, low_ssim, high_size, median_size, low_size




if __name__ == "__main__":
    print compute_ssim("/Users/Charles/Desktop/4.jpg", "/Users/Charles/Desktop/70.webp")
    print compute_ssim("/Users/Charles/Desktop/4.jpg", "/Users/Charles/Desktop/50.webp")
