import shutil, os, time, sched
import watchdog.observers as wd
from watchdog.events import FileSystemEventHandler, FileSystemEvent


folderNames = ["images", "videos", "documents", "music", "other", "coding"]
options = ["Watch Dir", "List directory", "Exit"]
events_schedule = sched.scheduler(time.time, time.sleep)


class eventLogger(FileSystemEventHandler):
    # Handle any event
    def on_any_event(self, event: FileSystemEvent) -> None:
        print(f"Event: {event.event_type} File: {event.src_path}")

    @staticmethod
    def sort_file(file_path):
        for root, dirs, files in os.walk(file_path):  # Searches for subdirectories and files in the root directory
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Get file extension
                file_extension = os.path.splitext(file_name)[1].lower()
                # Get the file extension and convert it to lowercase

                # Get the destination folder based on the file extension
                destination_folder = eventLogger.get_destination(file_extension)
                print(f"Destination folder: {destination_folder}")

                destination_path = os.path.join(file_path, '..',
                                                destination_folder)  # Get the destination path from original file path

                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)  # Check if the destination path exists and create it if it doesn't

                # DEBUG: print(f"Destination path: {destination_path}") # Print the destination path

                destination_file_path = os.path.join(destination_path, file_name)  # Full file path of the destination
                try:
                    shutil.move(file_path, destination_file_path)  # Move the file to the destination folder
                    print(
                        f"Moved {file_path} to {destination_file_path}")  # Printed confirmation of successful file move
                except Exception as e:
                    print(f"Error moving {file_path}: {str(e)}")

    # File type list, if not on list classed as other
    def get_destination(file_extension):
        file_type = {
            ".jpg": "images",
            ".png": "images",
            ".jpeg": "images",
            ".gif": "images",
            ".mp4": "videos",
            ".mkv": "videos",
            ".avi": "videos",
            ".pdf": "documents",
            ".doc": "documents",
            ".docx": "documents",
            ".txt": "documents",
            ".mp3": "music",
            ".wav": "music",
            ".flac": "music",
            ".zip": "other",
            ".rar": "other",
            ".exe": "other",
            ".msi": "other",
            ".iso": "other",
            ".deb": "other",
            ".rpm": "other",
            ".tar": "other",
            ".gz": "other",
            ".7z": "other",
            ".apk": "other",
            ".dmg": "other",
            ".pkg": "other",
            ".bin": "other",
            ".sh": "other",
            ".bat": "other",
            ".py": "coding",
            ".c": "coding",
            ".cpp": "coding",
            ".java": "coding",
            ".html": "coding",
            ".css": "coding",
            ".js": "coding",
            ".ts": "coding",
            ".php": "coding"
        }
        return file_type.get(file_extension, "other")


class Handler:

    def __init__(self):
        self.folder_found = None
        self.root_dir = None
        self.folder_to_watch = None
        self.windows_user = None

    @staticmethod
    def prompt_user_options(u_options, folder_found): # Prompt user to choose an option
        if folder_found:
            print("Choose")
            for i, option in enumerate(u_options): # lists the options from options list
                print(f"{i + 1}. {option}")
            try:
                choice = int(input("Enter the choice: ")) # Get user choice
                print(choice)
                if choice == 1: # TODO: Implment other options
                    prompt = input("sort files? (y/n): ") # Prompt user to sort files
                    if prompt == "y":
                        eventLogger.sort_file(folder_found) # Sort files in the folder
                    watch_dir = watchDir(folder_found) # Select the folder to watch for changes
                    watch_dir.start() # Start watching the folder
            except ValueError:
                print("Invalid choice, enter a number")
        else:
            print("Folder not found")

    @staticmethod
    def search_for_dir(rootdir, folder2watch, windows_user):
        possible_dirs = [] # List to store possible directories
        for root, dirs, files in os.walk(rootdir): # Searches for subdirectories and files in the root directory
            if "Users" in root: # Check for users folder in the root directory
                folder = os.listdir(root) # List root directory
                windows_user_lower = windows_user.lower() # Convert Windows user to lowercase
                folder_lower = [folder.lower() for folder in folder] # Convert folder names to lowercase
                if windows_user_lower in folder_lower: # Check if Windows user is in the folder list
                    user_dir = os.path.join(root, windows_user) # Get the user directory from root and Windows user
                    possible_dirs.append(user_dir) # Append the user directory to the possible directories list
        if len(possible_dirs) >= 1: # Check if possible directories list has at least one directory
            # TODO: Implement if its one option automatically choose it
            print("Choose the folder to proceed")
            for i, dirs in enumerate(possible_dirs): # List the possible directories for the user to choose
                print(f"{i + 1}. {dirs}")
            folder_choice = int(input("Enter the folder number: ")) # Get the user choice
            try:
                if 0 <= folder_choice <= len(possible_dirs): # Check if the user choice is within the possible directories list
                    for root, dirs, files in os.walk(possible_dirs[folder_choice - 1]): # Search the directory of the user choice for the folder to watch
                        folder2watch_lower = folder2watch.lower() # Change the folder name to lowercase
                        if folder2watch_lower in (folder.lower() for folder in dirs): # Check if the folder to watch is in the user directory
                            folder_found = os.path.join(root, folder2watch) # Get the path of the folder to watch
                            print(f"Folder found: {folder_found}") # Printed message to confirm that a folder was found
                            Handler.prompt_user_options(options, folder_found) # Prompt user to choose an option
                            #TODO: Maybe implment if folder not in this list, give the option to retry or continue
                        else:
                            return "Folder not found"
                else:
                    return "User folder not found" # TODO: Maybe implment a retry instead of exiting the program
            except Exception as e:
                print(e)
        else:
            return "Users folder not found"


class watchDir:
    def __init__(self, path):
        self.path = path
        self.observer = wd.Observer()
        self.event_handler = eventLogger()
        self.observer.schedule(self.event_handler, self.path, recursive=True)

    def stop(self): # Stop watching the directory
        self.observer.stop()
        self.observer.join()

    def start(self): # Start watching the directory 
        self.observer.start()
        self.observer.join()


if __name__ == "__main__":
    global root_dir
    global folder_to_watch
    global windows_user

    # Welcome message
    print("Welcome to the file sorter and directory watcher")

    # Get the root directory and the folder to watch aswell as the Windows user
    root_dir = input("Enter the root directory:  ")
    folder_to_watch = input("Enter the folder to watch: ")
    windows_user = input("Enter the windows user: ")

    # Check if the root directory provided exists if not exit
    if not os.path.exists(root_dir):
        print("Invalid directory")
        exit()

    #Main Handling
    found_folder = Handler.search_for_dir(root_dir, folder_to_watch, windows_user)
