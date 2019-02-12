# import modules
import cv2
import glob
import os
import datetime
from datetime import date
from PIL import Image as Img
from PIL import ImageTk
from random import randint
from Tkinter import *
import Tkinter,tkFileDialog, tkMessageBox

# setting dictionaries and keys for fast conversions
song_mode_dict = {
	"Singles":"S",
	"Doubles":"D"
	}

song_int_dict  = {
	1:"Singles",
	2:"Doubles"
	}
	

# global values
song_path   = "./Song_Directory"
log_path    = "./Tournament_Logs"
config_path = "./Tournament_Information"

# reads config file and returns tournament name, location, and organizer
def Obtain_Tournament_Information(config_path):

	# open file for reading
	Config_File = open("%s/Tournament_Information.txt" % config_path,'r')
	
	# initialized values if not found
	tournament_name     = 'Default Tournament Name'
	tournament_location = 'Location Unknown'
	tournament_organize = 'No Organizer'
	
	# goes through config file looking for sections
	for lines in Config_File:
		if lines.split(":")[0] == "Tournament Name":
			tournament_name = lines.split(":")[1].strip(" ").strip("\n")
		elif lines.split(":")[0] == "Tournament Location":
			tournament_location = lines.split(":")[1].strip(" ").strip("\n")
		elif lines.split(":")[0] == "Tournament Organizer":
			tournament_organizer = lines.split(":")[1].strip(" ").strip("\n")
			
	# returns tournament name, location, and organizer
	return tournament_name,tournament_location,tournament_organizer

# generates the log file if it does not exist, or opens if it does
def Create_Log_File(tournament_name,tournament_location,tournament_organizer):

	# changing name from space format to dash format for file naming
	converted_name = ""
	Converted_Name_Array = tournament_name.split(" ")
	for words in Converted_Name_Array:
		converted_name = converted_name + words + "-"
	clean_tournament_name = converted_name[:-1] + ".txt"
	
	# searches for tournament log file and creates/opens it
	file_path = "%s/%s" % (log_path, clean_tournament_name)
	Tournament_File = open(file_path,'a+')
	meta_path = "%s/%s" % (log_path, "Meta_Information.csv")
	Meta_File = open(meta_path, 'a+')
	
	# if the file was just created, generate tournament metadata
	if os.path.getsize(file_path) == 0:
		Tournament_File.write("Tournament Name: %s\n" % tournament_name)
		Tournament_File.write("Tournament Location: %s\n" % tournament_location)
		Tournament_File.write("Tournament Organizer: %s\n" % tournament_organizer)
		Tournament_File.write("Date Created: %s\n\n\n" % str(date.today()))
		
		Tournament_File.write("======================\n")
		Tournament_File.write("List of Matches Played\n")
		Tournament_File.write("======================\n\n\n")
		
	# return the opened file
	return Tournament_File, Meta_File
	
# the main script and gui.  contains randomizer and score recording scripts
def Show_GUI():
	
	# randomizer gui class
	class Selector_Screen:
	
		# initialized randomizer constraints
		min_diff     = -1
		max_diff     = -1
		diff_mode    = "none"
		
		# error handling
		bad_exit     = True
		
		# initialized recording constraints
		current_song = "none"
		current_diff = "none"
		report_mode  = False
		match_winner = "none"
		player_array = ['none','none']
		
		# exits the program safely
		def Exit_Program(self,event='<Button-1>'):
			Selector_Screen.bad_exit = False
			self.master.destroy()

		# clears the menu and refreashes splash image
		def Reset_Song(self,event='<Button-1>'):
		
			# clears randomizer constraints
			Selector_Screen.min_diff     = -1
			Selector_Screen.max_diff     = -1
			Selector_Screen.diff_mode    = "none"
			
			# clears recording constraints
			Selector_Screen.current_song = "none"
			Selector_Screen.current_diff = "none"
			Selector_Screen.report_mode  = False
			Selector_Screen.match_winner = "none"
			Selector_Screen.player_array = ['none','none']
			
			# clears entry boxes and radio buttons
			self.Game_Mode.set(0)
			self.Min_Difficulty.delete(0,END)
			self.Max_Difficulty.delete(0,END)
			self.Player_One_Entry.delete(0,END)
			self.Player_Two_Entry.delete(0,END)
			self.Selected_Song['image'] = self.Main_Menu
			
			# refreshes entry boxes and splash image
			self.Min_Difficulty.update()
			self.Max_Difficulty.update()
			self.Selected_Song.update()

		# popup asking and returning the winner of the match
		def Prompt_Winner(self,parent):
		
			# button function: saves winner to class variable and closes popup
			def return_value(event='<Button-1>'):
			
				# if button is selected
				if winner.get() != 0:
				
					# if not a draw
					if winner.get() != 3:
						Selector_Screen.match_winner = Selector_Screen.player_array[winner.get() - 1]
						
					# if a draw
					else:
						Selector_Screen.match_winner = "Draw"
						
					# close popup
					self.win.destroy()
			
			# creates popop window
			self.win = Toplevel(parent)
			self.win.wm_title("Select Winner")
			
			# button images
			self.Continue = Tkinter.PhotoImage(file="./Graphics/Continue.gif")
			self.Cancel   = Tkinter.PhotoImage(file="./Graphics/Cancel.gif")
			
			# initialize winner radio button variable
			winner = IntVar()
			winner.set(0)
			
			# construct frame for widgets
			self.Inner_Frame = Frame(self.win)
			self.Inner_Frame.grid(row=0,column=0)
			
			# asks who the winner is
			Winner_Label = Label(self.Inner_Frame, text="The winner is:")
			Winner_Label.grid(row=0, column=0,columnspan=2)
			Winner_Label.configure(font=("TkDefaultFont",24))

			# player one, two, and draw radio buttons
			self.Player_One__Winner = Radiobutton(self.Inner_Frame, text=Selector_Screen.player_array[0], variable=winner, value=1)
			self.Player_Two__Winner = Radiobutton(self.Inner_Frame, text=Selector_Screen.player_array[1], variable=winner, value=2)
			self.Draw = Radiobutton(self.Inner_Frame, text="Draw", variable=winner, value=3)
			
			# places radio buttons
			self.Player_One__Winner.grid(row=1,column=0,pady=(25,25))
			self.Player_Two__Winner.grid(row=1,column=1,pady=(25,25))
			self.Draw.grid(row=2,column=0,pady=(0,25),columnspan=2)
			
			# configures radio button fonts
			self.Player_One__Winner.configure(font=("TkDefaultFont",24))
			self.Player_Two__Winner.configure(font=("TkDefaultFont",24))
			self.Draw.configure(font=("TkDefaultFont",24))
			
			# creates and places continue button
			Select_Button = Button(self.Inner_Frame, image=self.Continue, command=return_value)
			Select_Button.grid(row=3, column=0)
			
			# creates and places cancel button
			Cancel_Button = Button(self.Inner_Frame, image=self.Cancel, command=self.win.destroy)
			Cancel_Button.grid(row=3, column=1)
			
		# asks for winner and saves match information in tournament log file
		def Report_Match(self,event='<Button-1'):
			
			# if there isn't a song selected, do nothing
			if not Selector_Screen.report_mode:
				return
				
			# initialize the time of the match
			time_of_match = str(datetime.datetime.now().time()).split(".")[0]
			
			# ask for the winner
			self.Prompt_Winner(self.master)
			self.master.wait_window(self.win)

			# initialize list of players
			name_list = ""
			
			# convert the time of day into 12 hour format
			time_array = time_of_match.split(":")
			if int(time_array[0]) > 12:
				time_of_match = "%s:%s PM" % (str(int(time_array[0]) - 12), time_array[1])
			elif int(time_array[0]) < 12 and int(time_array[0]) != 0:
				time_of_match = "%s:%s AM" % (time_array[0], time_array[1])
			elif int(time_array[0]) == 12:
				time_of_match = "%s:%s PM" % (time_array[0], time_array[1])
			elif int(time_array[0]) == 0:
				time_of_match = "%s:%s AM" % (str(int(time_array[0]) + 12), time_array[1])
				
			# save list of players
			for names in Selector_Screen.player_array:
				name_list = name_list + names + ", "
			name_list = name_list[:-2]
			
			# writes the song played, who played the song, who one the match, and when the match was
			Tournament_Log.write("Song: %s %s\n" % (Selector_Screen.current_song,Selector_Screen.current_diff))
			Tournament_Log.write("Players: %s\n" % (name_list))
			Tournament_Log.write("Winner: %s\n" % (Selector_Screen.match_winner))
			Tournament_Log.write("Time of Match: %s\n\n" % (time_of_match))
			
			# writes results to meta file for long-term statistics
			Meta_Log.write("%s,%s,%s,%s,%s,%s,\n" % ( 
				Selector_Screen.current_song, 
				Selector_Screen.diff_mode, 
				Selector_Screen.current_diff[1:], 
				tournament_name,
				Selector_Screen.match_winner,
				name_list
				)
			)
			
			# resets song
			Selector_Screen.current_song = "none"
			Selector_Screen.current_diff = "none"
			Selector_Screen.report_mode = False
			self.Selected_Song['image'] = self.Main_Menu
			
			# resets players
			self.Player_One_Entry.delete(0,END)
			self.Player_Two_Entry.delete(0,END)
			Selector_Screen.player_array = ['none','none']


			# refreshes entry boxes and splash screen
			self.Player_One_Entry.update()
			self.Player_Two_Entry.update()
			self.Selected_Song.update()
			
		# randomly selects song in range and displays on the screen
		def Select_Song(self,event='<Button-1>'):
			
			# check for required values before continuing
			if self.Min_Difficulty.get() != "" and self.Min_Difficulty.get().isdigit():
				Selector_Screen.min_diff = int(self.Min_Difficulty.get())
			else:
				return
			if self.Max_Difficulty.get() != "" and self.Max_Difficulty.get().isdigit():
				Selector_Screen.max_diff = int(self.Max_Difficulty.get())
			else:
				return
			if self.Game_Mode.get() != 0:
				Selector_Screen.diff_mode = song_int_dict[self.Game_Mode.get()]
			else:
				return
			if self.Player_One_Entry.get() != "" and self.Player_Two_Entry.get() != "":
				Selector_Screen.player_array = [self.Player_One_Entry.get(),self.Player_Two_Entry.get()]
			
			#call required parameters from class variables
			min_difficulty  = Selector_Screen.min_diff
			max_difficulty  = Selector_Screen.max_diff
			difficulty_mode = Selector_Screen.diff_mode
			difficulty_level = randint(min_difficulty,max_difficulty)
			
			# cycles through the difficulties to look for the correct mode and level
			for difficulties in os.listdir(song_path):
				
				# singles/doubles and #1-26
				target_mode  = difficulties.split("_")[0]
				target_level = int(difficulties.split("_")[1])
				
				# if there's a match, search foro a song at random
				if target_mode == difficulty_mode and  target_level == difficulty_level:
				
					# save path to mode_level folder
					target_path = "%s/%s/" % (song_path,difficulties)
					total_songs = len(os.listdir(target_path))
					
					#choose a random song in the folder
					target_song_index = randint(0,total_songs - 1)
					target_song_path = sorted(glob.glob(target_path + "*.JPG"))[target_song_index]
					
					# retrieve information from the song filename
					song_information = ((os.path.basename(target_song_path)).split(".")[0]).split("_")
					
					# convert song name from dash to space format
					song_name = ""
					song_name_information = song_information[0].split("-")
					for words in song_name_information:
						song_name = song_name + words + " "
					song_name = song_name[:-1]
					
					# retrieve song composer and bpm
					song_composer = song_information[1]
					song_bpm      = song_information[2]
					
					# retrieve song mode and difficulty
					song_mode       = song_mode_dict[target_mode]
					song_difficulty = target_level
					
					# retrieve song image from path
					song_image = cv2.imread(target_song_path)
					song_image = cv2.resize(song_image, (1280,720))
					
					# offset values for difficulty circle
					x_offset = 120
					y_offset = 120
					
					# changes color for singles or doubles
					if song_mode == "S":
						song_color = (0,100,230)
					elif song_mode == "D":
						song_color = (0,230,0)
					
					# draws circle and writes song mode and level
					cv2.circle(song_image,(15+x_offset,720-y_offset-15), min(x_offset,y_offset), song_color, -1)
					cv2.circle(song_image,(15+x_offset,720-y_offset-15), min(x_offset,y_offset), (128,128,128), 3)
					cv2.putText(song_image,"%s%d" % (song_mode,song_difficulty),(15+(x_offset/4),720-(y_offset)+(y_offset/4)-15),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),5)
					
					# converts the color space from BGR to RGB and allows import into tKinter from OpenCV
					img_color = cv2.cvtColor(song_image, cv2.COLOR_BGR2RGB)
					img_array = Img.fromarray(img_color)
					self.tk_photo  = ImageTk.PhotoImage(img_array)
					
					# saves song name, difficulty, and allows scores to be reported
					Selector_Screen.current_song = song_name
					Selector_Screen.current_diff = "%s%s" % (song_mode,song_difficulty)
					Selector_Screen.report_mode  = True
					
					# update splash image
					self.Selected_Song['image'] = self.tk_photo
					self.Selected_Song.update()
		
		# runs when the program starts.  constructs entire gui
		def __init__(self,master):
		
			# configure master window
			self.master = master
			self.master.resizable(0,0)
			master.title('Pump It Up Randomizer')
			
			# creates icon in top left corner
			if os.name == 'nt':
				self.master.iconbitmap("./Graphics/icon.ico")

			# initialize Singles/Doubles variable
			self.Game_Mode = IntVar()

			# TODO: Create file options at top for full gui support
			# blank bar at top for "file, edit, view, help" setings
			self.File_Options = Tkinter.Frame(self.master, height=25)
			self.File_Options.grid(row=0,column=0)
			
			# Images for buttons and splash screen
			self.Main_Menu = Tkinter.PhotoImage(file="./Graphics/Main_Menu.gif")
			self.Start = Tkinter.PhotoImage(file="./Graphics/Select_Song.gif")
			self.Report = Tkinter.PhotoImage(file="./Graphics/Report_Match.gif")
			self.Clear = Tkinter.PhotoImage(file="./Graphics/Clear_Screen.gif")
			self.Exit = Tkinter.PhotoImage(file="./Graphics/Exit_Program.gif")
			
			# splash screen image
			self.Selected_Song = Tkinter.Label(self.master, image=self.Main_Menu)
			self.Selected_Song.grid(row=1,column=0)

			# Contains all buttons and widgets
			self.Button_Frame = Tkinter.Frame(self.master, height=90)
			self.Button_Frame.grid(row=2,column=0)
			
			# Options for game mode and difficulty range
			self.Randomizer_Options = Tkinter.Frame(self.Button_Frame, height=90)
			self.Randomizer_Options.grid(row=0,column=0,pady=(25,25),sticky=N)
			
			# Explains choices of singles or doubles
			self.Game_Mode_Explanation = Tkinter.Label(self.Randomizer_Options, text="Game Mode")
			self.Game_Mode_Explanation.grid(row=0,column=0,columnspan=4,sticky=N)
			self.Game_Mode_Explanation.configure(font=("TkDefaultFont",20))
			
			# create singles/doubles radio buttons, place them in the frame, and change font size
			self.Singles_Radio = Radiobutton(self.Randomizer_Options, text="Singles", variable=self.Game_Mode, value=1)
			self.Doubles_Radio = Radiobutton(self.Randomizer_Options, text="Doubles", variable=self.Game_Mode, value=2)
			self.Singles_Radio.grid(row=1,column=0,columnspan=2)
			self.Doubles_Radio.grid(row=1,column=2,columnspan=2)
			self.Singles_Radio.configure(font=("TkDefaultFont",16))
			self.Doubles_Radio.configure(font=("TkDefaultFont",16))
			
			# padding layer in randomizer frame
			self.diff_padding = Tkinter.Label(self.Randomizer_Options, text=" ")
			self.diff_padding.grid(row=2,column=0,columnspan=4)
			self.diff_padding.configure(font=("TkDefaultFont",12))
			
			# Explains potential difficulty range
			self.Difficulty_Explanation = Tkinter.Label(self.Randomizer_Options, text="Difficulty")
			self.Difficulty_Explanation.grid(row=3,column=0,columnspan=4)
			self.Difficulty_Explanation.configure(font=("TkDefaultFont",20))
			
			# Text labels for GUI fluff
			(Tkinter.Label(self.Randomizer_Options, text="Between ",font=("TkDefaultFont",16))).grid(row=4,column=0)
			(Tkinter.Label(self.Randomizer_Options, text=" and ",font=("TkDefaultFont",16))).grid(row=4,column=2)
			
			# Minimum value for randomizing
			self.Min_Difficulty = Tkinter.Entry(self.Randomizer_Options,width=4)
			self.Min_Difficulty.grid(row=4,column = 1)
			self.Min_Difficulty.configure(font=("TkDefaultFont",16))
			
			# Maximum value for randomizing
			self.Max_Difficulty = Tkinter.Entry(self.Randomizer_Options,width=4)
			self.Max_Difficulty.grid(row=4,column = 3)
			self.Max_Difficulty.configure(font=("TkDefaultFont",16))
			
			# Fill in player 1 and player 2 names
			self.Player_Frame = Tkinter.Frame(self.Button_Frame, height=90)
			self.Player_Frame.grid(row=0,column=1,pady=(25,25),padx=(125,125),sticky=N)
			
			# Explains the player section
			self.Player_Explanation = Tkinter.Label(self.Player_Frame, text="Players")
			self.Player_Explanation.grid(row=0,column=0,columnspan=2,sticky=N)
			self.Player_Explanation.configure(font=("TkDefaultFont",20))
			
			# create player1 entry box, place them in the frame, and change font size
			self.Player_One_Label = Tkinter.Label(self.Player_Frame, text="Player 1: ")
			self.Player_One_Label.grid(row=1,column=0)
			self.Player_One_Label.configure(font=("TkDefaultFont",16))
			self.Player_One_Entry = Tkinter.Entry(self.Player_Frame,width=15)
			self.Player_One_Entry.grid(row=1,column=1)
			self.Player_One_Entry.configure(font=("TkDefaultFont",16))
			
			# create player2 entry box, place them in the frame, and change font size
			self.Player_Two_Label = Tkinter.Label(self.Player_Frame, text="Player 2: ")
			self.Player_Two_Label.grid(row=2,column=0)
			self.Player_Two_Label.configure(font=("TkDefaultFont",16))
			self.Player_Two_Entry = Tkinter.Entry(self.Player_Frame,width=15)
			self.Player_Two_Entry.grid(row=2,column=1)
			self.Player_Two_Entry.configure(font=("TkDefaultFont",16))
			
			# important buttons
			self.Command_Options = Tkinter.Frame(self.Button_Frame, height=90)
			self.Command_Options.grid(row=0,column=2,pady=(25,25))
			
			# starts randomizer
			self.Start_Button = Tkinter.Button(self.Command_Options, image=self.Start, command=self.Select_Song)
			self.Start_Button.grid(row=0,column=0,sticky=W+E+N+S)
			
			# records match results
			self.Start_Button = Tkinter.Button(self.Command_Options, image=self.Report, command=self.Report_Match)
			self.Start_Button.grid(row=0,column=1,sticky=W+E+N+S)

			# clears screen
			self.Reset_Button = Tkinter.Button(self.Command_Options, image=self.Clear, command=self.Reset_Song)
			self.Reset_Button.grid(row=1,column=0,sticky=W+E+N+S)
			
			# exits program
			self.Exit_Button = Tkinter.Button(self.Command_Options, image=self.Exit, command=self.Exit_Program)
			self.Exit_Button.grid(row=1,column=1,sticky=W+E+N+S)
			
			# hotkeys
			self.master.bind("<Return>", self.Select_Song)
			self.master.bind("<Escape>", self.Exit_Program)
	
	# starts GUI
	Select_Root = Tkinter.Tk()
	Select_Window = Selector_Screen(Select_Root)
	Select_Root.mainloop()
	
# read config file, pass information to tournament log, and start randomizer GUI
tournament_name,tournament_location,tournament_organizer = Obtain_Tournament_Information(config_path)
Tournament_Log, Meta_Log = Create_Log_File(tournament_name,tournament_location,tournament_organizer)
Show_GUI()	

# close tournament log file
Tournament_Log.close()