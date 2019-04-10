from cmd import Cmd
import os
import subprocess
import sys


class myPrompt(Cmd):                # main class for the prompt. inherits from cmd.Cmd

    def do_help(self, args):        # TODO: output redirection
        os.system("more readme")

    def do_quit(self, args):        # first few simple commands. each command needs an 'args' parameter
        print("Bye")                # even if it's not used, otherwise errors are thrown.
        return True
# random comment to test some git stuff
    def help_quit(self):
        print("Exit the application.")

    def do_echo(self, s):
        if " > " in s:                  # logic to check if i/o redirection is invoked. I was going to put this
            tokens = s.split(">")       # in a separate function and just call it in each command, but it was
            f = open(tokens[1], "w")    # awkward as the logic works differently for some commands, e.g. echo and dir.
            f.write(tokens[0])          # it's slightly cumbersome having it live here, but it's the best solution I
        elif " >> " in s:               # have right now.
            tokens = s.split(">>")
            f = open(tokens[1], "a")
            f.write(tokens[0])
        else:
            print(s)

    def help_echo(self):                # slightly cumbersome having the help commands interspersed with the do commands
        print("Return a given string. Usage: echo <string>")    # i may move them around for readability later.

    def do_cd(self, d=""):
        if d != "":
            try:
                os.chdir(d)
                full_path = os.getcwd()
                os.environ["PWD"] = os.getcwd()     # update PWD env variable
                prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~" + ENDC + "$ "
                # this just updates the prompt prefix on screen.
                # these variables are just global colour codes for terminal.
            except:             # very broad except but only one type of error will ever occur here
                print("Directory " + "'" + d + "'" + " does not exist in this location. Do 'help cd' for help.")

        else:
            print(os.getcwd())

    def help_cd(self):
        print("Change the current directory. If no arguments are supplied, print working directory.")
        print("Usage: cd <directory>")

    def do_clr(self, args):
        clear = lambda: os.system("clear")
        clear()

    def help_clr(self):
        print("Clears the terminal.")

    def do_dir(self, args):         # TODO: output redirection
        contents = os.listdir(full_path + "/" + args)
        for key in contents:
            print(key)

    def help_dir(self):
        print("Lists the contents of a given directory. If no arguments are supplied, current directory is used.")
        print("Usage: dir <directory>")

    def do_pause(self, args):
        input("Press Enter to continue...")     # rudimentary but functional pause.

    def help_pause(self):
        print("Pauses the shell and waits for user input.")

    def do_environ(self, args):
        if "> " in args:
            tokens = args.split()       # similar (but unfortunately slightly different) logic to check
            f = open(tokens[1], "w")    # whether i/o redirection is invoked.
            for key in os.environ:
                f.write(key + "\n")
        elif ">> " in args:
            tokens = args.split()
            f = open(tokens[1], "a")
            for key in os.environ:
                f.write(key + "\n")
        else:
            for l in os.environ:
                print(l)

    def help_environ(self):
        print("Lists all the environment variables.")

    def do_pwd(self, key):        # testing command for the PWD environment string update.
        print(os.environ["PWD"])

    def default(self, command):      # method called when command prefix not recognised (ie program invocation)
        # TODO: implement forking process here for program invocation
        # TODO: logic for error if command isn't an actual Linux command
        # print("default response test")
        # opener = "open" if sys.platform == "darwin" else "xdg-open"
        # subprocess.call([opener, line])
        if "&" in command:
            try:
                os.system(command[:-2])
            except:
                print("Command not recognised internally or by Linux shell.")
                print(command[:-2])
        else:
            try:
                os.system(command)
            except:
                print("Command not recognised internally or by Linux shell.")

    def do_testargs(self, args):
        for arg in args.split():
            print(arg)

    def do_testbg(self, args):
        subprocess.Popen("gedit", creationflags=subprocess.CREATE_NO_WINDOW)


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

if __name__ == '__main__':      # main function where prompt is created and run
    prompt = myPrompt()
    full_path = os.getcwd()     # path string for start of prompt
    # print(sys.argv)

    if len(sys.argv) > 1:                   # here is the logic for command line invocation with batch file argument.
        with open(sys.argv[1]) as file:
            for line in file.readlines():
                prompt.onecmd(line)

    else:                                   # else just prompt user for input.
        prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~" + ENDC + "$ "
        prompt.cmdloop(HEADER + "Starting prompt. Type '?' or 'help' for commands.")



