from tkinter import *
from tkinter import messagebox, filedialog
import time
from threading import Thread, Lock
import Source
import UI

lock = Lock()

class Control:
  speed = 1
  is_can_be_change = True
  is_runing = False
  is_end_modeling = True
  size_x, size_y = 0, 0
  ui = UI.UI()
  his = Source.History()
  model = Source.Model()
  memory = {}
  is_read = False
  th = None

  def __int__(self):
    self.speed = 1
    self.is_can_be_change = True
    self.is_runing = False
    self.is_end_modeling = True
    self.size_x, self.size_y = 0, 0
    self.ui = UI.UI()
    self.his = Source.History()
    self.model = Source.Model()
    self.ui.window.protocol("WM_DELETE_WINDOW", self.on_closing)

  def on_closing(self):
    self.is_can_be_change = True
    self.is_runing = False
    self.is_end_modeling = True

  def read_input(self, event):
    wid = event.widget
    inp = wid.get()
    if wid['bg'] == self.ui.color_error:
      wid['bg'] = '#ffffff'
    
    try:
      int_data = int(inp)
    except:
      wid["bg"] = self.ui.color_error
      return
    
    if wid == self.ui.control_entry_size_X:
      self.size_x = int_data
    if wid == self.ui.control_entry_size_Y:
      self.size_y = int_data

  def read_field(self):
    fe = self.ui.field_widgets
    field = []
    for y in range(self.size_y):
      field.append([])
      for x in range(self.size_x):
        if fe[y][x]["bg"] == self.ui.color_passive:
          field[y].append(False)
        else:
          field[y].append(True)
    return field

  def setup(self):
    self.ui.grid_all()
    self.ui.control_button_pause.config(state=DISABLED)
    self.ui.control_button_stop.config(state=DISABLED)
    self.ui.control_button_save.config(state=DISABLED)

    self.ui.control_button_speed_faster['command'] = self.inc_speed
    self.ui.control_button_speed_slower['command'] = self.dec_speed

    self.ui.control_button_start['command'] = self.run
    self.ui.control_button_pause['command'] = self.pause
    self.ui.control_button_stop['command'] = self.stop

    self.ui.control_entry_size_X.bind("<KeyRelease>", self.read_input)
    self.ui.control_entry_size_Y.bind("<KeyRelease>", self.read_input)

    self.ui.control_button_size['command'] = self.make_widgets
    self.ui.control_button_save['command'] = self.save

    self.ui.show()

  def run(self):
    if self.is_end_modeling: # Моделювання ще не було, або закінчено
      if len(self.ui.field_widgets) == 0:
        messagebox.showinfo("Поле не створено", "Неможливо запустити моделювання, поки не існує поля")
        return
      
      have = False
      for y in self.ui.field_widgets:
        for x in y:
          if x['bg'] == self.ui.color_active:
            have = True
            break
        if have:
          break
      if not have:
        messagebox.showinfo("Поле пусте", "Неможливо запустити моделювання, якщо в полі нічого нема")
        return
    
      self.is_runing = True
      self.is_can_be_change = False
      self.is_end_modeling = False
      self.ui.control_button_stop.config(state=NORMAL)
      self.ui.control_button_pause.config(state=NORMAL)
      self.ui.control_button_save.config(state=NORMAL)
      self.ui.control_button_start.config(state=DISABLED)

      self.th = Thread(target=self.cycle_modeling)
      self.th.start()

    else: # Моделювання вже було почато, але призупинено
      self.is_runing = True
      self.ui.control_button_start.config(state=DISABLED)
      self.ui.control_button_pause.config(state=NORMAL)

  def pause(self):
    self.is_runing = False
    self.ui.control_button_pause.config(state=DISABLED)
    self.ui.control_button_start.config(state=NORMAL)

  def stop(self):
    self.is_end_modeling = True
    self.ui.control_button_pause.config(state=DISABLED)
    self.ui.control_button_stop.config(state=DISABLED)
    self.ui.control_button_start.config(state=NORMAL)
    self.ui.control_button_save.config(state=NORMAL)
    self.is_runing = False
    self.is_can_be_change = True

  def fill_color(self, field):
    """Зафарбовує поле відповідно вхідних даних"""
    for y in range(self.size_y):
      for x in range(self.size_x):
        if field[y][x]:
          self.ui.field_widgets[y][x]["bg"] = self.ui.color_active
        else:
          self.ui.field_widgets[y][x]["bg"] = self.ui.color_passive

  def cycle_modeling(self):
    """Цикл моделювання. Розрахованний для запуску в окремому потоку"""
    fe = self.read_field()
    self.model.new_field(x=self.size_x, y=self.size_y, field=fe)
    self.his.start_new_history(self.size_x, self.size_y, fe)
    
    self.memory = {0:self.model.field}
    
    while True:
      if self.is_end_modeling:
        self.his.end_history() # Завершує моделювання
        break
      
      if not self.is_runing:
        continue # Зупиняє розрахунок, якщо вминкута пауза
    
      tim = time.time()
    
      speed = self.speed
      self.model.calculate_step()
      command = self.his.add_step(self.model.field)
      if command == "DEAD":
        messagebox.showinfo("Більше нічого нема", "В полі не залишилося живих клітин. Закінчення моделювання")
        return

      self.memory[self.model.step] = self.model.field
      self.ui.control_label_step['text'] = "Кроків: " + str(self.model.step)

      while time.time() - tim < speed:
        pass # наступник крок не буде розраховуватись, поки не пройде достатньо часу
      
      self.fill_color(self.model.field)

  def change_color(self, event):
    """Змінює колір віджета, в залежності від минулого кольору
    Розрахований на прив'язку до цього віджета"""
    wid = event.widget
    if not self.is_can_be_change:
      return
    
    if wid["bg"] == self.ui.color_passive:
      wid["bg"] = self.ui.color_active
    else:
      wid["bg"] = self.ui.color_passive

  def inc_speed(self):
    if self.speed == 0.1:
      return
    elif self.speed == 0.25:
      self.ui.control_label_speed['text'] = "10/сек"
      self.speed = 0.1
    elif self.speed == 0.5:
      self.ui.control_label_speed['text'] = "4/сек"
      self.speed = 0.25
    elif self.speed == 1:
      self.ui.control_label_speed['text'] = "2/сек"
      self.speed = 0.5
    elif self.speed == 2:
      self.ui.control_label_speed['text'] = "1/сек"
      self.speed = 1
    elif self.speed == 4:
      self.ui.control_label_speed['text'] = "1/2сек"
      self.speed = 2

  def dec_speed(self):
    if self.speed == 4:
      return
    elif self.speed == 2:
      self.ui.control_label_speed['text'] = "1/4сек"
      self.speed = 4
    elif self.speed == 1:
      self.ui.control_label_speed['text'] = "1/2сек"
      self.speed = 2
    elif self.speed == 0.5:
      self.ui.control_label_speed['text'] = "1/сек"
      self.speed = 1
    elif self.speed == 0.25:
      self.ui.control_label_speed['text'] = "2/сек"
      self.speed = 0.5
    elif self.speed == 0.1:
      self.ui.control_label_speed['text'] = "4/сек"
      self.speed = 0.25

  def make_widgets(self):
    if self.size_x <= 0 or self.size_y <= 0:
      messagebox.showinfo("Введенні дані некоректні", "Неможливо створити поле.")
      return
    
    end = False
    for y in self.ui.field_widgets:
      for x in y:
        if x['bg'] == self.ui.color_active:
          q = messagebox.askquestion("Поле не пусте", " Ви точно хочете перестворити поле?")
          if q == "yes":
            end = True
            break
          else:
            return
      if end:
        break
    self.ui.fill_field(self.size_x, self.size_y, self.change_color)

  def save(self):
    file = filedialog.asksaveasfile(title="Зберегти", filetypes=(("Текстові файли", "*.txt"), ))
    file.write(self.his.history)
    file.close()


if __name__ == '__main__':
  control = Control()
  control.setup()
  pass