import os
import sys
import traceback

def auto_wrapper(func):
  def wrapper (*args, **kwargs):
    try:
      result = func(*args, **kwargs)
      return result
    except Exception as e:
      traceback.print_exc()
    return "Error"
  return wrapper

@auto_wrapper
def tc_pass(name):
  print ("I'm pass: " + name)
  return True

@auto_wrapper
def tc_exception(boy, girl):
  print ("I'm exception: " + boy + " and " + girl)
  raise Exception("我死给你看!")


if (__name__ == "__main__"):
  print (tc_pass("Mary"))
  print (tc_exception("Tom", "Jerry"))