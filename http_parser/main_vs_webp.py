# -*- coding: utf-8 -*-
__author__ = 'Xin Zhong'

"""
compress image by webp type.
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
from image import image_type_detection, compress_image_by_webp75, get_image_info
from model import Image_Model

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
date_tag = datetime.now().strftime("%Y-%m-%d")
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.FileHandler("../logs/Main_webp%s.log" % date_tag)
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

    LEN_ORI_INPUT_TERMS = 5
    REQUEST_HEADER_KEYS = ['X-QB', 'Accept', 'Accept-Encoding', ]
    RESPONSE_HEADER_KEYS = ['Content-Length', 'Content-Type', ]


    filter_image_output_file = os.path.join(config['data_dir'], config['filter_image_output_file'])

    image_output_file = os.path.join(config['output_dir'],
                                     datetime.now().strftime("%Y%m%d%H%M%S") + "_webp_" + config['image_output_file'])



    if not os.path.isfile(filter_image_output_file):
        logging.error("filter input file: %s is not exist!", filter_image_output_file)
        sys.exit(-1)

    overall_statistic = defaultdict(int)
    real_image_type_statistic = defaultdict(int)

    request_head_keys = set()
    response_head_key = set()

    with open(filter_image_output_file) as r_handler, \
        open(image_output_file, 'w') as w_handler:

        for line in r_handler:
            try:
                if line and line.strip():
                    line = line.strip()
                    overall_statistic['all'] += 1

                    # file format : req_time|rep_time|key|base64(req)|base64(rep)
                    terms = line.split('\t')

                    if len(terms) != LEN_ORI_INPUT_TERMS:
                        overall_statistic['format_wrong']
                        continue

                    # time
                    req_time = datetime.fromtimestamp(float(terms[0])).second * 10 ** 6 + datetime.fromtimestamp(
                        float(terms[0])).microsecond
                    rep_time = datetime.fromtimestamp(float(terms[1])).second * 10 ** 6 + datetime.fromtimestamp(
                        float(terms[1])).microsecond

                    # request
                    http_request_parser = Request_Parser()
                    http_request_parser.parse(terms[3].decode('base64'))
                    http_request_model = http_request_parser.get_request(*REQUEST_HEADER_KEYS)

                    # response
                    http_response_parser = Response_Parser()
                    http_response_parser.parse(terms[4].decode('base64'))
                    http_response_model = http_response_parser.get_reponse(*RESPONSE_HEADER_KEYS)

                    # base writer
                    base_str = "{}\t{}\t{}\t{}".format(req_time, rep_time, http_request_model, http_response_model)
                    # w_base_handler.write("{}\n".format(base_str))

                    # reponse_body
                    reponse_body = http_response_parser.get_body()
                    real_image_type = image_type_detection(reponse_body)
                    real_image_type_statistic[real_image_type] += 1

                    # image


                    md5_code, width, height, image_pix_count = get_image_info(real_image_type, reponse_body)
                    image_model = Image_Model(real_image_type, md5_code, width, height, image_pix_count)


                    compress_md5_75, compress_size_75, cwebp_run_time_75,dwebp_run_time = compress_image_by_webp75(reponse_body)

                    w_handler.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(base_str, image_model,compress_md5_75, compress_size_75, cwebp_run_time_75,dwebp_run_time))





            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error:{0} ".format(e))
    logging.info("[Stat] overall_statistic: {}".format(overall_statistic))
    logging.info("[Stat] image_type_statistic: {}, total:{}".format(real_image_type_statistic,
                                                                    sum(real_image_type_statistic.values())))


if __name__ == "__main__": main()
