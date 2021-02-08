from tkinter import ttk, Tk, Button
from ui import GuiUtils
from PcapParser import PcapParser

parser = PcapParser()

root = Tk()
root.title("PCAP To CSV Converter")
root.resizable(width=1, height=1)
root.geometry("500x800")

tree = ttk.Treeview(root, selectmode="none")

file_explore_button = Button(root, text="Select PCAP Folder", width=20, command=lambda: GuiUtils.f_explore_callback(parser))
file_explore_button.pack()

retrieve_fields = Button(root, text="Retrieve PCAP Fields", width=20, command=lambda: GuiUtils.create_tree_view(tree, parser))
retrieve_fields.pack()

submit = Button(root, text="Create CSVs", width=20, command=lambda: GuiUtils.submit_callback(tree, parser))
submit.pack()

clear = Button(root, text="Clear", width=20, command=lambda: GuiUtils.clear_callback(tree))
clear.pack()


root.mainloop()
