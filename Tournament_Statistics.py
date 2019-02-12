import os
import csv
import cv2
import imutils
import random
import numpy as np
from pprint import pprint
from collections import Counter
from PIL import Image as Img
from PIL import ImageTk
from random import randint
from Tkinter import *
import Tkinter,tkFileDialog, tkMessageBox
meta_path = "./Tournament_Logs/Meta_Information.csv"

def Card_Information_GUI(meta_path):
	class Generator_Screen:
		PLAYER = " "
		TOURNAMENT = " "
		bad_exit = True
		
		def Exit_Program(self,event='<Button-1>'):
			self.master.destroy()

		def Start_Program(self,event='<Button-1>'):
			Generator_Screen.PLAYER = self.player_var.get()
			Generator_Screen.TOURNAMENT = self.tournament_var.get()
			Generator_Screen.bad_exit = False
			self.master.destroy()
			
		def Retrieve_Information(self,meta_path):
			player_array = ["None"]
			tournament_array = ["All"]
			with open(meta_path, 'rb') as csvfile:
				reader = csv.reader(csvfile,delimiter=',',quotechar='|')
				for row in reader:
					if row[3] not in tournament_array:
						tournament_array.append(row[3])
					players = row[5:]
					for groups in players:
						for people in players:
							if people.strip() not in player_array and len(people) > 0:
								player_array.append(people.strip())
			return player_array,tournament_array
			
		def __init__(self,master):
			
			# configure master window
			self.master = master
			self.master.resizable(0,0)
			master.title('Pump It Up Card Generator')
			
			# creates icon in top left corner
			if os.name == 'nt':
				self.master.iconbitmap("./Graphics/icon.ico")

			p_arr,t_arr = self.Retrieve_Information(meta_path)
			
			self.player_var = StringVar(self.master)
			self.tournament_var = StringVar(self.master)
			self.player_var.set(p_arr[0])
			self.tournament_var.set(t_arr[0])
			
			# TODO: Create file options at top for full gui support
			# blank bar at top for "file, edit, view, help" setings
			self.File_Options = Tkinter.Frame(self.master, height=25)
			self.File_Options.grid(row=0,column=0)
			
			# Images for buttons and splash screen
			self.Main_Menu = Tkinter.PhotoImage(file="./Graphics/Generator_Logo.gif")
			self.Start = Tkinter.PhotoImage(file="./Graphics/Generate_Card.gif")
			self.Exit = Tkinter.PhotoImage(file="./Graphics/Exit_Program.gif")
			
			# splash screen image
			self.Selected_Song = Tkinter.Label(self.master, image=self.Main_Menu)
			self.Selected_Song.grid(row=1,column=0)

			# Contains all buttons and widgets
			self.Button_Frame = Tkinter.Frame(self.master, height=90)
			self.Button_Frame.grid(row=2,column=0)
			
			# important buttons
			self.Command_Options = Tkinter.Frame(self.Button_Frame, height=90)
			self.Command_Options.config(bg="WHITE")
			self.Command_Options.grid(row=0,column=2,pady=(25,25))
			
			player_text = Tkinter.Label(self.Command_Options, text="Player")
			tournament_text = Tkinter.Label(self.Command_Options, text="Tournament")
			player_text.configure(font=("TkDefaultFont",20))
			tournament_text.configure(font=("TkDefaultFont",20))
			player_text.grid(row=0,column=0,sticky=W+E+N+S)
			tournament_text.grid(row=0,column=1,sticky=W+E+N+S)
			player_menu = Tkinter.OptionMenu(self.Command_Options, self.player_var, *p_arr)
			player_menu.config(bg='WHITE')
			tournament_menu = Tkinter.OptionMenu(self.Command_Options, self.tournament_var, *t_arr)
			tournament_menu.config(bg='WHITE')
			player_menu.configure(font=("TkDefaultFont",20))
			tournament_menu.configure(font=("TkDefaultFont",20))
			player_menu.grid(row=1,column=0,sticky=W+E+N+S)
			tournament_menu.grid(row=1,column=1,sticky=W+E+N+S)
			
			# exits program
			self.Start_Button = Tkinter.Button(self.Command_Options, image=self.Start, command=self.Start_Program)
			self.Start_Button.grid(row=2,column=0,sticky=W+E+N+S)
			# exits program
			self.Exit_Button = Tkinter.Button(self.Command_Options, image=self.Exit, command=self.Exit_Program)
			self.Exit_Button.grid(row=2,column=1,sticky=W+E+N+S)
			

			# hotkeys
			self.master.bind("<Return>", self.Exit_Program)
			self.master.bind("<Escape>", self.Exit_Program)
	
	# starts GUI
	Generator_Root = Tkinter.Tk()
	Generator_Window = Generator_Screen(Generator_Root)
	Generator_Root.mainloop()
	
	return Generator_Screen.PLAYER,Generator_Screen.TOURNAMENT,Generator_Screen.bad_exit
def Generate_Player_Card(PLAYER,TOURNAMENT,meta_path):
	def return_song_information(song_array,diff_array,mode_array,player_array,tournament_array,player="All",Tournament="All"):
		try:
			song_counts  = Counter()
			level_counts = Counter()
			
			songs  = []
			levels = []
			for i in range(len(song_array)):
				if (player in player_array[i+1] or player == "All") and Tournament in [tournament_array[i+1],"All"]:
					if mode_array[i] == "Singles":
						mode = 'S'
					elif mode_array[i] == "Doubles":
						mode = 'D'
						
					songs.append(song_array[i])
					song_counts[song_array[i]] += 1
					level = "%s %s%s" % (song_array[i],mode,diff_array[i])
					levels.append(level)
					level_counts[level] += 1
					
			sorted_song = sorted(songs, key=lambda x: -song_counts[x])
			sorted_level = sorted(levels, key=lambda x: -level_counts[x])
			printstring = ["Most Played Song:", "%s. (%d plays)" % (sorted_song[0],song_counts[sorted_song[0]]) ,"Most Played Level:", "%s. (%d plays)" % (sorted_level[0],level_counts[sorted_level[0]])]
			return printstring
		except:
			return []
		
	def return_difficulty_information(diff_array,mode_array,player_array,tournament_array,player="All",Tournament="All"):
		try:
			player_diff_array = []
			player_mode_array = []
			
			for i in range(len(diff_array)):
				if (player in player_array[i+1] or player == "All") and Tournament in [tournament_array[i+1],"All"]:
					if mode_array[i] == "Singles":
						mode = 'S'
					elif mode_array[i] == "Doubles":
						mode = 'D'

					player_diff_array.append(diff_array[i])
					player_mode_array.append("%s%d" %(mode,diff_array[i]))
			
			avg_value = sum(player_diff_array)/len(player_diff_array)
			highest_difficulty = max(player_diff_array)

			diff_counts = Counter()
			for elements in player_mode_array:
				diff_counts[elements] += 1
					
			sorted_list = sorted(player_mode_array, key=lambda x: -diff_counts[x])
			most_played = sorted_list[0]

			printstring = ["Average difficulty level: %d." % (avg_value), "Highest difficulty level: %d." % (highest_difficulty), "Most played difficulty: %s. (%d plays)" % (most_played,diff_counts[most_played])]
			return printstring
		except:
			return []
		
	def return_win_rate(winner_array,player_array,tournament_array,player="All",Tournament="All"):
		try:
			win_counts = Counter()
			for i in range(len(winner_array)):
				if Tournament in [tournament_array[i],"All"]:
					win_counts[winner_array[i].strip()] += 1

			player_counts = Counter()
			for i in range(len(player_array)):
				if Tournament in [tournament_array[i],"All"]:
					for players in player_array[i]:
						player_counts[players.strip()] += 1
			
			for indexes in win_counts:
				if indexes == player:
					win_percent = (float(win_counts[indexes])/float(player_counts[indexes]))*100.00
					printstring = [ "Number of games played: %d." % (player_counts[indexes]),"Number of games won: %d." % (win_counts[indexes]),
						"Average win rate: %.2f%%. (%d wins %d losses)" % (win_percent,win_counts[indexes],player_counts[indexes]-win_counts[indexes])]
			return printstring
						
		except:
			return []
	song_array = []
	mode_array = []
	diff_array = []

	tournament_array = ["All"]
	winner_array     = ["All"]
	player_array     = ["All"]

	with open(meta_path, 'rb') as csvfile:
		reader = csv.reader(csvfile,delimiter=',',quotechar='|')
		for row in reader:
			song_array.append(row[0])
			mode_array.append(row[1])
			diff_array.append(int(row[2]))
			tournament_array.append(row[3])
			winner_array.append(row[4])
			player_array.append([players for players in row[5:] if len(players) > 0])

	height = 780
	width = 640
	filler_string = ''
	for characters in PLAYER:
		filler_string += "="
	filler_string = filler_string [:-2]

	song_info = return_song_information(song_array,diff_array,mode_array,player_array,tournament_array,PLAYER,TOURNAMENT)
	diff_info = return_difficulty_information(diff_array,mode_array,player_array,tournament_array,PLAYER,TOURNAMENT)
	win_info  = return_win_rate(winner_array,player_array,tournament_array,PLAYER,TOURNAMENT)

	splash_array = ["./Graphics/Top_Generator_1.jpg","./Graphics/Top_Generator_2.jpg"]
	splash_path = random.choice(splash_array)

	accent_array = [(78,116,16),(32,6,96)]
	accent_color = accent_array[splash_array.index(splash_path)]

	logo_path = "./Graphics/Prime2_Logo.png"
	splash_image = cv2.imread(splash_path)
	logo_image = cv2.imread(logo_path)

	splash_image = imutils.resize(splash_image,width=width)
	logo_image = imutils.resize(logo_image,width=100)
	blank_image = np.zeros((height,width,3), np.uint8)
	blank_image[0:splash_image.shape[0], 0:splash_image.shape[1]] = splash_image

	font                   = cv2.FONT_HERSHEY_SIMPLEX
	fontScale              = 0.75
	fontColor              = (255,255,255)
	lineType               = 2

	cv2.rectangle(blank_image,(25,25),(25+275,splash_image.shape[0]-25),(0,0,0),-1)
	cv2.rectangle(blank_image,(25,25),(25+275,splash_image.shape[0]-25),(255,255,255),3)

	for j in range(logo_image.shape[0]):
		for i in range(logo_image.shape[1]):
			if logo_image[j][i][0] != 0 or logo_image[j][i][1] != 0 or logo_image[j][i][2] != 0:
				blank_image[j][i+25][0] = logo_image[j][i][0]
				blank_image[j][i+25][1] = logo_image[j][i][1]
				blank_image[j][i+25][2] = logo_image[j][i][2]
		
	cv2.putText(blank_image,PLAYER, (50,100),font,2*fontScale,fontColor,lineType*2)
	y_offset = 25+splash_image.shape[0]
	#cv2.rectangle(blank_image,(0,25+y_offset),(width,65+y_offset),accent_color,-1)
	if TOURNAMENT == "All":
		tournament_info = "Lifetime Record"
		TOURNAMENT = "Lifetime_Record"
	else:
		tournament_info = "Tournament: %s" % TOURNAMENT
		sublist = ''
		for elements in TOURNAMENT:
			if elements != ' ':
				sublist += elements
			else:
				sublist += '-'
		TOURNAMENT = sublist
		
	cv2.rectangle(blank_image,(0,y_offset-25),(width,40+y_offset-25),accent_color,-1)
	cv2.putText(blank_image,tournament_info, (10,y_offset),font,fontScale,fontColor,lineType)
	y_offset += 40
	for elements in win_info:
		cv2.putText(blank_image,elements,(10,y_offset),font,fontScale,fontColor,lineType)
		y_offset += 40
	y_offset += 40
	for elements in song_info:
		if "Most" in elements:
			cv2.rectangle(blank_image,(0,y_offset-25),(width,40+y_offset-25),accent_color,-1)
			cv2.putText(blank_image,elements, (10,y_offset),font,fontScale,fontColor,lineType)
			y_offset += 40
		else:
			cv2.putText(blank_image,elements, (10,y_offset),font,fontScale,fontColor,lineType)
			y_offset += 80
	#y_offset += 40
	cv2.rectangle(blank_image,(0,y_offset-25),(width,40+y_offset-25),accent_color,-1)
	cv2.putText(blank_image,"Song Difficulties:",(10,y_offset),font,fontScale,fontColor,lineType)
	y_offset += 40
	for elements in diff_info:
		cv2.putText(blank_image,elements,(10,y_offset),font,fontScale,fontColor,lineType)
		y_offset += 40
	y_offset += 40
		
	cv2.imwrite("./Player_Cards/%s_%s.jpg" % (PLAYER,TOURNAMENT), blank_image)
	cv2.imshow("Frame",blank_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

PLAYER, TOURNAMENT,CONTINUE = Card_Information_GUI(meta_path)
if not CONTINUE:
	Generate_Player_Card(PLAYER,TOURNAMENT,meta_path)