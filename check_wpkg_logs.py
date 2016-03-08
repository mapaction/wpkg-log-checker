import os
import os.path
import re


def get_log_files(logs_dir, recursive=False):
    for root, dirs, files in os.walk(logs_dir):
        if not recursive:
            while len(dirs) > 0:
                dirs.pop()

        # only include relevant files
        include_files = r'wpkg.*log$' # for files only
        files[:] = [os.path.join(root, f) for f in files]
        files[:] = [f for f in files if re.search(include_files, f)]

        return files

def get_file_contents(l_file):
    f = open(l_file)
    txt = f.read()
    f.close()
    return txt

def check_wpkg_stable_branch(log_text):
    return re.search(r"sysadmin/stable/installers/wpkg/hosts.xml", log_text, re.IGNORECASE) is not None

def get_wpkg_errors(log_text):
    return re.findall(r"20\d\d-\d\d-\d\d \d\d:\d\d:\d\d, ERROR.+$", log_text, re.IGNORECASE+re.MULTILINE)

def alert_on_error(log_file):
    pass

if __name__ == '__main__':
    wpkg_logs_dir = r"\\192.168.106.24\sysadmin\logs\wpkg"
    log_files = get_log_files(wpkg_logs_dir)

    # files[:] = [f for f in log_files if re.search(include_files, f)]

    # f_array = [(f for f in log_files if get_file_contents(f)]
    f_array = [(f, get_file_contents(f)) for f in log_files]
    print ("initial file count = {}".format(len(f_array)))
    # print (f_array[0][1])
    f_array[:] = [f for f in f_array if check_wpkg_stable_branch(f[1])]
    print ("stable log file count = {}".format(len(f_array)))

    err_array = [(f[0], err_msg) for f in f_array for err_msg in get_wpkg_errors(f[1])]

    for e in err_array:
        print ("{}\t{}".format(e[0], e[1]))

    print ("err msg count = {}".format(len(err_array)))


    # files_details = [(f, get_file_contents(f)) for f in log_files]
    # print(files_details[1])


    # for log_file in log_files:
    #     # print(log_file)
    #     # f = open(log_file)
    #     # log_file_text = f.read()
    #     log_file_text = get_file_contents(log_file)
    #     # print(log_file_text)
    #     # print("stable={},  name={}".format(check_wpkg_stable_branch(log_file_text), log_file))
    #
    #
    #     if check_wpkg_stable_branch(log_file_text):
    #         err_msgs = get_wpkg_errors(log_file_text)
    #
    #         if len(err_msgs) > 0:
    #             print("Errors in logfile {}".format(log_file))
    #
    #             for err_msg in err_msgs:
    #                 print(err_msg)
