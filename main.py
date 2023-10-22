import os.path
import tkinter as tk
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET


Treeview = None
frame_tw = None

def load_xml():
    """
    Load XML from file
    :return:
    """
    print("Load XML from file")
    try:
        data_set_XML.clear()
        if os.path.isfile(dataset_file_name):
            root = ET.parse(dataset_file_name).getroot()
            for type_tag in root.findall('item'):
                new_item = {"id": type_tag.get('id', ""),
                            "name": type_tag.get('name', ""),
                            "value": type_tag.get('value', "")}
                data_set_XML.append(new_item)
        print(f"Read {len(data_set_XML)} values from file\n")
    except:
        print("Can`t load file (\n")


def save_xml():
    """
    Save TreeView to XML
    :return:
    """
    print("Save TreeView to XML")
    try:
        _xml_root = ET.Element("root")  # root

        for el in Treeview.get_children():
            values = Treeview.item(el)["values"]
            _xml_Document = ET.SubElement(_xml_root, "item")
            _xml_Document.set("id", str(values[0]))
            _xml_Document.set("name", str(values[1]))
            _xml_Document.set("value", str(values[2]))

        _xml_tree = ET.ElementTree(_xml_root)
        _xml_tree.write(dataset_file_name, encoding='utf-8', xml_declaration=True, method='xml')

        print(f"Save {len(Treeview.get_children())} values to file...")
    except:
        print("Can`t save file (")


def fill_treeview():
    """
    Fill TreeView from Set, previous clear TV
    :param Treeview:
    :return:
    """
    print("Fill TreeView from Set")
    try:
        i = 0
        Treeview.delete(*Treeview.get_children())
        print(list(data_set_XML))
        for item in data_set_XML:
            Treeview.insert('', i, values=(item.get("id"), item.get("name"), item.get("value")))
            i = i + 1
            print(i)
        print(f"Insert {i} values\n")
    except:
        print("Can`t fill treeview (\n")


def fill_file_values():
    """
    Fill TreeView XML values
    :param Treeview:
    :return:
    """
    print('Load XML values...\n')
    data_set_XML.clear()
    load_xml()
    fill_treeview()

def fill_default_values():
    """
    Fill TreeView default values
    :param Treeview:
    :return:
    """
    print('Load default values...\n')
    data_set_XML.clear()
    new_item = {"id": "1", "name": "one", "value": "1900"}
    data_set_XML.append(new_item)

    new_item = {"id": "2", "name": "two", "value": "2500"}
    data_set_XML.append(new_item)
    fill_treeview()


def add_new_row():
    Treeview.insert('', len(Treeview.get_children())-1, values=(f"{len(Treeview.get_children()) + 1}", "", ""))
    Treeview.update()
    print("Add row\n")


def delete_row():
    curr = Treeview.focus()
    if '' == curr: return
    Treeview.delete(curr)
    Treeview.update()
    print("Del row\n")



def set_cell_value(event):
    """
    Edit cell value inline
    """
    for item in Treeview.selection():
        item_text = Treeview.item(item, "values")
        column = Treeview.identify_column(event.x)
        row = Treeview.identify_row(event.y)

    #print(f"{item_text=}; {column=}; {row=};")
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    #print(f"{item_text=}; {cn=}; {rn=}; {item_text[cn - 1]}")

    entryedit = Text(frame_tw, width=20, height=1)
    entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)
    entryedit.insert("1.0", item_text[cn - 1])

    def saveedit():
        Treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb1.destroy()
        okb2.destroy()
        print("Save cell value\n")

    def canceledit():
        entryedit.destroy()
        okb1.destroy()
        okb2.destroy()
        print("Cancel cell value\n")

    okb1 = ttk.Button(frame_tw, text='Save', width=6, command=saveedit)
    okb1.place(x=16 + (cn - 1) * 130, y=30 + rn * 20)

    okb2 = ttk.Button(frame_tw, text='Cancel', width=6, command=canceledit)
    okb2.place(x=80 + (cn - 1) * 130, y=30 + rn * 20)

def treeview_sort_column(tv, col, reverse):
    """
    Сортировка
    :param tv:
    :param col:
    :param reverse:
    """
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def main():
    load_xml()

    win = tk.Tk()
    win.title('Table')
    win.geometry('600x500')

    style = ttk.Style()
    # style.configure("Treeview", foreground='#00337f', background="#ffc61e", bordercolor="#ffc61e", borderwidth=33)
    style.configure("Treeview.Heading", background="purple", foreground='#00337f', font= ('calibri', 12, 'bold'))
    style.configure('TButton', font= ('calibri', 12, 'bold'), borderwidth='4')

    # TREEVIEW
    frame_tw = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    colTempl = ["ID", "Name", "Value"]
    columns = list(colTempl)

    global Treeview
    Treeview = ttk.Treeview(frame_tw, show="headings", columns=columns, selectmode="extended")

    for el in colTempl:
        Treeview.heading(el, text=el)
        Treeview.column(el, width=100, anchor='center')

    fill_treeview()

    Treeview.pack(fill=BOTH, expand=True)
    Treeview.bind('<Double-1>', set_cell_value)

    # Sorting
    for col in columns:
        Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Treeview, _col, False))

    # UPPER BTN
    frame_up_bt = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    up_btn_1 = ttk.Button(frame_up_bt, text='Load', width=20, command=lambda: fill_file_values())
    up_btn_1.grid(row=0, column=1, padx=5, pady=5)

    up_btn_2 = ttk.Button(frame_up_bt, text='Save', width=20, command=lambda: save_xml())
    up_btn_2.grid(row=0, column=2, padx=5, pady=5)

    up_btn_3 = ttk.Button(frame_up_bt, text='Process', width=20,)
    up_btn_3.grid(row=0, column=3, padx=5, pady=5)

    ub_btn_4 = ttk.Button(frame_up_bt, text='Load Default', width=20, command=lambda: fill_default_values())
    ub_btn_4.grid(row=0, column=3, padx=5, pady=5)

    # DOWN BTN
    frame_dw_btn = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
    new_btn = ttk.Button(frame_dw_btn, text='Add Row', width=20, command=lambda: add_new_row())
    new_btn.grid(row=0, column=1, padx=5, pady=5)
    del_btn = ttk.Button(frame_dw_btn, text='Del Row', width=20, command=lambda: delete_row())
    del_btn.grid(row=0, column=2, padx=5, pady=5)

    # FRAME PACK
    frame_up_bt.pack(side=TOP, fill=X, padx=5, pady=5)
    frame_tw.pack(fill=BOTH, expand=True, padx=5, pady=5)
    frame_dw_btn.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    win.mainloop()


if __name__ == '__main__':
    dataset_file_name = os.path.join(os.path.curdir, "dataset.xml")
    data_set_XML = []
    main()
