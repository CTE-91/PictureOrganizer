# PictureOrganizer
-------------------------------------Picture Organizer-------------------------------------
This is a Picture/Video organizer with simple UI which will sort picture and video files 
into appropriate folders based on when they were created or modified - whichever date is 
older. You can input a source directory and destination directory for where you want them 
organized. You can also just organize a single directory by inputting the same directory as 
the source and destination in the UI.

Features:
- Sorts files based on their extensions (Image, Video, Misc).
- Creates folders based on extensions (Image, Video, Misc).
    - Any file without a image/video extension goes into Misc directory.
- Creates folders by year, then by month (Only if files acutally exist for those dates).
- Moves files into appropriate folders.
- Deletes empty folders in source and destination directory.
- If files exist in destination already, script sorts them first.
- if a duplicate exists in destination from source, file move is skipped.

UI:
- Source and distination selection (Browse or type manually).
- Progress bar (Exciting, I know).

About me:
This is my first project not following a tutorial. I relied heavily on chatGPT as a 
personal tutor so any notes on improvement/best practices are appreciated. I developed
this project to sort the massive amount of picture and video files I've downloaded 
from my phone over the years. I found it annoying that the iPhone stores two files for
live images (A short video, and an actual image), which is why I wanted it to sort video
files too. 
