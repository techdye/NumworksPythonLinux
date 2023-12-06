from time import *
from random import *

from ion import *
from kandinsky import *

save = ""

# SCREEN
class Screen:
	def __init__(self, width: int = 320, height: int = 222, color: tuple = (255, 255, 255), text_margin: int = 8):
		self.width = width
		self.height = height
		self.color = color
		self.text_margin = text_margin
		self.text_size = 16
		self.max_text_size = self.height - 25

	def display_lines(self, commands):
		lines = commands.text_lines

		while (len(lines) * self.text_size + self.text_margin) > self.max_text_size:
			lines.pop(0)

		for i,line in enumerate(lines):
			draw_string(str(line), self.text_margin, self.text_margin + i * self.text_size)
	
	def reset(self):
		fill_rect(0,0,self.width,self.height,self.color)

# KEYBOARD 
class Keyboard:
	def __init__(self, commands, screen, settings, xs: int = 0, ys: int = 0, k_on: bool = True, wait_time: float = 0.1, x: int = 0, y: int = 0):
		self.text = ""
		self.text_size = 16

		self.k_on = k_on
		self.wait_time = wait_time
		self.text_margin = screen.text_margin

		self.commands = commands
		self.screen = screen
		self.settings = settings

		self.x = xs
		self.y = ys
	
	def reset_classes(self, commands, screen, settings):
		self.commands = commands
		self.screen = screen
		self.settings = settings

	def draw(self, x = None, y = None, text: str = ""):
		if len(text) <= 0:
			text = self.text
		if x == None:
			x = self.x
		if y == None:
			y = self.y

		self.screen.reset()
		draw_string(text, x + self.text_margin, screen.height - self.text_margin - self.text_size + y)

	def _spliter(self):
		return self.text.split()
	
	def _get_command(self, splited):
		if len(splited) <= 0:
			return False
		if splited[0] == "pwd":
			self.commands.pwd(self.settings)
			return True
		elif splited[0] == "ls":
			self.commands.ls(self.settings)
		elif splited[0] == "clear":
			self.commands.clear()
		
			return True
		elif len(splited) <= 1:
			return False
		elif splited[0] == "mkdir":
			self.commands.mkdir(self.settings, splited[1])
			return True
		elif splited[0] == "touch":
			self.commands.touch(self.settings, splited[1])
			return True
		elif splited[0] == "cd":
			self.commands.cd(self.settings, splited[1])
			
			return True

		return False

	def _exe(self):
		splited = self._spliter()
		self.text = ""
		self.screen.reset()

		self._get_command(splited)

	def use_keyboard(self):
		if not self.k_on:
			return False
		elif keydown(KEY_EXE):
			self._exe()
		elif keydown(KEY_EXP):
			self.text += "a" if not keydown(KEY_ALPHA) else "["
		elif keydown(KEY_LN):
			self.text += "b" if not keydown(KEY_ALPHA) else "]"
		elif keydown(KEY_LOG):
			self.text += "c" if not keydown(KEY_ALPHA) else "{"
		elif keydown(KEY_IMAGINARY):
			self.text += "d" if not keydown(KEY_ALPHA) else "}"
		elif keydown(KEY_COMMA):
			self.text += "e" if not keydown(KEY_ALPHA) else ","
		elif keydown(KEY_POWER):
			self.text += "f"
		elif keydown(KEY_SINE):
			self.text += "g"
		elif keydown(KEY_COSINE):
			self.text += "h"
		elif keydown(KEY_TANGENT):
			self.text += "i"
		elif keydown(KEY_PI):
			self.text += "j"
		elif keydown(KEY_SQRT):
			self.text += "k"
		elif keydown(KEY_SQUARE):
			self.text += "l"
		elif keydown(KEY_SEVEN):
			self.text += "m" if not keydown(KEY_ALPHA) else "7"
		elif keydown(KEY_EIGHT):
			self.text += "n" if not keydown(KEY_ALPHA) else "8"
		elif keydown(KEY_NINE):
			self.text += "o" if not keydown(KEY_ALPHA) else "9"
		elif keydown(KEY_LEFTPARENTHESIS):
			self.text += "p" if not keydown(KEY_ALPHA) else "("
		elif keydown(KEY_RIGHTPARENTHESIS):
			self.text += "q" if not keydown(KEY_ALPHA) else ")"
		elif keydown(KEY_FOUR):
			self.text += "r" if not keydown(KEY_ALPHA) else "4"
		elif keydown(KEY_FIVE):
			self.text += "s" if not keydown(KEY_ALPHA) else "5"
		elif keydown(KEY_SIX):
			self.text += "t" if not keydown(KEY_ALPHA) else "6"
		elif keydown(KEY_MULTIPLICATION):
			self.text += "u" if not keydown(KEY_ALPHA) else "*"
		elif keydown(KEY_DIVISION):
			self.text += "v" if not keydown(KEY_ALPHA) else "/"
		elif keydown(KEY_ONE):
			self.text += "w" if not keydown(KEY_ALPHA) else "1"
		elif keydown(KEY_TWO):
			self.text += "x" if not keydown(KEY_ALPHA) else "2"
		elif keydown(KEY_THREE):
			self.text += "y" if not keydown(KEY_ALPHA) else "3"
		elif keydown(KEY_PLUS):
			self.text += "z" if not keydown(KEY_ALPHA) else "+"
		elif keydown(KEY_MINUS):
			self.text += " " if not keydown(KEY_ALPHA) else "-"
		elif keydown(KEY_ZERO):
			self.text += "?" if not keydown(KEY_ALPHA) else "0"
		elif keydown(KEY_DOT):
			self.text += "!" if not keydown(KEY_ALPHA) else "."
		elif keydown(KEY_BACKSPACE):
			if len(self.text) > 0:
				self.text = self.text[0:-1]
		else:
			return False
		return True

	def set_state(self, state: bool):
		self.k_on = state
	
# DIRECTORIES AND FILES
class File:
	def __init__(self, name: str, content: str = "", back_dir = None):
		self.name = name
		self.content = content
		self.back_dir = back_dir

	def write(self, content: str):
		self.context = content
	
	def read(self):
		return self.content

	def path(self):
		stop = False
		path = []

		if self.back_dir == None:
			return path
		
		actual_dir = self.back_dir

		while not stop:
			path.insert(0,actual_dir)
			actual_dir = actual_dir.back_dir
			if actual_dir == None:
				stop = True
		return path		

class Directory:
	def __init__(self, name: str, files: list, back_dir = None):
		self.name = name
		self.files = files
		self.back_dir = back_dir

	def add_file(self, file):
		for f in self.files:
			if f.name == file.name:
				return False

		self.files.append(file)
		return True
	
	def remove_file(self, file):
		if file in self.files:
			self.files.remove(file)
	
	def path(self):
		stop = False
		path = [self]

		if self.back_dir == None:
			return path
		
		actual_dir = self.back_dir

		while not stop:
			path.insert(0,actual_dir)
			actual_dir = actual_dir.back_dir
			if actual_dir == None:
				stop = True
		return path	

# COMMANDS
class Commands:
	def __init__(self):
		self.text_lines = []

	def pwd(self, settings):
		current_directory = settings.current_directory

		self.text_lines.append("/".join([i.name for i in current_directory.path()]))
		screen.display_lines(self)
	
	def ls(self, settings):
		current_directory = settings.current_directory

		files = [i.name for i in current_directory.files]
		files_good = [[]]

		current = 0
		cursor = 0
		
		for file in files:
			if current >= 2:
				files_good.append([])
				current = 0
				cursor += 1
			files_good[cursor].append(file)
			current += 1
		
		for k,i in enumerate(files_good):
			text = ", ".join(i)
			if k + 1 < len(files_good):
				text += ","

			self.text_lines.append(text)

	def mkdir(self, settings, name):
		if settings.current_directory.add_file(Directory(name, [], settings.current_directory)):
			self.text_lines.append("Directory created!")
		else:
			self.text_lines.append("Already created.")

	def touch(self, settings, name):
		if settings.current_directory.add_file(File(name, "", settings.current_directory)):
			self.text_lines.append("File created!")
		else:
			self.text_lines.append("Already created.")

	def cd(self, settings, path):
		p = [i for i in path.split("/") if i]

		for i in p:
			exist = False

			if i == "..":
				if len(settings.current_directory.path()) >= 2:
					settings.current_directory = settings.current_directory.path()[-2]
					exist = True
				else:
					self.text_lines.append("Can't go back.")
					return

			if not exist:
				for k, file in enumerate(settings.current_directory.files):
					if file.name == i:
						try:
							file.files
						except:
							self.text_lines.append("Not a directory.")
							return

						settings.current_directory = file
						exist = True
				if not exist:
					self.text_lines.append("Doesn't exist.")
					return
	
	def rm(self, settings, path):
		p = [i for i in path.split("/") if i]
	
	def clear(self):
		self.text_lines = []


# SETTINGS
class Settings:
	def __init__(self):
		self.main_directory = Directory("src", [], None)
		self.current_directory = self.main_directory

# VARIABLES
commands = Commands()
screen = Screen()
settings = Settings()

keyboard = Keyboard(commands, screen, settings)

screen.reset()

settings.main_directory.add_file(File("readme.txt", "Welcome to the version of linux on calculator\nIt's for numworks.", settings.main_directory))

test = Directory("test", [], settings.main_directory)

settings.main_directory.add_file(test)

# RUNTIME
while True:
	keyboard.reset_classes(commands, screen, settings)
	key_wrote = keyboard.use_keyboard()
	
	if key_wrote:
		keyboard.draw()
		screen.display_lines(commands)
		sleep(keyboard.wait_time)
