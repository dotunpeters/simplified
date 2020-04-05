from datetime import datetime

with open("logs.txt", "a") as log_file:
    log_file.write(f"Run time: {datetime.now().month}:{datetime.now().day}, {datetime.now().hour}:{datetime.now().minute} \n")