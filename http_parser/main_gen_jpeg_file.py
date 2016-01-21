# -*- coding: utf-8 -*-
__author__ = 'Xin Zhong'

"""
    Make Jpeg file from filterd file.
"""

import sys
import os
import logging
import argparse
from datetime import datetime
from collections import defaultdict

from common_tools import parent_parser
from parser import Request_Parser, Response_Parser
from config import settings
from image import image_type_detection, get_image_info
from model import Image_Model

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
date_tag = datetime.now().strftime("%Y-%m-%d")
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.FileHandler("../logs/Main_gen_jpeg_file_%s.log" % date_tag)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

def write_jpeg(filename, body):
    with open(filename, 'w') as w:
        w.write(body)







def main():
    parser = argparse.ArgumentParser(parents=[parent_parser])
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    options = parser.parse_args()

    config = settings[options.config]
    logging.info("Setting {}".format(options.config))


    ori_input_file = os.path.join(config['data_dir'], config['ori_input_file'])

    store_jpeg_dir = config['jpeg_dir']



    if not os.path.isfile(ori_input_file):
        logging.error("input file: %s is not exist!", ori_input_file)
        sys.exit(-1)

    if not os.path.isdir(store_jpeg_dir):
        logging.error("jpeg base dir: %s is not exist", store_jpeg_dir)
        sys.exit(-1)


    overall_statistic = defaultdict(int)
    real_image_type_statistic = defaultdict(int)

    REQUEST_HEADER_KEYS = ['X-QB', 'Accept', 'Accept-Encoding', ]
    RESPONSE_HEADER_KEYS = ['Content-Length', 'Content-Type', ]

    DIR_LENGTH = 100
    FILE_LENGTH = 10000

    dir_i, file_i = 0,0
    pwd = ""
    with open(ori_input_file) as r_handler: \

        for line in r_handler:
            try:
                if line and line.strip():
                    line = line.strip()
                    overall_statistic['all'] += 1

                    # file format : req_time|rep_time|key|base64(req)|base64(rep)
                    terms = line.split('\t')

                    # response
                    http_response_parser = Response_Parser()
                    http_response_parser.parse(terms[4].decode('base64'))


                    # reponse_body
                    reponse_body = http_response_parser.get_body()
                    real_image_type = image_type_detection(reponse_body)
                    real_image_type_statistic[real_image_type] += 1

                    if real_image_type and real_image_type  == 'jpeg':
                        if file_i == 0:
                            pwd = os.path.join(store_jpeg_dir,str(dir_i))
                            os.mkdir(pwd)
                            logger.info("create dir :%d", dir_i)

                        write_jpeg(os.path.join(pwd,"%03d.jpeg" %file_i), reponse_body)
                        file_i += 1
                        if file_i == FILE_LENGTH:
                            file_i = 0
                            dir_i += 1


            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error:{0} ".format(e))
    logging.info("[Stat] overall_statistic: {}".format(overall_statistic))
    logging.info("[Stat] image_type_statistic: {}, total:{}".format(real_image_type_statistic,
                                                                    sum(real_image_type_statistic.values())))


if __name__ == "__main__": main()
