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

song_mode_dict = {
	"Singles":"S",
	"Doubles":"D"
	}

song_int_dict  = {
	1:"Singles",
	2:"Doubles"
	}
	
song_path   = "./Song_Directory"
log_path    = "./Tournament_Logs"
config_path = "./Tournament_Information"
def Obtain_Tournament_Information(config_path):
	Config_File = open("%s/Tournament_Information.txt" % config_path,'r')
	
	tournament_name     = 'Default Tournament Name'
	tournament_location = 'Location Unknown'
	tournament_organize = 'No Organizer'
	
	for lines in Config_File:
		if lines.split(":")[0] == "Tournament Name":
			tournament_name = lines.split(":")[1].strip(" ").strip("\n")
		elif lines.split(":")[0] == "Tournament Location":
			tournament_location = lines.split(":")[1].strip(" ").strip("\n")
		elif lines.split(":")[0] == "Tournament Organizer":
			tournament_organizer = lines.split(":")[1].strip(" ").strip("\n")
			
	return tournament_name,tournament_location,tournament_organizer

def Create_Log_File(tournament_name,tournament_location,tournament_organizer):
	Converted_Name_Array = tournament_name.split(" ")
	
	converted_name = ""
	for words in Converted_Name_Array:
		converted_name = converted_name + words + "-"
	clean_tournament_name = converted_name[:-1] + ".txt"
	
	file_path = "%s/%s" % (log_path, clean_tournament_name)
	Tournament_File = open(file_path,'a+')
	
	if os.path.getsize(file_path) == 0:
		Tournament_File.write("Tournament Name: %s\n" % tournament_name)
		Tournament_File.write("Tournament Location: %s\n" % tournament_location)
		Tournament_File.write("Tournament Organizer: %s\n" % tournament_organizer)
		Tournament_File.write("Date Created: %s\n\n\n" % str(date.today()))
		
		Tournament_File.write("======================\n")
		Tournament_File.write("List of Matches Played\n")
		Tournament_File.write("======================\n\n\n")
		
	return Tournament_File
	
def Show_GUI():
	
	class Selector_Screen:
		min_diff     = -1
		max_diff     = -1
		diff_mode    = "none"
		bad_exit     = True
		current_song = "none"
		current_diff = "none"
		report_mode  = False
		match_winner = "none"
		player_array = ['none','none']
		
		def Exit_Program(self,event='<Button-1>'):
			Selector_Screen.bad_exit = False
			self.master.destroy()

		def Reset_Song(self,event='<Button-1>'):
			Selector_Screen.min_diff     = -1
			Selector_Screen.max_diff     = -1
			Selector_Screen.diff_mode    = "none"
			Selector_Screen.current_song = "none"
			Selector_Screen.current_diff = "none"
			Selector_Screen.report_mode  = False
			Selector_Screen.match_winner = "none"
			Selector_Screen.player_array = ['none','none']
			
			self.Game_Mode.set(0)
			self.Min_Difficulty.delete(0,END)
			self.Max_Difficulty.delete(0,END)
			self.Player_One_Entry.delete(0,END)
			self.Player_Two_Entry.delete(0,END)
			self.Selected_Song['image'] = self.Main_Menu
			
			self.Min_Difficulty.update()
			self.Max_Difficulty.update()
			self.Selected_Song.update()

		def Prompt_Winner(self,parent):
		
			def return_value(event='<Button-1>'):
				if winner.get() != 0:
					if winner.get() != 3:
						Selector_Screen.match_winner = Selector_Screen.player_array[winner.get() - 1]
					else:
						Selector_Screen.match_winner = "Draw"
					self.win.destroy()
					
			self.win = Toplevel(parent)
			self.win.wm_title("Select Winner")
			
			width = 360
			height = 320
			screen_width = self.win.winfo_screenwidth()
			screen_height = self.win.winfo_screenheight()
			x = (screen_width/2) - (width/2)
			y = (screen_height/2) - (height/2)
			self.win.geometry('%dx%d+%d+%d' % (width, height, x, y))
			
			self.Continue = Tkinter.PhotoImage(file="./Graphics/Continue.gif")
			self.Cancel   = Tkinter.PhotoImage(file="./Graphics/Cancel.gif")
			winner = IntVar()
			winner.set(0)
			
			self.Inner_Frame = Frame(self.win)
			self.Inner_Frame.grid(row=0,column=0)
			
			Winner_Label = Label(self.Inner_Frame, text="The winner is:")
			Winner_Label.grid(row=0, column=0,columnspan=2)
			Winner_Label.configure(font=("TkDefaultFont",24))

			self.Player_One__Winner = Radiobutton(self.Inner_Frame, text=Selector_Screen.player_array[0], variable=winner, value=1)
			self.Player_Two__Winner = Radiobutton(self.Inner_Frame, text=Selector_Screen.player_array[1], variable=winner, value=2)
			self.Draw = Radiobutton(self.Inner_Frame, text="Draw", variable=winner, value=3)
			self.Player_One__Winner.grid(row=1,column=0,pady=(25,25))
			self.Player_Two__Winner.grid(row=1,column=1,pady=(25,25))
			self.Draw.grid(row=2,column=0,pady=(0,25),columnspan=2)
			self.Player_One__Winner.configure(font=("TkDefaultFont",24))
			self.Player_Two__Winner.configure(font=("TkDefaultFont",24))
			self.Draw.configure(font=("TkDefaultFont",24))
			
			Select_Button = Button(self.Inner_Frame, image=self.Continue, command=return_value)
			Select_Button.grid(row=3, column=0)
			Cancel_Button = Button(self.Inner_Frame, image=self.Cancel, command=self.win.destroy)
			Cancel_Button.grid(row=3, column=1)
			
		def Report_Match(self,event='<Button-1'):
			
			if not Selector_Screen.report_mode:
				return
				
			time_of_match = str(datetime.datetime.now().time()).split(".")[0]
			self.Prompt_Winner(self.master)
			self.master.wait_window(self.win)
			
			name_list = ""
			time_array = time_of_match.split(":")
			if int(time_array[0]) > 12:
				time_of_match = "%s:%s PM" % (str(int(time_array[0]) - 12), time_array[1])
			elif int(time_array[0]) < 12 and int(time_array[0]) != 0:
				time_of_match = "%s:%s AM" % (time_array[0], time_array[1])
			elif int(time_array[0]) == 12:
				time_of_match = "%s:%s PM" % (time_array[0], time_array[1])
			elif int(time_array[0]) == 0:
				time_of_match = "%s:%s AM" % (str(int(time_array[0]) + 12), time_array[1])
				
			for names in Selector_Screen.player_array:
				name_list = name_list + names + ", "
			name_list = name_list[:-2]
			
			Tournament_Log.write("Song: %s %s\n" % (Selector_Screen.current_song,Selector_Screen.current_diff))
			Tournament_Log.write("Players: %s\n" % (name_list))
			Tournament_Log.write("Winner: %s\n" % (Selector_Screen.match_winner))
			Tournament_Log.write("Time of Match: %s\n\n" % (time_of_match))
			
			Selector_Screen.current_song = "none"
			Selector_Screen.current_diff = "none"
			Selector_Screen.player_array = ['none','none']
			
			self.Player_One_Entry.delete(0,END)
			self.Player_Two_Entry.delete(0,END)
			self.Selected_Song['image'] = self.Main_Menu
			Selector_Screen.report_mode = False
			
			self.Player_One_Entry.update()
			self.Player_Two_Entry.update()
			self.Selected_Song.update()
			
		def Select_Song(self,event='<Button-1>'):
			
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
			
			min_difficulty  = Selector_Screen.min_diff
			max_difficulty  = Selector_Screen.max_diff
			difficulty_mode = Selector_Screen.diff_mode
			difficulty_level = randint(min_difficulty,max_difficulty)
			
			for difficulties in os.listdir(song_path):
				
				target_mode  = difficulties.split("_")[0]
				target_level = int(difficulties.split("_")[1])
				
				if target_mode == difficulty_mode and  target_level == difficulty_level:
				
					target_path = "%s/%s/" % (song_path,difficulties)
					total_songs = len(os.listdir(target_path))
					target_song_index = randint(0,total_songs - 1)
					
					target_song_path = sorted(glob.glob(target_path + "*.JPG"))[target_song_index]
					
					song_information = ((os.path.basename(target_song_path)).split(".")[0]).split("_")
					song_name_information = song_information[0].split("-")
					
					song_name = ""
					for words in song_name_information:
						song_name = song_name + words + " "
					
					song_name = song_name[:-1]
					#print song_name
					song_composer = song_information[1]
					song_bpm      = song_information[2]
					
					song_mode       = song_mode_dict[target_mode]
					song_difficulty = target_level
					
					song_image = cv2.imread(target_song_path)
					song_image = cv2.resize(song_image, (1280,720))
					
					x_offset = 120
					y_offset = 120
					
					if song_mode == "S":
						song_color = (0,100,230)
					elif song_mode == "D":
						song_color = (0,230,0)
					
					cv2.circle(song_image,(15+x_offset,720-y_offset-15), min(x_offset,y_offset), song_color, -1)
					cv2.circle(song_image,(15+x_offset,720-y_offset-15), min(x_offset,y_offset), (128,128,128), 3)
					cv2.putText(song_image,"%s%d" % (song_mode,song_difficulty),(15+(x_offset/4),720-(y_offset)+(y_offset/4)-15),cv2.FONT_HERSHEY_SIMPLEX,3,(255,255,255),5)
					
					img_color = cv2.cvtColor(song_image, cv2.COLOR_BGR2RGB)
					img_array = Img.fromarray(img_color)
					self.tk_photo  = ImageTk.PhotoImage(img_array)
					
					Selector_Screen.current_song = song_name
					Selector_Screen.current_diff = "%s%s" % (song_mode,song_difficulty)
					Selector_Screen.report_mode  = True
					
					self.Selected_Song['image'] = self.tk_photo
					self.Selected_Song.update()

					#cv2.imshow("Next Song: %s %s%d by %s.  BPM: %s" % (song_name, song_mode, song_difficulty, song_composer, song_bpm),song_image)
					#cv2.waitKey(0)
					#cv2.destroyAllWindows()
				
		def __init__(self,master):
			self.master = master
			self.master.resizable(0,0)
			master.title('Pump It Up Randomizer')
			
			width = 1280+5
			height = 1080
			
			screen_width = self.master.winfo_screenwidth()
			screen_height = self.master.winfo_screenheight()
			x = (screen_width/2) - (width/2)
			y = (screen_height/2) - (height/2)
			self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

			self.Game_Mode = IntVar()

			if os.name == 'nt':
				self.master.iconbitmap("./Graphics/icon.ico")
				
			self.File_Options = Tkinter.Frame(self.master, height=25)
			self.File_Options.grid(row=0,column=0)
			
			self.Main_Menu = Tkinter.PhotoImage(file="./Graphics/Main_Menu.gif")
			self.Start = Tkinter.PhotoImage(file="./Graphics/Select_Song.gif")
			self.Report = Tkinter.PhotoImage(file="./Graphics/Report_Match.gif")
			self.Clear = Tkinter.PhotoImage(file="./Graphics/Clear_Screen.gif")
			self.Exit = Tkinter.PhotoImage(file="./Graphics/Exit_Program.gif")
			
			self.Selected_Song = Tkinter.Label(self.master, image=self.Main_Menu)
			self.Selected_Song.grid(row=1,column=0)

			self.Button_Frame = Tkinter.Frame(self.master, height=90)
			self.Button_Frame.grid(row=2,column=0)
			
			self.Randomizer_Options = Tkinter.Frame(self.Button_Frame, height=90)
			self.Randomizer_Options.grid(row=0,column=0,pady=(25,25),sticky=N)
			
			self.Game_Mode_Explanation = Tkinter.Label(self.Randomizer_Options, text="Game Mode")
			self.Game_Mode_Explanation.grid(row=0,column=0,columnspan=4,sticky=N)
			self.Game_Mode_Explanation.configure(font=("TkDefaultFont",20))
			
			self.Singles_Radio = Radiobutton(self.Randomizer_Options, text="Singles", variable=self.Game_Mode, value=1)
			self.Doubles_Radio = Radiobutton(self.Randomizer_Options, text="Doubles", variable=self.Game_Mode, value=2)
			self.Singles_Radio.grid(row=1,column=0,columnspan=2)
			self.Doubles_Radio.grid(row=1,column=2,columnspan=2)
			self.Singles_Radio.configure(font=("TkDefaultFont",16))
			self.Doubles_Radio.configure(font=("TkDefaultFont",16))
			
			self.diff_padding = Tkinter.Label(self.Randomizer_Options, text=" ")
			self.diff_padding.grid(row=2,column=0,columnspan=4)
			self.diff_padding.configure(font=("TkDefaultFont",12))
			
			self.Difficulty_Explanation = Tkinter.Label(self.Randomizer_Options, text="Difficulty")
			self.Difficulty_Explanation.grid(row=3,column=0,columnspan=4)
			self.Difficulty_Explanation.configure(font=("TkDefaultFont",20))
			(Tkinter.Label(self.Randomizer_Options, text="Between ",font=("TkDefaultFont",16))).grid(row=4,column=0)
			(Tkinter.Label(self.Randomizer_Options, text=" and ",font=("TkDefaultFont",16))).grid(row=4,column=2)
			
			self.Min_Difficulty = Tkinter.Entry(self.Randomizer_Options,width=4)
			self.Min_Difficulty.grid(row=4,column = 1)
			self.Min_Difficulty.configure(font=("TkDefaultFont",16))
			
			self.Max_Difficulty = Tkinter.Entry(self.Randomizer_Options,width=4)
			self.Max_Difficulty.grid(row=4,column = 3)
			self.Max_Difficulty.configure(font=("TkDefaultFont",16))
			
			self.Player_Frame = Tkinter.Frame(self.Button_Frame, height=90)
			self.Player_Frame.grid(row=0,column=1,pady=(25,25),padx=(125,125),sticky=N)
			
			self.Player_Explanation = Tkinter.Label(self.Player_Frame, text="Players")
			self.Player_Explanation.grid(row=0,column=0,columnspan=2,sticky=N)
			self.Player_Explanation.configure(font=("TkDefaultFont",20))
			
			self.Player_One_Label = Tkinter.Label(self.Player_Frame, text="Player 1: ")
			self.Player_One_Label.grid(row=1,column=0)
			self.Player_One_Label.configure(font=("TkDefaultFont",16))
			self.Player_One_Entry = Tkinter.Entry(self.Player_Frame,width=15)
			self.Player_One_Entry.grid(row=1,column=1)
			self.Player_One_Entry.configure(font=("TkDefaultFont",16))
			
			self.Player_Two_Label = Tkinter.Label(self.Player_Frame, text="Player 2: ")
			self.Player_Two_Label.grid(row=2,column=0)
			self.Player_Two_Label.configure(font=("TkDefaultFont",16))
			self.Player_Two_Entry = Tkinter.Entry(self.Player_Frame,width=15)
			self.Player_Two_Entry.grid(row=2,column=1)
			self.Player_Two_Entry.configure(font=("TkDefaultFont",16))
			
			self.Command_Options = Tkinter.Frame(self.Button_Frame, height=90)
			self.Command_Options.grid(row=0,column=2,pady=(25,25))
			
			self.Start_Button = Tkinter.Button(self.Command_Options, image=self.Start, command=self.Select_Song)
			self.Start_Button.grid(row=0,column=0,sticky=W+E+N+S)
			
			self.Start_Button = Tkinter.Button(self.Command_Options, image=self.Report, command=self.Report_Match)
			self.Start_Button.grid(row=0,column=1,sticky=W+E+N+S)

			self.Reset_Button = Tkinter.Button(self.Command_Options, image=self.Clear, command=self.Reset_Song)
			self.Reset_Button.grid(row=1,column=0,sticky=W+E+N+S)
			
			self.Exit_Button = Tkinter.Button(self.Command_Options, image=self.Exit, command=self.Exit_Program)
			self.Exit_Button.grid(row=1,column=1,sticky=W+E+N+S)
			
			self.master.bind("<Return>", self.Select_Song)
			self.master.bind("<Escape>", self.Exit_Program)
		
	Select_Root = Tkinter.Tk()
	Select_Window = Selector_Screen(Select_Root)
	Select_Root.mainloop()
	
	min_difficulty   = Selector_Screen.min_diff
	max_difficulty   = Selector_Screen.max_diff
	difficulty_mode  = Selector_Screen.diff_mode
	continue_program = not Selector_Screen.bad_exit
	
tournament_name,tournament_location,tournament_organizer = Obtain_Tournament_Information(config_path)
Tournament_Log = Create_Log_File(tournament_name,tournament_location,tournament_organizer)
Show_GUI()	

Tournament_Log.close()