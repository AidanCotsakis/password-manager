import PgUI
import pygame
import os
import encryption
import clipboard
import random

NEW_IMAGE = "add_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
EXIT_IMAGE = "close_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
DELETE_IMAGE = "delete_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
DECRYPT_IMAGE = "key_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
VISIBLE_IMAGE = "visibility_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
HIDDEN_IMAGE = "visibility_off_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
COPY_IMAGE = "content_copy_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"
RANDOMIZE_IMAGE = "password_24dp_E8EAED_FILL0_wght400_GRAD0_opsz24.png"

PASSWORD_CHARACTERS = """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

loop = True
data = []

pygame.init()

windowSize = (1920, 1080)

clock = pygame.time.Clock()
pygame.display.set_caption("Password Manager")
os.environ['SDL_VIDEO_CENTERED'] = '1'
win = pygame.display.set_mode(windowSize, pygame.NOFRAME)

UI = PgUI.PgUI(win, windowSize[0], windowSize[1], 3, 1)

# BUTTON FUNCTIONALITY
def quit(button, link, args):
	global loop

	button.enabled = False
	UI.draw()
	pygame.display.update()

	if col2.enabled:
		string = buildString()
		encryption.write(col1_passwordBox.text, string)

	loop = False

def toggleVisibility(button, link, args):
	link.censored = not link.censored
	link.renderSurface()

	if link.censored:
		button.child.path = HIDDEN_IMAGE
	else:
		button.child.path = VISIBLE_IMAGE
	button.child.loadImage()

def loadFile(button, link, args):
	col1_decryptButton.enabled = False
	UI.draw()
	pygame.display.update()
	try:
		content = encryption.read(col1_passwordBox.text)
		content = content.split("\t")[1:-1]
		data = [content[i:i+5] for i in range(0, len(content), 5)]
		data.sort(key=lambda x: x[0])
		col1_decryptButton.enabled = False
		col1_passwordBox.enabled = False
		col1_passwordLabel.text = "SUPER DUPER SECRET MODE ACTIVATED!"
		col1_passwordLabel.renderSurface()
		col1_showHideButton.enabled = False
		col1_newButton.enabled = True
		col2.enabled = True

		for pageData in data:
			addPage(pageData = pageData)
	except:
		col1_decryptButton.enabled = True

def copy(button, link, args):
	clipboard.copy(link.text)

def randomString(button = None, link = None, args = None):
	if link.text == "":
		randomString = ""
		for i in range(args):
			randomString += random.choice(PASSWORD_CHARACTERS)

		link.text = randomString
		link.renderSurface()

def delete(button, link, args):
	global currentlyEnabled
	
	col2_list.children = [i for i in col2_list.children if i != args]
	UI.children = [i for i in UI.children if i != currentlyEnabled]
	currentlyEnabled = None

	col2_list.rePosition()

def addPage(button = None, link = None, args = [], pageData = ["", "", "", "", ""]):
	col3 = UI.add_container(tag = "page", enabled = False, col = 2)
	col3_largeContainer = col3.add_container(rows = 30, cols = 12, colour = None)

	col3_TitleLabel = col3_largeContainer.add_text(text = "TITLE:", width = 8, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", searchable = False)
	col3_UsernameLabel = col3_largeContainer.add_text(text = "USERNAME:", row = 2, width = 8, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", searchable = False)
	col3_EmailLabel = col3_largeContainer.add_text(text = "EMAIL:", row = 4, width = 8, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", searchable = False)
	col3_PasswordLabel = col3_largeContainer.add_text(text = "PASSWORD:", row = 6, width = 8, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", searchable = False)
	col3_NotesLabel = col3_largeContainer.add_text(text = "NOTES:", row = 8, width = 8, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", searchable = False)

	col3_TitleBox = col3_largeContainer.add_text(tag = "title", text = pageData[0], row = 1, width = 12, verticalAlign = "mid", margins = 0, editable = True)
	col3_UsernameBox = col3_largeContainer.add_text(tag = "username", text = pageData[1], row = 3, width = 12, verticalAlign = "mid", margins = 0, editable = True)
	col3_EmailBox = col3_largeContainer.add_text(tag = "email", text = pageData[2], row = 5, width = 12, verticalAlign = "mid", margins = 0, editable = True)
	col3_PasswordBox = col3_largeContainer.add_text(tag = "password", text = pageData[3], row = 7, width = 12, verticalAlign = "mid", margins = 0, editable = True, censored = True, searchable = False)
	col3_NotesBox = col3_largeContainer.add_text(tag = "notes", text = pageData[4], row = 9, width = 12, height = 20, margins = 0, editable = True)

	col3_TitleCopy = col3_largeContainer.add_button(row = 0, col = 11, onPress = copy, margins = 0, link = col3_TitleBox).add_image(path=COPY_IMAGE, margins = 0).parent
	col3_UsernameCopy = col3_largeContainer.add_button(row = 2, col = 11, onPress = copy, margins = 0, link = col3_UsernameBox).add_image(path=COPY_IMAGE, margins = 0).parent
	col3_EmailCopy = col3_largeContainer.add_button(row = 4, col = 11, onPress = copy, margins = 0, link = col3_EmailBox).add_image(path=COPY_IMAGE, margins = 0).parent
	col3_PasswordCopy = col3_largeContainer.add_button(row = 6, col = 11, onPress = copy, margins = 0, link = col3_PasswordBox).add_image(path=COPY_IMAGE, margins = 0).parent
	col3_NotesCopy = col3_largeContainer.add_button(row = 8, col = 11, onPress = copy, margins = 0, link = col3_NotesBox).add_image(path=COPY_IMAGE, margins = 0).parent

	col3_showHideButton = col3_largeContainer.add_button(row = 6, col = 9, onPress = toggleVisibility, margins = 0, link = col3_PasswordBox).add_image(path=HIDDEN_IMAGE, margins = 0).parent
	col3_randomizeButton = col3_largeContainer.add_button(row = 6, col = 10, onPress = randomString, margins = 0, link = col3_PasswordBox, args = 16).add_image(path=RANDOMIZE_IMAGE, margins = 0).parent

	col3_button = col2_list.add_button(onPress = swapPage, margins = 0, link = col3).add_text(text = pageData[0], verticalAlign = "mid", margins = 0, link = col3_TitleBox).parent

	col3_deleteButton = col3_largeContainer.add_button(row = 29, col = 11, onPress = delete, margins = 0, args = col3_button).add_image(path=DELETE_IMAGE, margins = 0).parent
	
	if button:
		col2_list.rePosition()
		swapPage(col3_button, col3, [])

currentlyEnabled = None
def swapPage(button, link, args):
	global currentlyEnabled
	if currentlyEnabled:
		currentlyEnabled.enabled = False
	link.enabled = True
	currentlyEnabled  = link

def buildString():
	string = ""
	for i in range(random.randint(32, 96)):
		string += random.choice(PASSWORD_CHARACTERS)
	string += "\t"
	for child in UI.children:
		if child.tag == "page":
			count = 0
			while count < 5:
				for item in child.children[0].children:
					if item.tag == "title" and count == 0:
						string += item.text + "\t"
						count += 1
					elif item.tag == "username" and count == 1:
						string += item.text + "\t"
						count += 1
					elif item.tag == "email" and count == 2:
						string += item.text + "\t"
						count += 1
					elif item.tag == "password" and count == 3:
						string += item.text + "\t"
						count += 1
					elif item.tag == "notes" and count == 4:
						string += item.text + "\t"
						count += 1
				if count < 5:
					string += "\t"
					count += 1
	for i in range(random.randint(32, 96)):
		string += random.choice(PASSWORD_CHARACTERS)

	return string

# PAGE 1
col1 = UI.add_container()
col1_largeContainer = col1.add_container(rows = 30, cols = 12, colour = None)
col1_passwordLabel = col1_largeContainer.add_text(text = "PASSWORD:", verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", width = 9)
col1_passwordBox = col1_largeContainer.add_text(text = "", verticalAlign = "mid", row = 1, width = 12, margins = 0, editable = True, censored = True)
col1_decryptButton = col1_largeContainer.add_button(row = 0, col = 9, onPress = loadFile, margins = 0, link = col1_passwordBox).add_image(path=DECRYPT_IMAGE, margins = 0).parent
col1_showHideButton = col1_largeContainer.add_button(row = 0, col = 10, onPress = toggleVisibility, margins = 0, link = col1_passwordBox).add_image(path=HIDDEN_IMAGE, margins = 0).parent
col1_newButton = col1_largeContainer.add_button(row = 0, col = 10, onPress = addPage, margins = 0, enabled = False).add_image(path=NEW_IMAGE, margins = 0).parent
col1_exitButton = col1_largeContainer.add_button(row = 0, col = 11, onPress = quit, margins = 0).add_image(path=EXIT_IMAGE, margins = 0).parent
col1_fileLabel = col1_largeContainer.add_text(text = "FILE:", row = 2, verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", width = 12)
col1_image = col1_largeContainer.add_image(path = "image.png", row = 3, height = 27, width = 12)


# PAGE 2
col2 = UI.add_container(enabled = False, col = 1)
col2_largeContainer = col2.add_container(rows = 30, colour = None)
col2_searchLabel = col2_largeContainer.add_text(text = "SEARCH:", verticalAlign = "mid", bold = True, margins = 0, colour = "Gold")
col2_searchBox = col2_largeContainer.add_text(text = "", verticalAlign = "mid", row = 1, margins = 0, editable = True)
col2_searchLabel = col2_largeContainer.add_text(text = "ENTRIES:", verticalAlign = "mid", bold = True, margins = 0, colour = "Gold", row = 2)
col2_list = col2_largeContainer.add_list(searchBox = col2_searchBox, rows = 27, row = 3, height = 27, margins = 0, colour = None)


while loop:
	clock.tick(30)
	UI.tick()

	for event in pygame.event.get():
		# Exit program
		if event.type == pygame.QUIT:
			loop = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and col1_passwordBox.selected and not col2.enabled:
			col1_passwordBox.text = col1_passwordBox.text[:-1]
			col1_passwordBox.renderSurface()
			loadFile(None, None, None)

	win.fill((0,0,0))

	UI.draw()
	pygame.display.update()

