# imports
import time, sys, queue
from pathlib import Path
# local imports
from src import play
from src.colors import colors

done_writing_queue = queue.Queue()
history_folder_path = Path(Path(__file__).parent.parent) / "history" 
history_file_path = history_folder_path / "history.txt"

def write_history(link, is_history, is_on_web = False):
    # Make the history folder and file if they doesn't exist
    try:
        history_folder_path.mkdir(parents=True, exist_ok=True)
        history_file_path.touch(exist_ok=True) 
    except PermissionError:
        print("Unable to write/read to where history file is suposed to be due to permissions.")
   
    with history_file_path.open('r') as history_file:
        data = history_file.readlines()

    index = 0
    in_data = False
    seconds = 0
    
    
    for i in data:
        if link in i:
            index = index
            in_data = True
            break
        else:
            pass
             
        index += 1
    
    if in_data == True:
        # match exsisting with provided link so we can add the newly watched seconds, when link already in history, to the old ones
        if is_history == True: 
            
            time.sleep(10) #delay until player opens (guessed) 
            while play.stop == False:
                time.sleep(1)
                seconds += 1

            changed_line = data[index].split("#")
            changed_secs = changed_line[1].replace(changed_line[1], str(seconds + int(changed_line[1])))
            changed_line = changed_line[0] + "#" + changed_secs + "\n"
            data[index] = changed_line
            data += [data.pop(index)] #move element to last line
            with history_file_path.open('w') as history_file:
                for element in data:    
                    history_file.write(element)
        else:
            # if already in history and the episode is not played from history-selection, move it to firstt plavce in history 
            data += [data.pop(index)]
            with history_file_path.open('w') as history_file:
                for element in data:    
                    history_file.write(element)
    else:
        if is_on_web == False:
            # loop to measure time until player is closed
            time.sleep(10) #delay until player opens (guessed) 
            while play.stop == False:
                time.sleep(1)
                seconds += 1
        else:
            pass
        
        with history_file_path.open('a') as history_file:
            # seperate link and seconds with "#" to make it esier to read history
            history_file.write(link + "#" + str(seconds) + "\n")

    done_writing_queue.put(True)
    
def read_history():
    while True:
        check = done_writing_queue.get()
        if check == True:
            break
        time.sleep(0.2)
        
    try:
        with history_file_path.open('r') as history_file:
            data = history_file.readlines()
        links = []
        resume_seconds = []
        
        
        for i in data:
            i = i.split("#")
            links.append(i[0])
            resume_seconds.append(i[1].replace("\n", ""))


    except:
        pass
    
    return links, resume_seconds

def pick_history():
    
    #read history and reverse lists so last history-point is first in selection
    history = read_history()
    links = history[0]
    resume_seconds = history[1]
    links.reverse()
    resume_seconds.reverse()

    if not links:
        print(colors.ERROR + "No history")
        sys.exit()
    counter = 1
    for i in links:
        print(colors.GREEN + "["+  str(counter) + "]" +  colors.END + " " + str(i.replace("https://gogoanime.wiki/", "")))
        counter += 1
    
    which_anime = input("Enter Number: " + colors.CYAN)
    
    try: 
        link = links[int(which_anime) - 1]
        resume_seconds = resume_seconds[int(which_anime) - 1]
    except:
        print(colors.ERROR + "Invalid Input")
        sys.exit()
    
    return link, resume_seconds 
