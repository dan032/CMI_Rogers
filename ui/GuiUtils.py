from tkinter import filedialog
import os


def f_explore_callback(parser):
    folder_name = filedialog.askdirectory(mustexist=True, initialdir=os.getcwd())
    if folder_name != '':
        parser.set_folder(folder_name)


def _select(event, tree):
    tree.selection_toggle(tree.focus())


def submit_callback(tree, parser):
    if parser.get_folder() is not None:
        fields = {}

        for i in tree.selection():
            protocol = tree.item(i)['values'][0]
            field_name = tree.item(i)['values'][1]

            fields[field_name] = protocol

        parser.pcap_to_csv(fields)


def clear_callback(tree):
    for item in tree.selection():
        tree.selection_remove(item)


def treeview_sort_column(tv, col, reverse):
    line = [(tv.set(k, col), k) for k in tv.get_children('')]
    line.sort(reverse=reverse)

    for index, (val, k) in enumerate(line):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def create_tree_view(tree, parser):
    tree.delete(*tree.get_children())
    tree.pack(fill="both", expand=True)
    tree["columns"] = ("1", "2")
    tree["show"] = "headings"

    tree.column("1", width=150, anchor='c')
    tree.column("2", width=300, anchor="w")
    tree.heading("1", text="Protocol", command=lambda: treeview_sort_column(tree, "1", False))
    tree.heading("2", text="Field Name", command=lambda: treeview_sort_column(tree, "2", False))
    tree.bind("<ButtonRelease-1>", lambda event: _select(event, tree))

    res = parser.run()

    if res[0]:
        choices_json = res[1]
        for protocol, fields in choices_json.items():
            for field in fields:
                tree.insert("", 'end', values=(f"{protocol}", f"{field}"))
