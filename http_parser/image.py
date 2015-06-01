__author__ = 'Charles'
from StringIO import StringIO
from imghdr import what
from hashlib import md5
import os
import subprocess
import logging

from PIL import Image

from webm import handlers
from webm import decode
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


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


def compress_image_by_webp(body, quality=70):
    """ Compress image and return runtime
    """
    try:
        with open("cal_image", 'w') as w:
            w.write(body)
        FNULL = open(os.devnull, 'w')
        start = time.clock()
        subprocess.call(["cwebp", "-q", str(quality), "cal_image", "-o", "zip_image.webp"], stdout=FNULL,
                        stderr=subprocess.STDOUT)
        end = time.clock()
        zip_size = os.stat("zip_image.webp").st_size
        md5_code = md5(open("zip_image.webp").read()).hexdigest()

        run_time = end - start
    except Exception as e:
        logging.info("error {} ".format(e))
        zip_size = '-1'
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
