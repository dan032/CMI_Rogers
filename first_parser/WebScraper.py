# Was used in previous iterations to scrape WireShark's webpages to populate the possible fields to select in the GUI
# Not used in current iteration as fields displayed in GUI are taken directly from the PCAP files themselves
import requests
from bs4 import BeautifulSoup
import json


class WebScraper:
    def __init__(self):
        self._user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                           '(KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        self._fields = {}
        self._urls = {
            'Frame': 'https://www.wireshark.org/docs/dfref/f/frame.html',
            'TCP': 'https://www.wireshark.org/docs/dfref/t/tcp.html',
            'UDP': 'https://www.wireshark.org/docs/dfref/u/udp.html',
            'SCTP': 'https://www.wireshark.org/docs/dfref/s/sctp.html',
            'S1AP': 'https://www.wireshark.org/docs/dfref/s/s1ap.html',
            'GTP': 'https://www.wireshark.org/docs/dfref/g/gtp.html',
            'IP': 'https://www.wireshark.org/docs/dfref/i/ip.html'
        }

    def run(self):
        self._iterate_urls()
        self._save_fields()

    def _iterate_urls(self):
        for protocol, url in self._urls.items():
            r = requests.get(url, headers={'user-agent': self._user_agent})
            soup = BeautifulSoup(r.content, 'html.parser')
            field_table = soup.find_all("tr")
            self._fields[protocol] = []
            for field_idx in range(1, len(field_table)):

                field_cols = field_table[field_idx].find_all("td")
                field_name = ""
                field_desc = ""
                for col_idx in range(0, len(field_cols) - 1):
                    if col_idx == 0:
                        field_name = field_cols[col_idx].text
                    if col_idx == 1:
                        field_desc = field_cols[col_idx].text

                protocol_dict = {field_name: field_desc}
                self._fields[protocol].append(protocol_dict)

    def _save_fields(self):
        with open("fields/fields.txt", "w") as f:
            f.write(json.dumps(self._fields))



