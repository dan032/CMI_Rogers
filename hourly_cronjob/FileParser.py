from pathlib import Path
from nfstream import NFStreamer


class FileParser:

    def __init__(self, path, directory, file_name):
        self._path = path
        self._directory = directory
        self._file_name = file_name

    def run(self):
        offline_streamer = NFStreamer(source=self._path, statistical_analysis=True, splt_analysis=10)
        print(self._directory)
        Path(f"{self._directory}").mkdir(parents=True, exist_ok=True)
        total_flows = offline_streamer.to_csv(flows_per_file=10000, path=f"{self._directory}{self._file_name}.csv")
