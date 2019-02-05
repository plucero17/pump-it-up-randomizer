# Pump It Up Randomizer
Randomized card-draw system for the dance rhythm game Pump It Up

## Notes
This randomizer is currently set up for PRIME 2 2018 Version 2.05.  Some songs may be different in other releases.


## Starting the Program
 1. Before running the program, please install Python2.7 and pip-install opencv-python (Instructions in Install_Prerequisites).
 2. Configure your "./Tournament_Information/Tournament_Information.txt" folder to fit your own tournament information.
 3. Make sure your song list contains the songs, modes, and difficulties that you need for your tournament.
 4. On Windows, double-click "Randomizer.py".  On Linux, do "python Randomizer.py" from your terminal.
 
## Using the Program
 - Setting up the randomizer
   - Select your mode (Singles or Doubles) on the lower left-hand side.
   - Select your difficulty range (e.g. 13 and 18) on the bottom left-hand side.
   - Type in your player names in the lower middle section.
   - Either hit enter or click "select song" on the lower right-hand side to select a random song in your range.
 
 - Saving Results to the Tournament Log
   - When the game is over, hit the "report match" button to record scores.
   - After the popup menu appears, select the player that won and choose "continue" to save your results.
   - The tournament log file is now updated.
   
 - Resetting the Program
   - Click "clear screen" to reset the song selection and clear all settings.
   
 - Exiting the Program
   - Either hit escape or click "exit program" to stop using the randomizer.
   
## File Structure
 - Graphics
   - Contans graphic for buttons and splash screens
   
 - Install_Prerequisites
   - Contains a list of requirements needed to run this program
   
 - Song_List
   - Contains all the song mode/difficulties and the songs for each category
   
 - Tournament_Information
   - Uses the tournament name, location, and organizer information from this file and generates tournament logs
   
 - Tournament_Logs
   - Contains the history/order of matches for each tournament

## The Song List

Generating images for every difficulty for every song is hard!  Any help in keeping the song list up to date would be appreciated!

- Folder Structure
  - For each each difficulty, the folder format is "Mode_Level", where mode is 'Singles' or 'Doubles' and level is the numerical difficulty.
  - An example would be Doubles_22 or Singles_26
  
- Song Structure
  - The naming convention used for each song filename is "Name_Composer_BPM"
  - Replace spaces in the name or composer sections with dashes "-" instead
  - Only numbers,letters, and dashes are allowed in the filename
  - The file should be the image that appears when the song loads in game
  - The file should have the song name, composer, and bpm visible
  - An example would be Cleaner_Doin_203 or Love-is-a-Danger-Zone-2_Banya_162
