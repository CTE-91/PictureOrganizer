from os import walk, makedirs, rmdir, listdir, chmod, path
from os.path import exists
from time import localtime, strftime
from shutil import move
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import stat


class PictureOrganizerApp:
    
    # Image file extensions
    IMAGE_EXTENSIONS = [
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif",
    ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic",
    ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", 
    ".ai", ".eps", ".ico"]

    # Video file extensions
    VIDEO_EXTENSIONS = [
    ".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v",
    ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

    # Initiation
    def __init__(self, root):                   
        self.root = root                            
        self.root.title("Picture Organizer")        #Sets window title

        self.source_var = tk.StringVar()            #intializes source_var variable for tk.entry field   
        self.dest_var = tk.StringVar()              #intializes dest_var variable for tk.entry field

        self.setup_ui()                             #call method to setup UI

    #UI design
    def setup_ui(self):
        tk.Label(self.root, text="Please select where your pictures are and where you want them to be organized") \
            .grid(row=0, column=0, columnspan=3, padx=10, pady=20)

        tk.Label(self.root, text="Source Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(self.root, textvariable=self.source_var, width=50).grid(row=1, column=1, padx=5)
        tk.Button(self.root, text="Browse", command=self.select_source).grid(row=1, column=2, padx=10)

        tk.Label(self.root, text="Destination Folder:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self.root, textvariable=self.dest_var, width=50).grid(row=2, column=1)
        tk.Button(self.root, text="Browse", command=self.select_destination).grid(row=2, column=2)

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        tk.Button(button_frame, text="Accept", command=self.start_organizing).pack(side="left", padx=10)
        tk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.grid(row=5, column=0, columnspan=3, pady=(0, 10))

    #Browsing folder for source
    def select_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_var.set(folder)

    #Browsing folder for destination
    def select_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_var.set(folder)

    #Clears all information from tk.entry field
    def clear_fields(self):
        self.source_var.set("")
        self.dest_var.set("")
        self.progress["value"] = 0
        self.progress_label.config(text="")

    #Handles any incomplete information or invalid directories, then begins organization
    def start_organizing(self):
        source = self.source_var.get()
        dest = self.dest_var.get()

        if not source or not dest:      #Warning for incomplete info
            messagebox.showwarning("Missing Information", "Please select both source and destination folders")
            return
        if not path.isdir(source):      #Error for invalid source
            messagebox.showerror("Invalid Source", "The source folder is invalid or doesn't exist")
            return
        if not path.isdir(dest):        #Error for invalid destination
            messagebox.showerror("Invalid Destination", "The destination folder is invalid or doesn't exist")
            return

        #passes valid source and destination directories to organize_directory function
        self.organize_directory(source, dest)

    #Handles progress bar information, organizes files, and deletes empty directories
    def organize_directory(self, source_dir, dest_dir):
        total_files = sum(len(files) for _, _, files in walk(source_dir)) + \
                      sum(len(files) for _, _, files in walk(dest_dir))         #runs through entire source and destination directory and counts all files    
        self.progress["value"] = 0                                              #Start progress bar at 0
        self.progress["maximum"] = total_files                                  

        log_path = path.join(dest_dir, "Organizer_log.txt")                     #variable for storing log
        with open(log_path, "a") as log:                                        #opens log and start writing
            log.write(f"\n=== Organizing started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            
            self.organize_files(dest_dir, dest_dir, log)                #Organizes destination first
            self.organize_files(source_dir, dest_dir, log)              #Organizes Source source next and moves source to destination

            self.delete_empty_folders(source_dir, log)                  #Once file loop empty, cleans out empty files from source
            self.delete_empty_folders(dest_dir, log)                    #Cleans out destination

            log.write("=== Organizing completed ===\n")                 #End of log

        messagebox.showinfo("Done", "Files organized successfully!")    #Completion popup          
        self.clear_fields()

    # Moves files from source to destination
    def organize_files(self, source_dir, dest_dir, log):        
        for dirpath, _, filenames in walk(source_dir):              #Walks through every subfolder until it hits files
            for filename in filenames:                              #Walks through every file
                if filename == "Organizer_log.txt":                 #Appends to log if it already exists
                    continue   
                full_path = path.join(dirpath, filename)            #joins the directory path and the file

                created = path.getctime(full_path)                  #Variable for date created
                modified = path.getmtime(full_path)                 #Variable for date modified
                origin_date = min(created, modified)                #Takes the older of the two

                year = strftime("%Y", localtime(origin_date))                       #Formats year for directory creation
                month = self.format_month(strftime("%m", localtime(origin_date)))   #Formats Month for directory creations

                sub_folder = self.get_file_type(filename)           #Determines file type and what folder to store file in. Returns Image, Video, Misc
                dest_base = path.join(dest_dir, sub_folder)         #Joins directory to subfolder(Image, Video, Misc)
                target_folder = path.join(dest_base, year, month)   #Joins directory with subfolder to appropriately dated subfolder
                dest_path = path.join(target_folder, filename)      #Adds the filename to directory path
                if exists(dest_path):                               #Skips duplicate file already in destination
                    log.write(f"Skipped (duplicate): {filename}")   #Log notes that a duplicate file was skipped
                    continue
                makedirs(target_folder, exist_ok=True)              #Makes the directory
                try:
                    move(full_path, dest_path)                      #Attempts to move file                     
                except Exception as e:                              #Any failed attempt logged
                    log.write(f"Failed to move {filename}: {str(e)}")
                    
                log.write(f"Moved: {path.join(source_dir,filename)} => {dest_path}\n")  #Logs the file

                self.progress["value"] += 1                         #Adds to completed files transfer
                self.progress_label.config(text=f"Transferring: {filename} ({int(self.progress['value'])} / {int(self.progress['maximum'])})")
                self.root.update_idletasks()                        #Updates UI progress bar

    #Deletes any empty folders
    def delete_empty_folders(self, directory, log):                 
            for dirpath, _, _ in walk(directory, topdown=False):
                try:
                    if dirpath == directory:
                        continue                        # skip root directory itself
                    contents = listdir(dirpath)
                    if not contents:
                        #OneDrive often locks files to read only because of syncing, the following code
                        #modifies the permissions to allow empty folder to be deleted
                        chmod(dirpath, stat.S_IWRITE)   #Remove read-only flag if set
                        rmdir(dirpath)                  #Removes folder
                        log.write(f"Deleted empty folder: {dirpath}\n") 
                    else:
                        log.write(f"Skipped: {dirpath} is not empty.\n")
                except Exception as e:
                    log.write(f"Failed to delete {dirpath}: {str(e)}\n")

    #Determines file type and returns folder name
    def get_file_type(self, filename):
        name = filename.lower()
        if any(name.endswith(ext) for ext in self.IMAGE_EXTENSIONS):
            return "Images"
        elif any(name.endswith(ext) for ext in self.VIDEO_EXTENSIONS):
            return "Videos"
        else:
            return "Misc"

    #Formats date for the output folders
    def format_month(self, month):
        return f"{int(month)} - {datetime.strptime(month, '%m').strftime('%B')}"

if __name__ == "__main__":
    root = tk.Tk()
    app = PictureOrganizerApp(root)
    root.mainloop()
