import tkinter as tk

class DnDFrame(tk.Frame):
    pass

main = tk.Tk()
notesFrame = DnDFrame(main, bd = 4, bg = "grey")
notesFrame.place(x=10,y=10)
notes = tk.Text(notesFrame)
notes.pack()

def DragDropWidget(cls):
    def init(self, *args, **kwargs):
        __init__(self, *args, **kwargs)
        self.drag_start_x= 0
        self.drag_start_y= 0
        self.bind("<Button-1>", drag_start)
        self.bind("<B1-Motion>", drag_motion)

    def drag_start(event):
        widget= event.widget
        widget.drag_start_x= event.x
        widget.drag_start_y= event.y

    def drag_motion(event):
        widget= event.widget
        x= widget.winfo_x()-widget.drag_start_x+event.x
        y= widget.winfo_y()-widget.drag_start_y+event.y
        widget.place(x=x, y=y)

    __init__= cls.__init__
    cls.__init__= init

    return cls