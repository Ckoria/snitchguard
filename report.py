from datetime import datetime

def write_to_csv(name):
    current_time = datetime.now()
    with open("log.csv", "r+") as log:
        id = int((log.readlines()[-1].split(","))[0])
        id += 1
        log.writelines(f'\n{id}, {name}, {current_time},')
             
             
