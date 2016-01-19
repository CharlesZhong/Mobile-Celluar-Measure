__author__ = 'Charles'
import os
settings = {
    "mac_test": {
        "data_dir": "/Users/Charles/Data/NSDI2015",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/Users/Charles/Data/NSDI2015/output/mac_test",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },
    "mac_prod":{
        "data_dir": "/Users/Charles/Data/NSDI2015",
        "ori_input_file": "1211.txt",
        "output_dir": "/Users/Charles/Data/NSDI2015/output/mac_prod",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },
    "linux_test": {
        "data_dir": "/media/sf_baidu_data",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/media/sf_baidu_data/linux_test",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",

    },
    "linux_prod":{
        "data_dir": "/media/sf_baidu_data",
        "ori_input_file": "1211.txt",
        "output_dir": "/media/sf_baidu_data/linux_prod",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },
    "thtf_test":{
        "data_dir": "/home/charles/Data/NSDI2015",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/home/charles/Data/NSDI2015/result/test",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },
    "thtf_prod":{
        "data_dir": "/home/charles/Data/NSDI2015",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/home/charles/Data/NSDI2015/result/prod",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },


    "s3_test":{
        "data_dir": "/home/zhongxin/workspace/nsdi_2015/data",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/home/zhongxin/workspace/nsdi_2015/data/result/test",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },
    "s3_prod":{
        "data_dir": "/home/zhongxin/workspace/nsdi_2015/data",
        "ori_input_file": "test_ori.txt",
        "output_dir": "/home/zhongxin/workspace/nsdi_2015/data/result/prod",
        "base_output_file": "ori_output.txt",
        "image_output_file": "image_output.txt",
        "ori_image_output_file": "ori_image_output.txt",
        "filter_image_output_file": "filter_image_output_file.txt",
    },


}