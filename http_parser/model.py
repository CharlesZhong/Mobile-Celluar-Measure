__author__ = 'Charles'

from httplib import HTTPResponse


class HTTP_Requset(object):
    def __init__(self, header_keys, len_request, len_request_body):
        self.user_token, self.user_conf = self.parse_X_QB(header_keys['X-QB'])
        self.accept = header_keys['Accept'] if header_keys['Accept'] else '-'
        self.accept_encoding = header_keys['Accept-Encoding'] if header_keys['Accept-Encoding'] else '-'
        self.len_request = len_request
        self.len_request_body = len_request_body

    def parse_X_QB(self, X_QB):
        user_token, user_conf = '-', '-'
        if X_QB:
            terms = X_QB.split('^')
            if len(terms) == 4:
                user_token = terms[0].strip() if terms[0]  else '-'
                user_conf = terms[2].strip() if terms[2] else '-'
        return user_token, user_conf

    def __repr__(self):
        return "{}\t{}\t{}\t{}\t{}".format(self.user_token,
                                           self.accept, self.accept_encoding,
                                           self.len_request, self.len_request_body)


class HTTP_Response(object):
    def __init__(self, status_code, header_keys, len_repsonse, len_response_body):
        self.status_code = status_code

        self.content_length = header_keys['Content-Length'] if header_keys['Content-Length'] else '-'
        self.content_type = header_keys['Content-Type'] if header_keys['Content-Type'] else '-'

        self.len_repsonse = len_repsonse
        self.len_response_body = len_response_body

    def __repr__(self):
        return "{}\t{}\t{}\t{}\t{}".format(self.status_code,
                                           self.content_length, self.content_type,
                                           self.len_repsonse, self.len_response_body)


class Image_Model(object):
    def __init__(self, real_type, md5, weight, height, pixel_count, ):
        self.real_type = real_type
        self.md5 = md5
        self.weight = weight
        self.height = height
        self.pixel_count = pixel_count
        self.quality = '-'
        self.compress_md5 = '-'
        self.compress_size = '-'

    def set_zip(self, compress_md5, compress_size):
        self.compress_md5 = compress_md5
        self.compress_size = compress_size

    def __repr__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.real_type, self.md5,
                                                       self.weight, self.height, self.pixel_count,
                                                       self.quality,
                                                       self.compress_md5, self.compress_size)


class IMAGE_OUTPUT_MODEL():
    def __init__(self, terms):
        self.requset_time = terms[0]
        self.response_time = terms[1]
        self.user_token = terms[2]
        # self.user_conf = terms[3]
        self.accept = terms[3]
        self.accept_encoding = terms[4]
        self.len_request = terms[5]
        self.len_request_body = terms[6]

        self.status_code = terms[7]
        self.content_length = terms[8]
        self.content_type = terms[9]
        self.len_repsonse = terms[10]
        self.len_response_body = terms[11]

        self.real_type = terms[12]
        self.md5 = terms[13]
        self.weight = terms[14]
        self.height = terms[15]
        self.pixel_count = terms[16]
        self.quality = terms[17]

        self.compress_md5 = terms[18]
        self.compress_size = terms[19]

        self.cwebp_runtime = terms[20]
        self.dwebp_runtime = terms[21]
        self.ziproxy_runtime = terms[22]