from cmd import Cmd
import os
import subprocess
import sys


class myPrompt(Cmd):
    def do_quit(self, key):
        print("Bye")
        return True

    def help_quit(self):
        print("Exit the application.")

    def do_echo(self, s):
        print(s)

    def help_echo(self):
        print("Return a given string. Usage: echo <string>")

    def do_cd(self, d=""):
        if d != "":
            try:
                os.chdir(d)
                full_path = os.getcwd()
                os.environ["PWD"] = os.getcwd()
                prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~" + ENDC + "$ "
            except:
                print("Directory " + "'" + d + "'" + " does not exist in this location. Do 'help cd' for help.")

        else:
            print(os.getcwd())

    def help_cd(self):
        print("Change the current directory. If no arguments are supplied, print working directory.")
        print("Usage: cd <directory>")

    def do_clr(self, key):
        clear = lambda: os.system("clear")
        clear()

    def help_clr(self):
        print("Clears the terminal.")

    def do_dir(self, directory):
        contents = os.listdir(full_path + "/" + directory)
        for key in contents:
            print(key)

    def help_dir(self):
        print("Lists the contents of a given directory. If no arguments are supplied, current directory is used.")
        print("Usage: dir <directory>")

    def do_pause(self, key):
        input("Press Enter to continue...")

    def help_pause(self):
        print("Pauses the shell and waits for user input.")

    def do_environ(self, key):
        for line in os.environ:
            print(line)

    def help_environ(self):
        print("Lists all the environment variables.")

    def do_pwd(self, key):        # testing command for the PWD environment string update.
        print(os.environ["PWD"])

    def default(self, line): # method called when command prefix not recognised (ie program invocation)
        # TODO: implement forking process here for program invocation
        print("default response test")
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, line])


# global variables for ease of access to ANSI escape sequences
# for colour coding in the terminal
HEADER = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

if __name__ == '__main__':
    prompt = myPrompt()
    full_path = os.getcwd()
    print(sys.argv)

    if len(sys.argv) > 1:                   # here is the logic for command line invocation with batch file argument.
        with open(sys.argv[1]) as file:
            for line in file.readlines():
                prompt.onecmd(line)

    else:
        prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~" + ENDC + "$ "
        prompt.cmdloop(HEADER + "Starting prompt. Type ? to list commands.")



