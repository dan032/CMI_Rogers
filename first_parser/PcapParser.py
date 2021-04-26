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
        self._carry_over_fields = ["cellidentity", "mme_ue_s1ap_id", "enb_ue_s1ap_id"]

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
                        else:
                            attr = getattr(pkt, layer)
                            for field in getattr(attr, 'field_names'):
                                if field not in self._fields[layer] and len(field) >= 2:
                                    self._fields[layer].append(field)

                cap.close()
        self._save_fields()

        t1 = time.time()
        print(t1-t0)

        return True, self._fields

    def pcap_to_csv_imsi_mapping(self, selected_fields):

        for file in os.listdir(self._folder):
            carry_data = {}
            imsi_enb_mapping = {}
            # mme_imsi_mapping = {}
            sn_imsi_mapping = {}
            tei_sn_mapping = {}
            tei_imsi_mapping = {}

            header = "Frame Number,"
            for field_name in selected_fields:
                header += field_name + ","
                if field_name in self._carry_over_fields:
                    carry_data[field_name] = "-1"

            header += "IMSI"
            carry_data["imsi"] = "-1"

            if self._has_valid_extension(file):
                cap = ps.FileCapture(os.path.join(self._folder, file))
                csv_name = f"outputs\\output{self._current_file_count}.csv"
                self._current_file_count += 1

                count = 0
                with open(csv_name, 'w') as csv:
                    csv.write(f"{header}\n")
                    for pkt in cap:
                        count += 1
                        row = f"{count},"

                        if hasattr(pkt, "s1ap") and int(pkt.s1ap.procedurecode) == 12:
                            # identification_data[pkt.s1ap.e212_imsi] = {"enb_ue_s1ap_id" : pkt.s1ap.enb_ue_s1ap_id}
                            imsi_enb_mapping[pkt.s1ap.enb_ue_s1ap_id] = pkt.s1ap.e212_imsi

                        # if hasattr(pkt, "s1ap") and int(pkt.s1ap.procedurecode) == 11:
                        #     imsi = imsi_enb_mapping[pkt.s1ap.enb_ue_s1ap_id]
                        #     # identification_data[imsi]["mme_ue_s1ap_id"] = pkt.s1ap.mme_ue_s1ap_id
                        #     mme_imsi_mapping[pkt.s1ap.mme_ue_s1ap_id] = imsi

                        if hasattr(pkt, "gtpv2") and int(pkt.gtpv2.message_type) == 32:
                            sn_imsi_mapping[pkt.gtpv2.seq] = pkt.gtpv2.e212_imsi

                        if hasattr(pkt, "gtpv2") and int(pkt.gtpv2.message_type) == 33:
                            tei_sn_mapping[pkt.gtpv2.seq] = pkt.gtpv2.f_teid_gre_key
                            tei_imsi_mapping[pkt.gtpv2.f_teid_gre_key] = sn_imsi_mapping[pkt.gtpv2.seq]

                        for field_name, layer_name in selected_fields.items():
                            if field_name in carry_data and carry_data[field_name] != "-1":
                                row += carry_data[field_name] + ","
                            else:
                                if hasattr(pkt, f"{layer_name}"):
                                    layer_info = getattr(pkt, f"{layer_name}")
                                    if hasattr(layer_info, field_name):
                                        val = getattr(layer_info, field_name)
                                        if field_name == "protocols":
                                            val = val.replace(":", "|")
                                        row += val + ","
                                        if field_name in carry_data:
                                            carry_data[field_name] = getattr(layer_info, field_name)
                                    else:
                                        row += ","
                                else:
                                    row += ","

                        try:
                            if hasattr(pkt, "s1ap"):
                                carry_data["imsi"] = imsi_enb_mapping[pkt.s1ap.enb_ue_s1ap_id]
                                row += imsi_enb_mapping[pkt.s1ap.enb_ue_s1ap_id] + ","
                            elif hasattr(pkt, "gtpv2"):
                                if hasattr(pkt.gtpv2, "teid"):
                                    carry_data["imsi"] = tei_imsi_mapping[pkt.gtpv2.f_teid_gre_key]
                                    row += tei_imsi_mapping[pkt.gtpv2.f_teid_gre_key] + ","
                            elif hasattr(pkt, "gtp"):
                                if hasattr(pkt.gtp, "teid"):
                                    carry_data["imsi"] = tei_imsi_mapping[pkt.gtp.teid]
                                    row += tei_imsi_mapping[pkt.gtp.teid] + ","
                            else:
                                row += ","

                        except Exception:
                            row += ","

                        csv.write(row[:-1])
                        csv.write('\n')
                cap.close()



    def pcap_to_csv(self, selected_fields):
        header = "Frame Number,"
        for field_name in selected_fields:
            header += field_name + ","
        header = header[:-1]

        for file in os.listdir(self._folder):
            if self._has_valid_extension(file):
                cap = ps.FileCapture(os.path.join(self._folder, file))
                csv_name = f"outputs\\output{self._current_file_count}.csv"
                self._current_file_count += 1

                count = 0
                with open(csv_name, 'w') as csv:
                    csv.write(f"{header}\n")
                    for pkt in cap:
                        count += 1
                        row = f"{count},"
                        for subfield, layer_name in selected_fields.items():
                            try:
                                layer_info = getattr(pkt, f"{layer_name}")
                                row += getattr(layer_info, subfield) + ","

                            except AttributeError as e:
                                row += "-1,"

                        csv.write(row[:-1])
                        csv.write('\n')
                cap.close()

    def _has_valid_extension(self, file):
        for extension in self._valid_extensions:
            if file.endswith(extension):
                return True
        return False

    def _save_fields(self):
        with open("fields/fields.txt", "w") as f:
            f.write(json.dumps(self._fields))
#
p = PcapParser()
p.set_folder(os.path.join(os.getcwd(), "pcaps"))
with open("fields/selected_fields.txt", "r") as f:
    data = json.load(f)
    p.pcap_to_csv_imsi_mapping(data)
