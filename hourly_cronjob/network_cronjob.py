import pyshark
import datetime
from pathlib import Path
from FileParser import FileParser
import time

start = time.time()

# Determines the directory and filename to be used.
# The directory that stores the PCAP and CSV files is separated into sub directories as such:
# ./Captures/[Month]/Day/[hour].pcap

date = datetime.datetime.now()
current_dir = "/home/cmi-controller/network_capture"
timestamp_directory = str(date.strftime("%B")) + "/" + str(date.day) + "/"
directory = f"{current_dir}/Captures/" + timestamp_directory
file_name = str(date.hour) + ".pcap"

Path(f"{directory}").mkdir(parents=True, exist_ok=True)

filepath = directory + file_name

with open(filepath, "a+") as output:
    capture = pyshark.LiveCapture(interface="enp0s8", output_file=filepath)     # CHANGE INTERFACE DEPENDING ON YOUR MACHINE
    capture.sniff(timeout=60*60)
    capture.close()

print(time.time() - start)
start = time.time()
fp = FileParser(filepath, f"{current_dir}/Flows/{timestamp_directory}", file_name)
fp.run()

print(time.time() - start)