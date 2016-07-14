import time
import xml.etree.ElementTree as ET
import requests
import winsound
import time


class MorseDaemon:

	def __init__(self):
		
		self.continue_running = True
		self.wait_length = 20
		
		# replace these next three with you dev key and login info for your pastebin account
		self.pastebin_dev_key = "" 
		self.pastebin_username = "" 
		self.pastebin_password = ""
		self.pastebin_user_key = None
		self.all_pastes = None
	
		self.pastes_xml = None
		self.paste_title = "project-prank";
		self.paste_key = None

		self.message = None
		self.message_delay= None
		self.message_repeat = False


		self.get_pastebin_user_key()

		while self.continue_running:	
			self.get_message()	
			self.get_paste_key()
			self.parse_message()
			for num in range(self.message_repeat):
				morsecode(self.message)
				time.sleep(2)
			self.pause()
			

		print("closing")

	def pause(self):
		time.sleep(self.wait_length)

	def get_message(self):
		r = requests.post("https://pastebin.com/api/api_post.php", data = {'api_dev_key'  : self.pastebin_dev_key,
										 'api_user_key' : self.pastebin_user_key,
										 'api_option'   : 'list'})

		if r.status_code == requests.codes.ok:
			self.all_pastes = "<root>" + r.text + "</root>";
		else:
			print("ERROR: Could not download pastes.")


	def get_paste_key(self):
		root = ET.fromstring(self.all_pastes)

		for item in root:
			if item.find('paste_title').text == self.paste_title:
				self.paste_key = item.find('paste_key').text
		return


	def get_pastebin_user_key(self):
		r = requests.post("http://pastebin.com/api/api_login.php", data = {'api_dev_key':self.pastebin_dev_key, 
                                                                                   'api_user_name': self.pastebin_username, 
                                                                                   'api_user_password':self.pastebin_password})
		if r.status_code == requests.codes.ok:
			self.pastebin_user_key = r.text
		else:
			print("ERROR: Could not get user key.")

	def parse_message(self):
		r = requests.post("http://pastebin.com/api/api_raw.php", data = {'api_dev_key':self.pastebin_dev_key, 
                                                                                 'api_user_key': self.pastebin_user_key, 
                                                                                 'api_paste_key': self.paste_key,
                                                                                 'api_option' : 'show_paste'})
		root = ET.fromstring(r.text)

		self.message = root.find('message').text
		self.message_delay = int(root.find('delay').text)
		self.message_repeat = int(root.find('repeat').text)
		self.continue_running = int(root.find('running').text)



class morsecode():

	def __init__(self, message):
		self.message = message
		self.string_to_morse()
		self.morse_to_beep()

	def sound_dot(self):
		winsound.Beep(700, 150)
		time.sleep(.05)

	def sound_dash(self):
		winsound.Beep(700, 350)
		time.sleep(.05)

	def sound_pause(self):
		time.sleep(.350)

	def sound_pause_letter(self):
		time.sleep(.10)
	
	def char_to_morse_code(self, character):
		if character == 'a' or character == 'A':
			return ".-"
		if character == 'b' or character == 'B':
			return "-..."
		if character == 'c' or character == 'C':
			return "-.-."
		if character == 'd' or character == 'D':
			return "-.."
		if character == 'e' or character == 'E':
			return "."
		if character == 'f' or character == 'F':
			return "..-."
		if character == 'g' or character == 'G':
			return "--."		
		if character == 'h' or character == 'H':
			return "...."
		if character == 'i' or character == 'I':
			return ".."
		if character == 'j' or character == 'J':
			return ".---"
		if character == 'k' or character == 'K':
			return "-.-"
		if character == 'l' or character == 'L':
			return ".-.."
		if character == 'm' or character == 'M':
			return "--"
		if character == 'n' or character == 'N':
			return "-."
		if character == 'o' or character == 'O':
			return "---"
		if character == 'p' or character == 'P':
			return ".--."
		if character == 'q' or character == 'Q':
			return "--.-"
		if character == 'r' or character == 'R':
			return ".-."
		if character == 's' or character == 'S':
			return "..."
		if character == 't' or character == 'T':
			return "-"
		if character == 'u' or character == 'U':
			return "..-"
		if character == 'v' or character == 'V':
			return "...-"
		if character == 'w' or character == 'W':
			return ".--"
		if character == 'x' or character == 'X':
			return "-..-"
		if character == 'y' or character == 'Y':
			return "-.--"
		if character == 'z' or character == 'Z':
			return "--.."
		if character == '1':
			return ".----"
		if character == '2':
			return "..---"
		if character == '3':
			return "...--"
		if character == '4':
			return "....-"
		if character == '5':
			return "....."
		if character == '6':
			return "-...."
		if character == '7':
			return "--..."
		if character == '8':
			return "---.."
		if character == '9':
			return "----."
		if character == '0':
			return "-----"
		if character == '0':
			return " "
		if character == ".":
			return ""
		if character == ",":
			return ""
		if character == "/":
			return ""
		if character == "?":
			return ""
		if character == "'":
			return ""
		if character == '"':
			return ""
		if character == ";":
			return ""
		if character == ":":
			return ""
		if character == "!":
			return ""
		if character == " ":
			return " "
		
	def string_to_morse(self):
		self.morse_string = ""
		for char in self.message:
			self.morse_string += str(self.char_to_morse_code(char) + "|")
		
	def morse_to_beep(self):
		for char in self.morse_string:
			if char == ".":
				self.sound_dot()
			elif char == "-":
				self.sound_dash()
			elif char == " ":
				self.sound_pause()
			elif char == "|":
				self.sound_pause_letter()

		

			