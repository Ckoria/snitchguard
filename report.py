from datetime import datetime

def write_to_csv(name):
    current_time = datetime.now()
    with open("log.csv", "r+") as log:
        print(log.readlines())
        id = 0
        log.writelines(f'\n{id}, {name}, {current_time},')
             