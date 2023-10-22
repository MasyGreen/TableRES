import tkinter as tk
from tkinter import *
from tkinter import ttk
# def button_clear():
#     for el in my_entries:
#         print(el.get())


win = tk.Tk()
win.title('Table')
win.geometry('600x500')

frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])

btn1 = tk.Button(frame, text='Сбросить')#, command=button_clear)
btn2 = tk.Button(frame, text='Сохранить')
btn3 = tk.Button(frame, text='Обработать')
btn1.grid(row=0, column=0)
btn2.grid(row=0, column=1)
btn3.grid(row=0, column=2)

btn1.pack()
btn2.pack()
btn3.pack()

curRow = 5

colTempl = ["ID", "Name", "Value"]
columns = list(colTempl)

Treeview = ttk.Treeview(win, height=18, show="headings", columns=columns, selectmode="extended")

style = ttk.Style()
style.configure("Treeview", foreground='#00337f', background="#ffc61e", bordercolor="#ffc61e", borderwidth=33)
style.configure("Treeview.Heading", background="purple", foreground='#00337f', font=(14))


for el in colTempl:
    Treeview.heading(el, text=el)
    Treeview.column(el, width=200, anchor='center')


ysb = ttk.Scrollbar(win, orient=tk.VERTICAL, command=Treeview.yview)
Treeview.configure(yscroll=ysb.set)

Treeview.grid(row=curRow, column=0)
#Treeview.pack(side=LEFT, fill=BOTH)

# DataHeader = ['ID', 'NAME', 'VALUE']
#
# curRow = 1
# for i in range(0, len(DataHeader)):
#     el = tk.Entry(win, width=10)
#     el.grid(row=curRow, column=i)
#     el.insert(tk.END, DataHeader[i])
# 1111
# my_entries = []
#
# DataValues = [['1', 'Иван', '12'], ['2', 'Коля', '141']]
# for val in DataValues:
#     for i in range(0, len(val)):
#         # print(f'{i=}; {el=}; {el[0]}')
#         el = tk.Entry(win, width=10)
#         el.grid(row=curRow, column=i)
#         el.insert(tk.END, val[i])
#         my_entries.append(el)
#     curRow = curRow + 1

# 222
# columns = ("Items", "Values")
# Treeview = ttk.Treeview(win, height=18, show="headings", columns=columns)  #
#
# Treeview.column("Items", width=200, anchor='center')
# Treeview.column("Values", width=200, anchor='center')
#
# Treeview.heading("Items", text="Items")
# Treeview.heading("Values", text="Values")
# Treeview.pack(side=LEFT, fill=BOTH)


name = ['Item1', 'Item2', 'Item3']
ipcode = ['10', '25', '163']
for i in range(min(len(name), len(ipcode))):
    Treeview.insert('', i, values=(name[i], ipcode[i]))

itemCount = len(name)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def set_cell_value(event):
    for item in Treeview.selection():
        item_text = Treeview.item(item, "values")
        column = Treeview.identify_column(event.x)
        row = Treeview.identify_row(event.y)
    cn = int(str(column).replace('#', ''))
    rn = int(str(row).replace('I', ''))
    entryedit = Text(root, width=10 + (cn - 1) * 16, height=1)
    entryedit.place(x=16 + (cn - 1) * 130, y=6 + rn * 20)

    def saveedit():
        Treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()

    okb = ttk.Button(root, text='Save', width=4, command=saveedit)
    okb.place(x=90 + (cn - 1) * 242, y=2 + rn * 20)


def newrow():
    name.append('to be named')
    ipcode.append('value')
    Treeview.insert('', len(name) - 1, values=(name[len(name) - 1], ipcode[len(name) - 1]))
    Treeview.update()

    newb.place(x=0, y=(len(name) - 1) * 20 + 45)
    delb.place(x=200, y=(len(name) - 1) * 20 + 45)
    newb.update()
    delb.update()

def delrow():
    curr = Treeview.focus()
    if '' == curr: return
    #rowCount = rowCount - 1
    Treeview.delete(curr)
    Treeview.update()

    newb.place(x=0, y=(len(name) - 1) * 20 + 45)
    delb.place(x=200, y=(len(name) - 1) * 20 + 45)
    newb.update()
    delb.update()

Treeview.bind('<Double-1>', set_cell_value)
newb = ttk.Button(win, text='new item', width=20, command=newrow)
newb.place(x=0, y=(len(name) - 1) * 20 + 45)

delb = ttk.Button(win, text='del item', width=20, command=delrow)
delb.place(x=200, y=(len(name) - 1) * 20 + 45)

for col in columns:
    Treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(Treeview, _col, False))

win.mainloop()
