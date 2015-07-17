#!/bin/python
#encoding:utf-8
__author__ = 'Charles'
import argparse

"""
Config Config
"""
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('-s', '--setting', action='store', dest='config',
                           default="test", required=True, help="设置环境: test,sandbox, prod. 默认:test.")


parent_parser.add_argument('--filter_image', action='store_true', dest='is_filter_image', default=False,
                           help='is_filter_image')

parent_parser.add_argument('--filter_non_image', action='store_true', dest='is_filter_non_image', default=False,
                           help='is_filter_non_image')
