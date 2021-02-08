# Is used to parse all the PCAP/PCAPNG files within a folder and is used to either populate the GUI
# as to show all fields within the PCAP files, as well as taking the selected fields and parses them into a CSV file

import json
import os
import time

import pyshark as ps
from pyshark.packet.layer import Layer


class PcapParser:
    def __init__(self):
        self._folder = None
        self._fields = {}
        self._current_file_count = 0
        self._valid_extensions = [".pcap", ".pcapng"]

    def set_folder(self, folder):
        self._folder = folder

    def get_folder(self):
        return self._folder

    def run(self):
        t0 = time.time()
        if self._folder is None:
            return False, None

        for file in os.listdir(self._folder):               # Iterate through files in selected folder
            if self._has_valid_extension(file):
                cap = ps.FileCapture(os.path.join(self._folder, file))
                for pkt in cap:                             # Iterate through frames in files
                    pkt_fields = [field for field in dir(pkt) if isinstance(getattr(pkt, field), Layer)]
                    for layer in pkt_fields:                # Iterate through each Layer in frames
                        if layer not in self._fields:
                            attr = getattr(pkt, layer)
                            self._fields[layer] = [field for field in getattr(attr, 'field_names') if len(field) >= 2]

                cap.close()
        self._save_fields()

        t1 = time.time()
        print(t1-t0)

        return True, self._fields

    def pcap_to_csv(self, selected_fields):
        for file in os.listdir(self._folder):
            if self._has_valid_extension(file):
                cap = ps.FileCapture(os.path.join(self._folder, file))
                csv_name = f"outputs\\output{self._current_file_count}.csv"
                self._current_file_count += 1

                count = 0
                with open(csv_name, 'w') as csv:
                    header = "Frame Number, "
                    for field_name in selected_fields:
                        header += field_name + ", "

                    csv.write(f"{header}\n")
                    for pkt in cap:
                        count += 1
                        row = f"{count}, "
                        for subfield, layer_name in selected_fields.items():
                            try:
                                layer_info = getattr(pkt, f"{layer_name}")
                                row += getattr(layer_info, subfield) + ", "

                            except AttributeError as e:
                                row += "-1, "

                        csv.write(row)
                        csv.write('\n')
                cap.close()

    def _has_valid_extension(self, file):
        for extension in self._valid_extensions:
            if file.endswith(extension):
                return True
        return False

    def _save_fields(self):
        with open("outputs/fields.txt", "w") as f:
            f.write(json.dumps(self._fields))
