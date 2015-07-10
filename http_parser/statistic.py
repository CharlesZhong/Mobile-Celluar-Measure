__author__ = 'Charles'

from collections import defaultdict
from warpper import check_files
from model import IMAGE_OUTPUT_MODEL
from datetime import datetime
import logging
import sys
import image

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
        print "{}\t{}\t{}\t{}\t{}".format(item, real_type_count_statistic[item], ori_size_statistic[item],
                                          compress_size_statistic[item],
                                          float(compress_size_statistic[item]) / ori_size_statistic[item])


@check_files("image_output_file")
def stat_non_webp_runtime(image_output_file):
    overall_statistic = defaultdict(int)

    real_type_count_statistic = defaultdict(int)
    cwebp_runtime_statistic = defaultdict(float)
    dwebp_runtime_statistic = defaultdict(float)
    ziproxy_runtime_statistic = defaultdict(float)

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
                        cwebp_runtime = float(image_model.cwebp_runtime)
                    except ValueError as e:
                        # print e
                        cwebp_runtime = 0.0
                    try:
                        dwebp_runtime = float(image_model.dwebp_runtime)
                    except ValueError as e:
                        # print e
                        dwebp_runtime = 0.0
                    try:
                        ziproxy_runtime = float(image_model.ziproxy_runtime)
                    except ValueError as e:
                        # print e
                        ziproxy_runtime = 0.0
                    real_type_count_statistic[image_model.real_type] += 1
                    cwebp_runtime_statistic[image_model.real_type] += cwebp_runtime
                    dwebp_runtime_statistic[image_model.real_type] += dwebp_runtime
                    ziproxy_runtime_statistic[image_model.real_type] += ziproxy_runtime

            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error {} in line {}".format(e, line))

    logging.info("[STAT] overstat is {}".format(overall_statistic))
    for item in real_type_count_statistic:
        print "{}\t{}\t{}\t{}\t{}".format(item, real_type_count_statistic[item],
                                          cwebp_runtime_statistic[item], dwebp_runtime_statistic[item],
                                          ziproxy_runtime_statistic[item])


@check_files("image_output_file")
def statistic_ssim(image_output_file):
    overall_statistic = defaultdict(int)


    count_statistic = defaultdict(int)
    ssim_statistic = defaultdict(float)
    ori_size_statistic = defaultdict(int)
    ori_pixel_statistic = defaultdict(int)
    compressed_size_statistic = defaultdict(int)

    with open(image_output_file) as r_handler:
        for line in r_handler:
            try:
                if line and line.strip():
                    overall_statistic['all'] += 1
                    line = line.strip()
                    terms = line.split('\t')
                    if len(terms) != 26:
                        overall_statistic['format_wrong'] += 1
                        continue

                    overall_statistic['right'] += 1
                    weight = int(terms[14])
                    height = int(terms[15])

                    ori_size = int(terms[11])

                    high_ssim = float(terms[-6])
                    median_ssim = float(terms[-5])
                    low_ssim = float(terms[-4])
                    high_size = int(terms[-3])
                    median_size = int(terms[-2])
                    low_size = int(terms[-1])

                    pixel_type = image.image_pixel_type_detection(weight, height)
                    real_type = terms[12]

                    count_statistic[pixel_type, real_type] += 1

                    ori_pixel_statistic[pixel_type, real_type] += weight * height
                    ori_size_statistic[pixel_type, real_type] += ori_size
                    compressed_size_statistic[pixel_type, real_type, 'high'] += high_size
                    compressed_size_statistic[pixel_type, real_type, 'median'] += median_size
                    compressed_size_statistic[pixel_type, real_type, 'low'] += low_size

                    ssim_statistic[pixel_type, real_type, 'high'] += high_ssim
                    ssim_statistic[pixel_type, real_type, 'median'] += median_ssim
                    ssim_statistic[pixel_type, real_type, 'low'] += low_ssim




            except Exception as e:
                overall_statistic['error'] += 1
                logging.error("error {} in line {}".format(e, line))

    # logging.info("[STAT] overstat is {}".format(overall_statistic))
    # logging.info("[STAT] ori_pixel_statistic is {}".format(ori_pixel_statistic))
    # logging.info("[STAT] ori_size_statistic is {}".format(ori_size_statistic))
    # logging.info("[STAT] compressed_size_statistic is {}".format(compressed_size_statistic))
    # logging.info("[STAT] ssim_statistic is {}".format(ssim_statistic))

    for pixel_type in ['Tiny', 'Small', 'Middle', 'Large']:
        for real_type in ['jpeg', 'png', 'gif', 'bmp']:
            p, r = pixel_type, real_type
            size = count_statistic[p, r]
            avg_pixel = ori_pixel_statistic[p, r] / size if size > 0 else '-'
            avg_size = ori_size_statistic[p, r] / size if size > 0 else '-'

            avg_ssim_high = ssim_statistic[p, r, 'high'] / size if size > 0 else '-'
            avg_ssim_median = ssim_statistic[p, r, 'median'] / size if size > 0 else '-'
            avg_ssim_low = ssim_statistic[p, r, 'low'] / size if size > 0 else '-'

            avg_compressed_high = compressed_size_statistic[p, r, 'high'] / size if size > 0 else '-'
            avg_compressed_median = compressed_size_statistic[p, r, 'median'] / size if size > 0 else '-'
            avg_compressed_low = compressed_size_statistic[p, r, 'low'] / size if size > 0 else '-'

            print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format((p, r),size,avg_pixel,avg_size,avg_ssim_high,avg_ssim_median,avg_ssim_low,avg_compressed_high,avg_compressed_median,avg_compressed_low)

if __name__ == "__main__":
    pass
    statistic_ssim(image_output_file="/Users/Charles/Data/20150528/output/mac_test/20150703004153_image_output.txt")
    # stat_webp_compress(image_output_file="/Users/Charles/image_output.txt")
