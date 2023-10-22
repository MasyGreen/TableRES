import os.path
import tkinter as tk
from tkinter import *
from tkinter import ttk
import xml.etree.ElementTree as ET

def load_xml(Treeview):
    data_set_XML = []
    dataset_file_name = os.path.join(os.path.curdir, "dataset.xml")
    if os.path.isfile(dataset_file_name):
        root = ET.parse(dataset_file_name).getroot()
        for type_tag in root.findall('item'):
            new_item = {"id": type_tag.get('id', ""), "name": type_tag.get('name', "")}
            data_set_XML.append(new_item)
    i = 0
    for item in data_set_XML:
        Treeview.insert('', i, values=(item.get("id"), item.get("name"), item.get("value")))
        i = i + 1


win = tk.Tk()
win.title('Table')
win.geometry('600x500')

# UPPER BTN
frame_bt = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
btn1 = tk.Button(frame_bt, text='Сбросить').grid(row=0, column=1, padx=5, pady=5)  # , command=button_clear)
btn2 = tk.Button(frame_bt, text='Сохранить').grid(row=0, column=2, padx=5, pady=5)
btn3 = tk.Button(frame_bt, text='Обработать').grid(row=0, column=3, padx=5, pady=5)
frame_bt.pack(side=TOP, fill=X, padx=5, pady=5)

# TREEVIEW
frame_tw = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
colTempl = ["ID", "Name", "Value"]
columns = list(colTempl)

Treeview = ttk.Treeview(frame_tw, show="headings", columns=columns, selectmode="extended")

style = ttk.Style()
# style.configure("Treeview", foreground='#00337f', background="#ffc61e", bordercolor="#ffc61e", borderwidth=33)
style.configure("Treeview.Heading", background="purple", foreground='#00337f', font=20)

for el in colTempl:
    Treeview.heading(el, text=el)
    Treeview.column(el, width=100, anchor='center')

load_xml(Treeview)


# id_list = ['Item1', 'Item2', 'Item3', 'Item1', 'Item2', 'Item3']
# name_list = ['10', '25', '163', '10', '25', '163']
# for i in range(min(len(id_list), len(name_list))):
#     Treeview.insert('', i, values=(id_list[i], name_list[i], ""))


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


def set_cell_value(event):
    """
    Установить значение ячейки
    """
    for item in Treeview.selection():
        item_text = Treeview.item(item, "values")
        column = Treeview.identify_column(event.x)
        row = Treeview.identify_row(event.y)

    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))

    print(f"{item_text=}; {cn=}; {rn=}; {item_text[cn - 1]}")

    entryedit = Text(frame_tw, width=20, height=1)
    entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)
    entryedit.insert("1.0", item_text[cn - 1])

    def saveedit():
        Treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb1.destroy()
        okb2.destroy()

    def canceledit():
        entryedit.destroy()
        okb1.destroy()
        okb2.destroy()

    okb1 = ttk.Button(frame_tw, text='Save', width=6, command=saveedit)
    okb1.place(x=16 + (cn - 1) * 130, y=30 + rn * 20)

    okb2 = ttk.Button(frame_tw, text='Cancel', width=6, command=canceledit)
    okb2.place(x=80 + (cn - 1) * 130, y=30 + rn * 20)


def newrow():
    id_list.append('to be named')
    name_list.append('value')
    Treeview.insert('', len(id_list) - 1, values=(id_list[len(id_list) - 1], name_list[len(id_list) - 1]))
    Treeview.update()


def delrow():
    curr = Treeview.focus()
    if '' == curr: return
    Treeview.delete(curr)
    Treeview.update()


for col in columns:
    Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Treeview, _col, False))

Treeview.pack(fill=BOTH, expand=True)
frame_tw.pack(fill=BOTH, expand=True, padx=5, pady=5)

# КНОПКИ СНИЗУ
frame_dbtn = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
Treeview.bind('<Double-1>', set_cell_value)

newb = ttk.Button(frame_dbtn, text='Добавить', width=20, command=newrow).grid(row=0, column=1, padx=5, pady=5)
delb = ttk.Button(frame_dbtn, text='Удалить', width=20, command=delrow).grid(row=0, column=2, padx=5, pady=5)

frame_dbtn.pack(side=BOTTOM, fill=X, padx=5, pady=5)
win.mainloop()
