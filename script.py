import os
import time
import subprocess
# Configuration
WATCH_FOLDER = "path_to_watch_folder"  # Path to monitor for new images
UPLOADED_FOLDER = os.path.join(WATCH_FOLDER, "uploaded")
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
CHECK_INTERVAL = 5  # Time in seconds between folder checks
UPLOAD_DELAY = 30  # Time to wait before uploading a new file
# Ensure the "uploaded" folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)
def upload_file(file_path):
    """Uploads a file using the curl command."""
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and "success" in result.stdout.lower():
            print(f"[INFO] Uploaded: {file_path}")
            return True
        else:
            print(f"[ERROR] Upload failed for {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception during upload for {file_path}: {e}")
        return False
def move_to_uploaded(file_path):
    """Moves a file to the uploaded folder."""
    try:
        destination = os.path.join(UPLOADED_FOLDER, os.path.basename(file_path))
        os.rename(file_path, destination)
        print(f"[INFO] Moved to uploaded: {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not move {file_path} to uploaded folder: {e}")
def monitor_folder():
    """Monitors the folder for new images and handles upload and moving."""
    print(f"[INFO] Monitoring folder: {WATCH_FOLDER}")
    processed_files = set()
    while True:
        try:
            # Get a list of all files in the watch folder
            current_files = {
                os.path.join(WATCH_FOLDER, f)
                for f in os.listdir(WATCH_FOLDER)
                if os.path.isfile(os.path.join(WATCH_FOLDER, f))
            }
            # Identify new files that haven't been processed yet
            new_files = current_files - processed_files
            for file_path in new_files:
                print(f"[INFO] Detected new file: {file_path}")
                time.sleep(UPLOAD_DELAY)  # Wait before uploading
                if upload_file(file_path):
                    move_to_uploaded(file_path)
                    processed_files.add(file_path)
                else:
                    print(f"[WARNING] Skipping file: {file_path}")
            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"[ERROR] Exception in monitor loop: {e}")
            time.sleep(CHECK_INTERVAL)
if __name__ == "__main__":
    monitor_folder()














