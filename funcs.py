import os

def readfile(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
    else:
        lines = []
    return lines

def writeFile(filename,lines):
    with open(filename, 'w') as f:
        f.writelines(lines)