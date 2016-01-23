# -*- coding: utf-8 -*-
__author__ = 'Xin Zhong'

"""
 cal time from file
"""

import sys
import os
import logging
import argparse
import time
from datetime import datetime
from collections import defaultdict

from common_tools import parent_parser
from config import settings
from image import  compress_jpeg_file_by_webp75, compress_jpeg_file_by_ziporxy,compress_local_jpeg_file_by_ziporxy,compress_local_jpeg_file_by_webp75

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
date_tag = datetime.now().strftime("%Y-%m-%d")
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.FileHandler("../logs/Main_precise_time_%s.log" % date_tag)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def main():
    parser = argparse.ArgumentParser(parents=[parent_parser])
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    options = parser.parse_args()

    config = settings[options.config]
    logging.info("Setting {}".format(options.config))

    jpeg_dir = config['jpeg_dir']


    if not os.path.isdir(jpeg_dir):
        logging.error("jpeg_dir : %s is not exist!", jpeg_dir)
        sys.exit(-1)
    """
    zip_time_output_file = os.path.join(config['output_dir'], datetime.now().strftime("%Y%m%d%H%M%S") + "_" + config['zip_time_output_file'])

    zip_statistic = defaultdict(int)
    with open(zip_time_output_file, 'w') as zip_handler:
        for root, dirs, files in os.walk(jpeg_dir):
            for file in files:
                zip_statistic['total'] += 1
                jpeg_file = os.path.join(root, file)
                try:
                    zip_time = compress_jpeg_file_by_ziporxy(jpeg_file)
                    mv_time, local_zip_time = compress_local_jpeg_file_by_ziporxy(jpeg_file)

                    zip_handler.write("{}\t{}\t{}\n".format(zip_time,mv_time, local_zip_time))
                except:
                    zip_statistic['error'] += 1

    logging.info("[Stat] zip_statistic: {}".format(zip_statistic))

    if options.config == "thtf_test":
        time.sleep(20)
    else:
        time.sleep(600)
    """
    webp_time_output_file = os.path.join(config['output_dir'], datetime.now().strftime("%Y%m%d%H%M%S") +  "_" + config['webp_time_output_file'])

    webp_statistic = defaultdict(int)
    with open(webp_time_output_file, 'w') as webp_handler:
        for root, dirs, files in os.walk(jpeg_dir):
            for file in files:
                webp_statistic['total'] += 1
                jpeg_file = os.path.join(root, file)
                try:
                    cwebp_time , dwebp_time = compress_jpeg_file_by_webp75(jpeg_file)

                    mv_time, local_cwebp_time, local_dwebp_time = compress_local_jpeg_file_by_webp75(jpeg_file)

                    webp_handler.write("{}\t{}\t{}\t{}\t{}\n".format(cwebp_time,dwebp_time,mv_time, local_cwebp_time, local_dwebp_time))
                except:
                    webp_statistic['error'] += 1

    logging.info("[Stat] webp_statistic: {}".format(webp_statistic))




if __name__ == "__main__": main()
