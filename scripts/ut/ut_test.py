import sys
import subprocess as commands
import os
import json
import inspect
import time
import logging
import logger
import cfg
import inspect

import requests
import urllib3
from ut.userManage import *
from ut.publicManage import *
from ut.common import comm
url = cfg.test_conf["url"]
admin = cfg.test_conf["admin"]
test_admin = 'admin1'
sadmin = cfg.test_conf["sadmin"]
init_admin_password = cfg.test_conf["init_admin_password"]
admin_password = cfg.test_conf["admin_password"]
cdm_serverip = cfg.test_conf["cdm_server"]
#print(cfg.test_conf)


def tc_cdm_userinit():
  a = login(url=url, name=admin, password=init_admin_password)
  result = a.pass_user(init_admin_password, admin_password)["status"]
  if result == "success":
      comm.log_info("Pass")
      return True
  
  #print(a.get_user('admin', 0))
  #userstatus = a.get_user('admin', 0)["status"]
  #if userstatus == "success":
  #    cfg.tc_log.info("Pass")
  #    return True

def tc_cdm_add_backup_transip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
  #    print(cdm_serverip[i])
      comm.log_info("add backup transferip " + cdm_serverip[i])
      result = a.add_transferip(cdm_serverip[i], cdm_serverip[i], 0)["status"]
      if result != "success":
          comm.log_info("add backup transferip fail " + cdm_serverip[i])
          return False
  comm.log_info("add backup transferip success " )
  comm.log_info("Pass")
  return True


def tc_cdm_add_nautilus_dataip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
  #    print(cdm_serverip[i])
      comm.log_info("add nautilus data ip " + cdm_serverip[i])
      result = a.add_transferip(cdm_serverip[i], cdm_serverip[i], 1)["status"]
      if result != "success":
          comm.log_info("add nautilus data ip fail " + cdm_serverip[i])
          return False
  comm.log_info("add nautilus data ip success " )
  comm.log_info("Pass")
  return True

def tc_cdm_add_nautilus_transip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
  #    print(cdm_serverip[i])
      comm.log_info("add nautilus transferip " + cdm_serverip[i])
      result = a.add_transferip(cdm_serverip[i], cdm_serverip[i], 2)["status"]
      if result != "success":
          comm.log_info("add nautilus transferip fail " + cdm_serverip[i])
          return False
  comm.log_info("add nautilus transferip success ")
  comm.log_info("Pass")
  return True

def tc_cdm_remove_backup_transip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
    comm.log_info("remove backup transferip " + cdm_serverip[i])
    result = a.del_transferip(cdm_serverip[i], cdm_serverip[i], 0)["status"]
    if result != "success":
      comm.log_info("remove backup transferip fail " + cdm_serverip[i])
      return False
  comm.log_info("remove backup transferip success ")
  comm.log_info("Pass")
  return True

def tc_cdm_remove_nautilus_dataip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
    comm.log_info("remove nautilus data ip " + cdm_serverip[i])
    result = a.del_transferip(cdm_serverip[i], cdm_serverip[i], 1)["status"]
    if result != "success":
      comm.log_info("remove nautilus data ip fail " + cdm_serverip[i])
      return False
  comm.log_info("remove nautilus data ip success ")
  comm.log_info("Pass")
  return True

def tc_cdm_remove_nautilus_transip():
  a = publicManage(url=url, name=admin, password=admin_password)
  for i in range(len(cdm_serverip)):
    comm.log_info("remove nautilus transfer ip " + cdm_serverip[i])
    result = a.del_transferip(cdm_serverip[i], cdm_serverip[i], 2)["status"]
    if result != "success":
      comm.log_info("remove nautilus transfer ip fail " + cdm_serverip[i])
      return False
  comm.log_info("remove nautilus transfer ip success ")
  comm.log_info("Pass")
  return True
  

def tc_pass():
  cfg.tc_log.info("Pass")
  return True
  
def tc_pwd():
  cfg.tc_log.info("Pass with Defect")
  return "Pass with Defect"

def tc_fail():
  cfg.tc_log.info("Fail")
  return False

def tc_one_parameter(name):
  print ("Hello " + name)
  return True

def tc_three_parameters(a, b, c):
  print ("Hello " + a + ", " + b + " and " + c)
  return True


#if __name__ == '__main__':
#    tc_cdm_logintest()

    

