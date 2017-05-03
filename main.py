import sys, os
import traceback
import time
import zipfile
from gathering_data import gather_data
import sending_email
import pdb

def main():
    # reminder: sys.argv[0] is the name of the script
    if len(sys.argv) == 1:
        start_gathering_and_reporting()
    if len(sys.argv) == 2:
        gathering_frequency = int(sys.argv[1])
        start_gathering_and_reporting(gathering_frequency)
    if len(sys.argv) == 3:
        gathering_frequency = int(sys.argv[1])
        reporting_frequency = int(sys.argv[2])
        start_gathering_and_reporting(gathering_frequency, reporting_frequency)


def start_gathering_and_reporting(gathering_frequency=300, reporting_frequency=86400, retry_after_error=True):
    error_counter = 0
    time_to_next_report = reporting_frequency
    previous_report_timestamp = time.time()
    current_time_string = time.strftime("%Y_%m_%d_%H_%M_%S")
    current_dir_name = current_time_string
    while(True):
        try:
            current_time_string = time.strftime("%Y_%m_%d_%H_%M_%S")
            current_timestamp = time.time()
            if current_timestamp - previous_report_timestamp >= reporting_frequency:
                zip_dir(current_dir_name)
                sending_email.send_data(current_dir_name)
                current_dir_name = current_time_string
                previous_report_timestamp = current_timestamp

            safe_mkdir(current_dir_name)
            filename = current_dir_name + "/" + current_time_string + ".json"
            gather_data.get_data(filename)
            print "Time of data dump:", current_time_string
            sleeping_time = gathering_frequency

            if error_counter != 0:
                sending_email.send_end_error_mail(error_counter)
                error_counter = 0

        except Exception as e:
            print "ERROR, gonna try again"
            print e
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            error_counter += 1
            if error_counter == 1:
                sending_email.send_error_mail(e)
            if retry_after_error:
                sleeping_time = gathering_frequency/10

        time.sleep(sleeping_time)


def safe_mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def zip_dir(dir_name):
    zip_handle = zipfile.ZipFile(dir_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
    
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            zip_handle.write(os.path.join(root, file))


if __name__ == "__main__":
    main()
