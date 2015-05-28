__author__ = 'Charles'
import sys
import logging
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from pprint import pprint
from http_parser.http import HttpStream
from http_parser.reader import SocketReader
from model import HTTP_Requset, HTTP_Response

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser
reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Request_Parser():
    def __init__(self):
        self.parser = HttpParser()
        self.len_request = 0
        self.len_body = 0

    def parse(self, raw_requset):
        self.len_request = len(bytearray(raw_requset))
        self.parser.execute(raw_requset, self.len_request)
        self.len_body = len(bytearray(self.parser.recv_body()))

    def get_all_keys(self):
        """Get All the key in request headers."""
        return self.parser.get_headers().keys()

    def get_keys(self, *args):
        header_keys = {}
        for key in args:
            header_keys[key] = self.parser.get_headers().get(key, '-')
        return header_keys

    def get_request(self, *args):
        values = self.get_keys(*args)
        obj = HTTP_Requset(values, self.len_request, self.len_body)
        return obj

    def get_body(self):
        return self.parser.recv_body()


class Response_Parser():
    def __init__(self):
        self.parser = HttpParser()
        self.len_response = 0
        self.len_body = 0
        self.body = None
    def parse(self, raw_response):
        self.len_response = len(bytearray(raw_response))
        self.parser.execute(raw_response, self.len_response)
        self.body = self.parser.recv_body()
        self.len_body = len(bytearray(self.body))

    def get_all_keys(self):
        """Get All the key in request headers."""
        return self.parser.get_headers().keys()

    def get_keys(self, *args):
        header_keys = {}
        for key in args:
            header_keys[key] = self.parser.get_headers().get(key, '-')
        return header_keys

    def get_reponse(self, *args):
        values = self.get_keys(*args)
        status_code = self.parser.get_status_code()
        obj = HTTP_Response(status_code, values, self.len_response, self.len_body)
        return obj

    def get_body(self):
        return self.body


