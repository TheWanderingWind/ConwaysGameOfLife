class Model:
  """Реалізовує моделювання"""
  size_x, size_y = 0, 0
  step = 0
  field = []

  def new_field(self, x, y, field = None):
    """Створює нове поле"""
    self.size_x = x
    self.size_y = y
    self.field = []
    self.step = 0
    if field == None:
      for yi in range(y):
        self.field.append([])
        for xi in range(x):
          self.field[yi].append(0)
    else:
      self.field = field

  def get_nearby(self, x, y):
    """Утворює масив 3х3 з клітин навколо вказаних координат"""
    m = self.field
    xl = x - 1 # кордината, котра менше за x (y) на 1. Якщо x (або y) будуть 0, то xl (yl) будуть = -1
    yl = y - 1 # що в синтаксі вказує на останій елемент

    # а якщо x (y) будуть вказувати на останій елемет, то потрібна коректировка значення:
    if y == self.size_y - 1:
      ym = 0
    else:
      ym = y + 1
    
    if x == self.size_x - 1:
      xm = 0
    else:
      xm = x + 1
    
    result = [
      [m[yl][xl], m[yl][x], m[yl][xm]],
      [m[y][xl], m[y][x], m[y][xm] ],
      [m[ym][xl], m[ym][x], m[ym][xm]]
    ]
    return result

  def calculate_step(self):
    """Розраховує наступний крок моделювання"""
    
    new_feild = []
    for y in range(self.size_y):
      new_feild.append([])
      for x in range(self.size_x):
        nerby = self.get_nearby(x, y)
    
        # Рахуємо, скільки живих сусідів
        num_nerby = nerby[0][0] + nerby[0][1] + nerby[0][2] +\
                    nerby[1][0] +               nerby[1][2] +\
                    nerby[2][0] + nerby[2][1] + nerby[2][2]
        
        if nerby[1][1] == 0 and num_nerby == 3: # Якщо клітина спочатку була пуста
          new_feild[y].append(1)
          continue

        elif nerby[1][1] == 0:
          new_feild[y].append(0)
          continue
        
        if num_nerby == 2 or num_nerby == 3: # Якщо клітина спочатку була живою
          new_feild[y].append(1)
          continue
        else:
          new_feild[y].append(0)
          continue
    self.field = new_feild
    self.step += 1


class History:
  """Об'єкт для утворення історії процесу моделювання"""
  def __int__(self):
    self.start_field = []
    self.last_field = []
    self.size_x, self.size_y = 0, 0
    self.step = 0
    self.history = ""

  def is_all_same(self, mas, param):
    """Перевіряє, чи усі значення масиву однакові
    :param mas масив, котрий треба перевірити
    :param param знчення, котре повинно мати масив
    :returns True якщо усі значення масиву є param;
    False якщо не всі значення є param
    """
    for item in mas:
      if item == param:
        continue
    else:
      return False
    return True

  def write_full_field(self, field, step):
    """Записує в історію усе поле
    :param field поле, яке треба записати
    :param step номер кроку
    """
    self.history += "step:" + str(step) + "@"
    for item in field:
      if self.is_all_same(item, item[0]):
        self.history += "a" + str(item[0])

      else:
        for i in item:
          self.history += str(item[0])
      self.history += "@"

  def start_new_history(self, x, y, field):
    """Почати нову історію для нової моделі"""
    self.size_x = x
    self.size_y = y
    self.start_field = field
    self.last_field = field
    self.step = 0
    self.history = "@Start@"+ str(x)+"@"+str(y)+"@\n"
    self.write_full_field(field, 0)

  def add_step(self, field):
    """Записує наступний крок у історію
    :param field новий стан поля"""

    if self.history[-5:-1] == "DEAD" or self.history[-5:-1] == "@END":
      return "END" # якщо останій запис є кінець, то пропуск будь-якого запису
    
    self.step += 1
    self.history += "step:" + str(self.step) + "@"
    is_dead = True # Перевіряє, чи не пусте поле
    
    for item in field:
      if not self.is_all_same(item, 0):
        is_dead = False
        break

    if is_dead:
      self.history += "DEAD;\n"
      return "DEAD"
    
    # В кожному блоці записуємо інформацію про один рядок
    for y in range(self.size_y):
      bufer = "&" # Спочатку намагаємось сформувати зміни вказуючи на номери чисел, що змінились
      for x in range(self.size_x):
        if self.last_field[y][x] != field[y][x]:
          bufer += str(x) + ":" + str(int(field[y][x])) + ";"

      if len(bufer) > self.size_x: # Якщо такий запис довше, аніж просто записаний підряд усі значення,
        for x in field[y]: # то записуємо просто усі значення підряд
          self.history += str(x)
      elif len(bufer) == 1: # Рядок за минулий крок не змінився
        self.history += "N"
      else:
        self.history += bufer
      self.history += "@"
    self.history += "\n"
    self.last_field = field.copy()

  def end_history(self):
    """Ручне завершення запису"""
    self.history += "END;\n"

if __name__ == "__main__":
  """Консольне відлагоження"""

  print("Введіть розмір поля:")
  x, y = map(int, input().split())
  mod = Model()
  mod.new_field(x, y)
  print("Поле створено")

  def print_field():
    print()
    for yi in range(mod.size_y):
      print(mod.field[yi])
    print()

  while True:
    print_field()
    print("start - Запустити моделювання\nx, y - координати, де поставити одиницю (або нуль)")
    command = input()
    
    if command == "start":
      break
    
    command = command.split()
    if len(command) != 2:
      print("Помилкові введені данні")
      continue
    
    try:
      x, y = map(int, command)
    except:
      print("Помилкові введені данні")
      continue
  
    if mod.field[y][x] == 0:
      mod.field[y][x] = 1
    else:
      mod.field[y][x] = 0

  print("Моделювання починається.\nНатискайте Enter, щоб розрахувати наступний крок",
        "\nВведить stop щоб зупинити моделювання.")
  
  while True:
    command = input()
    if command == "stop":
      break
    mod.calculate_step()
    print_field()