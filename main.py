import psutil
import win32api
import time

def sandboxCheck():
    ### Config

    checktype = "all"
    # "all" means that all of them have to be true to consider the computer as clean
    # "partial" means that at least one of them has to be true to consider the computer as clean


    ### Config end
    """
    Explanation of Checks:

    (False negative (FN) = Computer is a sandbox, and wasn't detected)
    (False positive (FP) = Computer wasn't a sandbox, and was detected to be one)
    (Most of these ratings are guesses)

    Process check: FN: REALLY-LOW / FP: HIGH
        Most sandboxes don't usually have programs like Chrome or Discord running.
        This means that if we check if those processes are running,
        we can guess if it's a sandbox.
        You can add custom processes via the function config
        Configs:
            - Processes to look for
    
    Mouse check: FN: MEDIUM / FP: LOW
        Checks if the mouse is moving for roughly 30 seconds (configurable).
        Most automated sandboxes (like virustotal) don't move their mouse (afaik).
        But an actual person might move their virtual mouse in an sandbox or a virtual machine.
        Configs:
            - Timeout (Default 30 seconds)

    RAM check: FN: LOW / FP: MEDIUM
        Checks how much the computer has RAM.
        Most sandboxes don't have much RAM, especially automated ones.
        Personal virtual machines might have quite a bit though
        Configs:
            - Total RAM (Default 4 gb)
            - Currently used RAM (Default 1 gb)

    All of these checks have configs inside of them, feel free to adjust them to your liking
    """



    ######### Don't touch anything below this line (Except for the check's configs) ########



    # Process Check
    def processCheck():
        # Config:
        # Put processes that would normally be running on the victim's computer here
        processes = ["Discord.exe", "explorer.exe", "python.exe", "chrome.exe"]
        # You can check them from the "Details" tab on task manager

        proceed = False
        for process in psutil.process_iter():
            for i in processes:
                if process.name() == i:
                    proceed = True

        if proceed is False:
            return False

        return True

    # Mouse check
    def mouseCheck():
        # Config:
        # Seconds until timeout
        timeoutseconds = 30


        # Get the current position of the mouse
        x, y = win32api.GetCursorPos()

        # Wait for the mouse to move
        while True:
            timeoutseconds -= 1
            time.sleep(1)
            new_x, new_y = win32api.GetCursorPos()
            # If the mouse moves, return True
            if new_x != x or new_y != y:
                return True
            # If timeout reaches 0, return False
            elif timeoutseconds <= 0:
                return False

    # RAM check
    def ramCheck():
        # Config:
        # All of these are in bytes!
        minimum_used_ram = 1000000000 # Default is 1 gb (2097152000 bytes)
        minimum_total_ram = 4194304000 # Default is 4 gb (4194304000 bytes)

        ram_stats = psutil.virtual_memory()
        if ram_stats.total <= minimum_total_ram:
            return False
        if ram_stats.used <= minimum_used_ram:
            return False
        return True


    # Logic      
    if checktype == "all": # "all" check
        isSandbox = False
        if processCheck() == False:
            isSandbox = True
        elif mouseCheck() == False:
            isSandbox = True
        elif ramCheck() == False:
            isSandbox = True

    elif checktype == "partial": # "partial" check
        isSandbox = True
        if processCheck() == True:
            isSandbox = False
        elif mouseCheck() == True:
            isSandbox = False
        elif ramCheck() == True:
            isSandbox = False

    else:
        raise("You entered an invalid check-type")

    if isSandbox == True:
        return False
    return True

if sandboxCheck() == False:
    print("Sandbox active!")
    quit()

# Put un-sandboxed code here
print("Computer was not a sandbox!")
