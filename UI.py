from tkinter import *

class UI:
  color_passive = '#ffffff'
  color_active = '#000000'
  color_error = '#ff637c'

  window = Tk()
  window.title("Life")

  control_frame = Frame(window)
  control_label_size = Label(control_frame, text="Встановити розмір поля:")
  control_label_size_X = Label(control_frame, text="X: ")
  control_entry_size_X = Entry(control_frame, width=3)
  control_label_size_Y = Label(control_frame, text="Y: ")
  control_entry_size_Y = Entry(control_frame, width=3)
  control_button_size = Button(control_frame, text="Створити\nполе")
  
  control_button_start = Button(control_frame, text="▶")
  control_button_pause = Button(control_frame, text="⏸")
  control_button_stop = Button(control_frame, text="⏹")
  
  control_button_speed_faster = Button(control_frame, text="🡆")
  control_button_speed_slower = Button(control_frame, text="🡆")
  control_label_step = Label(control_frame, text="Кроків: Н/А")
  control_label_speed = Label(control_frame, text="1/сек.")
  control_button_save = Button(control_frame, text="Зберегти моделювання")
  control_button_load = Button(control_frame, text="Завантажити моделювання")
  
  control_empty = [] # спискок frame-ів, котрі будуть використовуватись як проміжки між об'єктами
  
  field_frame = Frame(window)
  field_widgets = [] # список з віджетів, з котрих буде складатись поле

  def grid_all(self):
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=0, row=0)
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=4, row=2)
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=8, row=4)
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=11, row=2)
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=14, row=2)
    self.control_empty.append(Frame(self.control_frame, height=10, width=10))
    self.control_empty[-1].grid(column=16, row=2)
    self.control_empty.append(Frame(self.window, height=10, width=10))
    self.control_empty[-1].grid(column=0, row=1)
    self.control_empty.append(Frame(self.window, height=10, width=10))
    self.control_empty[-1].grid(column=3, row=3)

    self.control_frame.grid(column=1, row=0)
    self.field_frame.grid(column=1, row=2)
    
    self.control_label_size.grid(column=1, row=1, columnspan=3)
    self.control_label_size_X.grid(column=1, row=2)
    self.control_entry_size_X.grid(column=2, row=2)
    self.control_label_size_Y.grid(column=1, row=3)
    self.control_entry_size_Y.grid(column=2, row=3)
    
    self.control_button_size.grid(column=3, row=2, rowspan=2)
    self.control_button_start.grid(column=5, row=1)
    self.control_button_pause.grid(column=6, row=1)
    self.control_button_stop.grid(column=7, row=1)
    
    self.control_label_step.grid(column=5, row=2, columnspan=3)
    self.control_button_speed_slower.grid(column=5, row=3)
    self.control_label_speed.grid(column=6, row=3)
    self.control_button_speed_faster.grid(column=7, row=3)
    
    self.control_button_save.grid(column=12, row=1)

  def clear_field(self):
    """Видалити усі віджети поля"""
    for y_item in self.field_widgets:
      for x_item in y_item:
        x_item.destroy()
    self.field_widgets = []

  def fill_field(self, x, y, func):
    """Заповнює поле новими віджетами
    x, y - розмір поля

    func - функція, котру прив'язувати до клітин
    """
    self.clear_field()
    for yi in range(y):
      self.field_widgets.append([])
      for xi in range(x):
        self.field_widgets[yi].append(Frame(self.field_frame, width=10,height=10, bg=self.color_passive))
        self.field_widgets[yi][-1].bind('<Button-1>', func) 
        self.field_widgets[yi][-1].grid(row=yi, column=xi)

  def show(self):
    self.window.mainloop()