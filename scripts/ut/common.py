# import required module
import sys
import subprocess as commands
import os
import json
import time
import logging
import logger
import cfg


class common:
    def __init__(self):
        print("init...")

    def log_title(self, info):
        cfg.tc_log.info("========" + "Test Case: " + info + "========")
        print("========" + "Test Case: " + info + "========")

    def log_info(self, info):
        cfg.tc_log.info(info)
        print(info)
        
    def log_error(self, info):
        cfg.tc_log.error(info)
        print (info)

comm = common()

if __name__ == '__main__':
    a = common()
    a.log_title('test')
