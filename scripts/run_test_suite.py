import sys
import os
import json
import yaml
import logging
import logger
import time
import traceback
import cfg
import threading
import importlib
import queue as Queue
from multiprocessing import Pool
from multiprocessing import Manager


#import ConfigParser
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

# tc result pattern definition
tc_init_pattern = " - Waiting"
tc_pass_pattern = " - Pass"
tc_pwd_pattern = " - Pass with Defect"
tc_fail_pattern = " - Fail"
tc_error_pattern = " - Error"
tc_timeout_pattern = " - TimeOut"
tc_cnr_pattern = " - CNR"
tc_unknown_pattern = " - Unkown Error"

# global variable default value
tc_timeout = "30"

# set yamlloadwarning to false
yaml.warnings({'YAMLLoadWarning': False})


def main():
    # Input Parameter Validation
    SCRIPT_NAME = os.path.basename(sys.argv[0])
    if len(sys.argv) != 3:
        print("Usage: " + SCRIPT_NAME + " test.conf" + "suite.conf")
        print("test.conf is the test/env configuration file")
        print("suite.conf is the test suite definition file")
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " doesn't exist")
        sys.exit(1)
    if not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + " doesn't exist")
        sys.exit(1)
    
    load_conf_files()
    load_shitv1_conf_files()
    test_conf_manager()
    suite_conf_manager()
    suite_result_initil()

    if ("execution_mode" not in cfg.test_conf) or (cfg.test_conf["execution_mode"] != "concurrent"):
        run_suite_sequential()
    else:
        run_suite_concurrent_v2()

    print("suite_result is:")
    print(json.dumps(cfg.suite_result._getvalue(), indent=2))
    # with open(cfg.test_conf["RES_DIR"] + "/execution_res.json", "w") as text_file:
    #   print(json.dumps(cfg.suite_result._getvalue(), indent=2), file=text_file)
    with open(cfg.test_conf["RES_DIR"] + "/execution_res.js", "w") as text_file:
        print("var data=" + json.dumps(cfg.suite_result._getvalue(), indent=2), file=text_file)

    # gen report html
    HOME_DIR = cfg.test_conf["HOME_DIR"]
    # print("gen report: "+HOME_DIR + "/scripts/to_html.py "+cfg.test_conf["RES_DIR"]+" "+cfg.test_conf["RES_FILE"])
    # os.system("chmod a+x " + HOME_DIR + "/scripts/to_html.py")
    # if (os.system(HOME_DIR + "/scripts/to_html.py "+cfg.test_conf["RES_DIR"]+" "+cfg.test_conf["RES_FILE"]) != 0):
    #   print ("report html cannot be created successfully!")
    #   sys.exit(1)
    os.system("cp " + HOME_DIR + "/scripts/report_template.html " + cfg.test_conf["RES_DIR"] + "/report.html")

def load_shitv1_conf_files():
    
    # get Environment vars WORKSPACE
    SHITv1_WORKSPACE = os.getenv('WORKSPACE')
    # shitv1 conf definition
    if not SHITv1_WORKSPACE:
        SHITv1_DIR = "/home/SHITv1test"
    else:
        SHITv1_DIR = SHITv1_WORKSPACE
    ANSIBLE_DIR = SHITv1_DIR + "/ansible"
    CDM_PATH = ANSIBLE_DIR + "/ansible-cdm"
    VARS_FILE = CDM_PATH + "/vars.yml"
    HOST_FILE = CDM_PATH + "/hosts"
    
    #load ansible hosts files 
    dl = DataLoader()
    im = InventoryManager(loader=dl, sources=HOST_FILE)
    server_group = im.get_groups_dict().get("server")
    client_group = im.get_groups_dict().get("client")
    
    
    #load ansible vars files
    with open(VARS_FILE, 'r') as f:
        cfg.test_conf.update(yaml.load(f))

    cfg.test_conf["cdm_server"] = server_group
    cfg.test_conf["cdm_client"] = client_group


def load_conf_files():
    # Read test.conf and suite.conf
    with open(sys.argv[1], 'r') as f:
        cfg.test_conf = yaml.load(f)
    # print test_conf for user review
    # print ("original test conf is: ")
    # print (cfg.test_conf)
    with open(sys.argv[2], 'r') as f:
        cfg.suite_conf = yaml.load(f)

    # print ("original suite conf is: ")
    # print (cfg.suite_conf)


def test_conf_manager():
    # system conf definition
    ts = str(int(time.time()))
    HOME_DIR = os.path.abspath(sys.path[0]) + "/.."
    DATA_DIR = HOME_DIR + "/data"
    RES_DIR = HOME_DIR + "/results/" + ts
    TMP_DIR = HOME_DIR + "/runtime/" + ts
    CONF_DIR = HOME_DIR + "/conf"
    SUITE_DIR = HOME_DIR + "/suite"
    RES_FILE = RES_DIR + "/execution.res"
    AB_CONF_FILE = CONF_DIR + "/ut/ut_test_AB.yml"
    HW_CONF_FILE = CONF_DIR + "/ut/ut_test_HW.yml"
    
    
    if cfg.test_conf["cdm_branch"] == "AB":
        with open(AB_CONF_FILE, 'r') as f:
            cfg.test_conf.update(yaml.load(f))
    elif cfg.test_conf["cdm_branch"] == "HW":
        with open(HW_CONF_FILE, 'r') as f:
            cfg.test_conf.update(yaml.load(f))
    
    # compose url to test conf
    cfg.test_conf["url"] = "https://" + cfg.test_conf["cdm_cluster_ip"] + ":" + cfg.test_conf["port"] 
 
    # Add system conf to test conf
    cfg.test_conf["HOME_DIR"] = HOME_DIR
    cfg.test_conf["DATA_DIR"] = DATA_DIR
    cfg.test_conf["RES_DIR"] = RES_DIR
    cfg.test_conf["TMP_DIR"] = TMP_DIR
    cfg.test_conf["CONF_DIR"] = CONF_DIR
    cfg.test_conf["SUITE_DIR"] = SUITE_DIR
    cfg.test_conf["RES_FILE"] = RES_FILE
    if ("timeout" not in cfg.test_conf) or cfg.test_conf["timeout"] == "":
        cfg.test_conf["timeout"] = tc_timeout
    if ("exec_uid" not in cfg.test_conf) or cfg.test_conf["exec_uid"] == "":
        cfg.test_conf["exec_uid"] = "auto" + ts[-4:]

    # print test_conf for user review
    print("test_conf is: ")
    print(yaml.dump(cfg.test_conf, ))
    #print(json.dumps(cfg.test_conf, indent=2))


def suite_conf_manager():
    # add tc name if not provided
    for suite in cfg.suite_conf["testsuite"]:
        testcases = suite["testcases"]
        for testcase in testcases:
            module = testcase["script"]
            func = testcase["testcase"]
            if ("tc_name" not in testcase) or testcase["tc_name"] == "":
                testcase["tc_name"] = module + r'.' + func
            if ("timeout" not in testcase) or testcase["timeout"] == "":
                testcase["timeout"] = cfg.test_conf["timeout"]
            if "dependency" not in testcase:
                testcase["dependency"] = ""
            if "tc_parameter" not in testcase:
                testcase["tc_parameter"] = ""
    # print suite_conf for user review
    print("suite_conf is:")
    print(yaml.dump(cfg.suite_conf, ))
    #print(json.dumps(cfg.suite_conf, indent=2))


def suite_result_initil():
    if not os.path.exists(cfg.test_conf["RES_DIR"]):
        os.mkdir(cfg.test_conf["RES_DIR"])
    open(cfg.test_conf["RES_FILE"], "a").close()

    # dump test conf to file
    with open(cfg.test_conf["RES_DIR"] + "/env.json", 'a') as f:
        f.write(json.dumps(cfg.test_conf, indent=2))

    if not os.path.exists(cfg.test_conf["TMP_DIR"]):
        os.mkdir(cfg.test_conf["TMP_DIR"])

    cfg.tc_res = logger.get_logger("EXEC_RES", cfg.test_conf["RES_FILE"], logging.Formatter(''))

    for suite in cfg.suite_conf["testsuite"]:
        testcases = suite["testcases"]
        for testcase in testcases:
            string = testcase["tc_name"] + tc_init_pattern
            print("TC:" + string)
            cfg.tc_res.info(string)

    cfg.suite_result = Manager().dict(cfg.suite_conf)


def replace_string_in_file(file_path, old_str, new_str):
    try:
        f = open(file_path, 'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            line = line.replace(old_str, new_str)
            f.write(line)
        f.close()
    except Exception as e:
        print(e)


def update_tc_result(tc_name, result):
    tc = ""
    suite_result = cfg.suite_result._getvalue()
    for suite in suite_result["testsuite"]:
        if tc != "":
            break
        testcases = suite["testcases"]
        for testcase in testcases:
            if testcase["tc_name"] == tc_name:
                tc = testcase
                break
    if result == True or result == "Pass":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_pass_pattern)
        testcase["result"] = "Pass"
    elif result == "Pass with Defect":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_pwd_pattern)
        testcase["result"] = "Pass with Defect"
    elif result == False or result == "Fail":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_fail_pattern)
        testcase["result"] = "Fail"
    elif result == "Error":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_error_pattern)
        testcase["result"] = "Error"
    elif result == "TimeOut":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_timeout_pattern)
        testcase["result"] = "TimeOut"
    elif result == "CNR":
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern, tc_name + tc_cnr_pattern)
        testcase["result"] = "CNR"
    else:
        replace_string_in_file(cfg.test_conf["RES_FILE"], tc_name + tc_init_pattern,
                               tc_name + tc_unknown_pattern + "(" + result + ")")
        testcase["result"] = "Unkown Error" + "(" + result + ")"

    cfg.suite_result.update(suite_result)


def run_suite_sequential():
    if not os.path.exists(cfg.test_conf["RES_DIR"]):
        os.mkdir(cfg.test_conf["RES_DIR"])
    open(cfg.test_conf["RES_FILE"], "a").close()

    for testcase in cfg.suite_conf["testsuite"]:
        cfg.test_conf["TC_RES_DIR"] = cfg.test_conf["RES_DIR"] + "/" + testcase["tc_name"]
        cfg.test_conf["TC_LOG_FILE"] = cfg.test_conf["TC_RES_DIR"] + "/execution.txt"

        tc_name = testcase["tc_name"]
        module = testcase["script"]
        func = testcase["testcase"]

        print("running test case: " + tc_name)
        print("script: " + module)
        print("function: " + func)
        # print("TC_RES_DIR:"+cfg.test_conf["TC_RES_DIR"])
        # print("TC_LOG_FILE:"+cfg.test_conf["TC_LOG_FILE"])
        if not os.path.exists(cfg.test_conf["TC_RES_DIR"]):
            os.mkdir(cfg.test_conf["TC_RES_DIR"])
        open(cfg.test_conf["TC_LOG_FILE"], "a").close()
        try:
            obj = __import__(module)
        except Exception as e:
            traceback.print_exc()
            sys.exit("import module error: " + module)

        if hasattr(obj, func):
            function = getattr(obj, func)
        else:
            print("Function doesn't exist: " + func)
            sys.exit(1)

        function()
        print("test case is completed: " + tc_name)


def run_one_tc(testcase):
    cfg.test_conf["TC_RES_DIR"] = cfg.test_conf["RES_DIR"] + "/" + testcase["tc_name"]
    cfg.test_conf["TC_LOG_FILE"] = cfg.test_conf["TC_RES_DIR"] + "/execution.txt"

    tc_name = testcase["tc_name"]
    module = testcase["script"]
    func = testcase["testcase"]
    timeout = int(testcase["timeout"])
    dependency = testcase["dependency"]
    tc_parameter = testcase["tc_parameter"]

    print("======== initializing test case: " + tc_name + " =========")
    if dependency == "":
        print(tc_name + " has no dependency")
    else:
        print(tc_name + " has dependency: " + dependency)
        dependency_list = dependency.split(',')
        for d in dependency_list:
            cmd = "cat " + cfg.test_conf["RES_FILE"] + " | grep '" + d + " - Pass'"
            if os.system(cmd) != 0:
                print("dependency tc not pass: " + d)
                result = "CNR"
                update_tc_result(tc_name, result)
                return
        print("all dependency tc pass, start to execute")

    print("script: " + module)
    print("function: " + func)
    # print("TC_RES_DIR:"+cfg.test_conf["TC_RES_DIR"])
    # print("TC_LOG_FILE:"+cfg.test_conf["TC_LOG_FILE"])

    if not os.path.exists(cfg.test_conf["TC_RES_DIR"]):
        os.mkdir(cfg.test_conf["TC_RES_DIR"])
    open(cfg.test_conf["TC_LOG_FILE"], "a").close()

    cfg.tc_log = logger.get_logger("EXEC_LOG", cfg.test_conf["TC_LOG_FILE"],
                                   logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    try:
        obj = importlib.import_module(module)
    except Exception as e:
        traceback.print_exc()
        update_tc_result(tc_name, "Module Import Error")
        return "Module Import Error"
    if hasattr(obj, func):
        function = getattr(obj, func)
    else:
        print("Function doesn't exist: " + func)
        update_tc_result(tc_name, "Function Import Error")
        return "Function Import Error"

    que = Queue.Queue()
    if tc_parameter == "":
        thread = threading.Thread(target=lambda q: q.put(function()), args=(que,))
    else:
        tc_parameter = tc_parameter.split(",")
        thread = threading.Thread(target=lambda q: q.put(function(*tc_parameter)), args=(que,))
    thread.setDaemon(True)
    thread.start()
    #thread.run()
    try:
        result = que.get(timeout=timeout)
    except Queue.Empty:
        result = "TimeOut"
    update_tc_result(tc_name, result)


def run_suite_concurrent_v2():
    if not os.path.exists(cfg.test_conf["RES_DIR"]):
        os.mkdir(cfg.test_conf["RES_DIR"])
    open(cfg.test_conf["RES_FILE"], "a").close()
    # print(cfg.test_conf["RES_FILE"]+" created")

    pool = Pool(int(cfg.test_conf["concurrent_max_p"]))

    for suite in cfg.suite_conf["testsuite"]:
        testcases = suite["testcases"]
        for testcase in testcases:
            pool.apply_async(func=run_one_tc, args=(testcase,))
            #run_one_tc(testcase)

    pool.close()
    pool.join()
    pool.terminate()


def dummy_callback(arg):
    print("I am callback: " + str(arg))


if __name__ == "__main__":
    main()
