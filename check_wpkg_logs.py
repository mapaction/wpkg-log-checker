import os
import os.path
import re


def get_log_files(logs_dir, recursive=False):
    for root, dirs, files in os.walk(logs_dir):
        if not recursive:
            while len(dirs) > 0:
                dirs.pop()

        # only include relevant files
        include_files = 'wpkg.*log$' # for files only
        files[:] = [os.path.join(root, f) for f in files]
        files[:] = [f for f in files if re.search(include_files, f)]

        return files

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

    for log_file in log_files:
        # print(log_file)
        f = open(log_file)
        log_file_text = f.read()
        # print(log_file_text)
        # print("stable={},  name={}".format(check_wpkg_stable_branch(log_file_text), log_file))

        # files[:] = [f for f in log_files if re.search(include_files, f)]


        if check_wpkg_stable_branch(log_file_text):
            err_msgs = get_wpkg_errors(log_file_text)

            if len(err_msgs) > 0:
                print("Errors in logfile {}".format(log_file))

                for err_msg in err_msgs:
                    print(err_msg)
