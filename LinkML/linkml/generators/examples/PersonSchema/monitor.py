import os
import pyinotify

# Define the file path you want to monitor
file_path = "personinfo.yaml"

# Define a custom event handler class
class FileMonitor(pyinotify.ProcessEvent):
    def process_default(self, event):
        if event.pathname == os.path.abspath(file_path):
            print(f"File {file_path} has been modified!")

# Initialize the inotify instance and event handler
wm = pyinotify.WatchManager()
mask = pyinotify.IN_MODIFY
notifier = pyinotify.Notifier(wm, FileMonitor())

# Add the file to the watch list
wdd = wm.add_watch(file_path, mask, rec=False)

try:
    print(f"Monitoring changes to {file_path}. Press Ctrl+C to stop.")
    notifier.loop()
except KeyboardInterrupt:
    pass
finally:
    notifier.stop()
