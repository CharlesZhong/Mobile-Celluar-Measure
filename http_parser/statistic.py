__author__ = 'Charles'

from collections import defaultdict
from warpper import check_files
from model import IMAGE_OUTPUT_MODEL
from datetime import datetime
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
date_tag = datetime.now().strftime("%Y-%m-%d")
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.FileHandler("../logs/Main%s.log" % date_tag)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


@check_files("image_output_file")
def stat_webp_compress(image_output_file):
    """statistic compress radio use webp"""

    overall_statistic = defaultdict(int)

    real_type_count_statistic = defaultdict(int)
    ori_size_statistic = defaultdict(int)
    compress_size_statistic = defaultdict(int)

    with open(image_output_file) as r_handler:
        for line in r_handler:
            try:
                if line and line.strip():
                    overall_statistic['all'] += 1
                    line = line.strip()
                    terms = line.split('\t')
                    if len(terms) != 23:
                        overall_statistic['format_wrong'] += 1
                        continue

                    overall_statistic['right'] += 1
                    image_model = IMAGE_OUTPUT_MODEL(terms)
                    # print image_model.len_response_body
                    # print image_model.compress_size
                    try:
                        len_response_body = int(image_model.len_response_body)
                    except ValueError as e:
                        # print e
                        len_response_body = 0

                    try:
                        compress_size = int(image_model.compress_size)
                    except ValueError as e:
                        # print e
                        compress_size = 0
                    real_type_count_statistic[image_model.real_type] += 1
                    ori_size_statistic[image_model.real_type] += len_response_body

                    compress_size_statistic[image_model.real_type] += compress_size

            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error {} in line {}".format(e, line))

    logging.info("[STAT] overstat is {}".format(overall_statistic))
    for item in ori_size_statistic:
        print "{}\t{}\t{}\t{}\t{}".format(item,real_type_count_statistic[item], ori_size_statistic[item], compress_size_statistic[item],
                                      float(compress_size_statistic[item]) / ori_size_statistic[item])


@check_files("image_output_file")
def stat_non_webp_runtime(image_output_file):
    overall_statistic = defaultdict(int)

    real_type_count_statistic = defaultdict(int)
    cwebp_runtime_statistic = defaultdict(int)
    dwebp_runtime_statistic = defaultdict(int)
    zipproxy_runtime_statistic = defaultdict(int)

    with open(image_output_file) as r_handler:
        for line in r_handler:
            try:
                if line and line.strip():
                    overall_statistic['all'] += 1
                    line = line.strip()
                    terms = line.split('\t')
                    if len(terms) != 23:
                        overall_statistic['format_wrong'] += 1
                        continue

                    overall_statistic['right'] += 1
                    image_model = IMAGE_OUTPUT_MODEL(terms)

                    try:
                        cwebp_runtime = int(image_model.cwebp_runtime)
                    except ValueError as e:
                        # print e
                        cwebp_runtime = 0
                    try:
                        dwebp_runtime = int(image_model.dwebp_runtime)
                    except ValueError as e:
                        # print e
                        dwebp_runtime = 0
                    try:
                        zipproxy_runtime = int(image_model.zipproxy_runtime)
                    except ValueError as e:
                        # print e
                        zipproxy_runtime = 0
                    real_type_count_statistic[image_model.real_type] += 1
                    cwebp_runtime_statistic[image_model.real_type] += cwebp_runtime
                    dwebp_runtime_statistic[image_model.real_type] += dwebp_runtime
                    zipproxy_runtime_statistic[image_model.real_type] += zipproxy_runtime

            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error {} in line {}".format(e, line))

    logging.info("[STAT] overstat is {}".format(overall_statistic))
    for item in real_type_count_statistic:
        print "{}\t{}\t{}\t{}\t{}".format(item,real_type_count_statistic[item],
                                          cwebp_runtime_statistic[item], dwebp_runtime_statistic[item],
                                            zipproxy_runtime_statistic[item])


if __name__=="__main__":
    stat_webp_compress(image_output_file="/Users/Charles/image_output.txt")