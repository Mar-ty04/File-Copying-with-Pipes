#Marisol Morales ID: 029984979
#Project 1: Pipes and Forks
#Due by 2/16/2025

import os
import sys

BUFFER = 25

def main():
    ##The main function will parse command-line arguments, create a pipe, fork a child process, and handle file copying

    #making sure that 3 arguments are used in the terminal
    if len(sys.argv) != 3:
        print("Error: insufficient arguments")
        print("Please follow the guidlines of ./filecopy.py <source_file.txt> <destination_file.txt>")
        sys.exit(1)

    #start procress for the code if 3 arguments are provided in terminal
    original_file = sys.argv[1]
    copy_file = sys.argv[2]

    #check if input file exists, if it doesn't then throw an error message!
    if not os.path.isfile(original_file):
        print(f"Error: Unable to open source file '{original_file}'.") #this will be thrown if file does not exist.
        sys.exit(1)

    #make file descriptors for reading a writing
    read, write = os.pipe()

    #create a child process using fork
    child_pid = os.fork()

    #this is the parent process
    if child_pid > 0:
        #close file descriptor for reading
        os.close(read)
        #begin process
        with open(original_file, "rb") as original:
            while True:
                contents = original.read(BUFFER)
                if not contents:
                    break
                os.write(write, contents)
        
        print(f"File successfully copied from {original_file} to {copy_file}")        

        os.close(write) #close file descriptor for writing
               
    #this is the child process, this is the equvialent of doing "elif child_pipe == 0:"
    elif child_pid == 0:
        #close file descriptor for writing
        os.close(write)
        #begin process
        with open(copy_file, "wb") as copy:
            while True:
                contents = os.read(read, BUFFER)
                if not contents:
                    break
                copy.write(contents)

        os.close(read) #close file descriptor for reading
    
    #check if fork failed
    else: 
        print("Error: Fork failed")
        sys.exit(1)
               
    #we commented this out since it resulted in it being printed twice
    #thus we print it out in the parent process instead!
    #print(f"File successfully copied from {original_file} to {copy_file}")

if __name__ == "__main__":
    main()
