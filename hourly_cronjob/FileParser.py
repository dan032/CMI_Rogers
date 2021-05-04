from pathlib import Path
from nfstream import NFStreamer


class FileParser:
    """
    Creates a CSV file containing flow information based off of the provided PCAP file

    path: str
        The absolute path of the pcap file
    directory: str
        The directory to save the csv file
    file_name: str
        The name of the file
    """
    def __init__(self, path, directory, file_name):
        self._path = path
        self._directory = directory
        self._file_name = file_name

    def run(self):
        offline_streamer = NFStreamer(source=self._path, statistical_analysis=True, splt_analysis=10)
        print(self._directory)
        Path(f"{self._directory}").mkdir(parents=True, exist_ok=True)
        total_flows = offline_streamer.to_csv(flows_per_file=10000, path=f"{self._directory}{self._file_name}.csv")
