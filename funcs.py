import os, subprocess

def diskUsage(path):
    # """disk usage in human readable format (e.g. '2,1GB')"""
    # return subprocess.check_output(['du','-sh', '--block-size=1M', path]).split()[0].decode('utf-8')
    """disk usage in Mb"""
    return subprocess.check_output(['du','-sh', '--block-size=1M', path]).split()[0].decode('utf-8')

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