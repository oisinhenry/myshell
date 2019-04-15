from cmd import Cmd
import os
import subprocess
import sys


class myPrompt(Cmd):                # main class for the prompt. inherits from cmd.Cmd

    def do_help(self, args):

        if args.startswith("> "):   # help invoked with overwrite redirection.
            tokens = args.split()
            f = open(tokens[1].strip(), "w")
            readfile = open("readme", "r")
            f.write(readfile.read())

        elif args.startswith(">>"):  # help invoked with append redirection.
            tokens = args.split()
            f = open(tokens[1].strip(), "a")
            readfile = open("readme", "r")
            f.write(readfile.read())

        else:                        # help invoked without redirection.
            os.system("more readme")

    def do_quit(self, args):        # first few simple commands. each command needs an 'args' parameter
        print("Bye")                # even if it's not used, otherwise errors are thrown.
        return True

    def help_quit(self):
        print("Exit the application.")

    def do_echo(self, s):

        if " > " in s:     # echo invoked with overwrite redirection.
            tokens = s.split(">")
            f = open(tokens[1].strip(), "w")
            f.write(tokens[0])

        elif " >> " in s:  # echo invoked with append redirection.
            tokens = s.split(">>")
            f = open(tokens[1].strip(), "a")
            f.write(tokens[0])

        else:               # echo invoked without redirection.
            print(s)

    def help_echo(self):
        print("Return a given string. Usage: echo <string>")

    def do_cd(self, d=""):
        if d != "":         # directory supplied as an argument.
            try:
                os.chdir(d)
                full_path = os.getcwd()
                os.environ["PWD"] = os.getcwd()     # update PWD env variable
                prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~" + ENDC + "$ "
                # this just updates the prompt prefix on screen.
                # ALL CAPS variables are just global colour codes for terminal.

            except:
                print("Directory " + "'" + d + "'" + " does not exist in this location. Do 'help cd' for help.")

        else:               # no arguments supplied. use current dir.
            print(os.getcwd())

    def help_cd(self):
        print("Change the current directory. If no arguments are supplied, print working directory.")
        print("Usage: cd <directory>")

    def do_clr(self, args):
        sys.stderr.write("\x1b[2J\x1b[H")   # linux escape sequence to clear the terminal.

    def help_clr(self):
        print("Clears the terminal.")

    def do_dir(self, args):
        # logic is cumbersome here because of multiple cases. 4 possibilities between argument/no argument
        # and ">" or ">>".
        # #TODO: make this live in another file/function?
        if " > " in args and len(args.split()) == 3:          # case of dir somedir > somefile.txt
            tokens = args.split(" > ")
            f = open(tokens[1].strip(), "w")
            files = os.listdir(os.environ['PWD'] + "/" + tokens[0])
            for key in files:
                f.write(key + "\n")

        elif " >> " in args and len(args.split()) == 3:       # case of dir somedir >> somefile.txt
            tokens = args.split(" >> ")
            f = open(tokens[1].strip(), "a")
            files = os.listdir(os.environ['PWD'] + "/" + tokens[0])
            for key in files:
                f.write(key + "\n")

        elif args.startswith("> "):        # case of dir > somefile.txt (i.e. current dir)
            tokens = args.split()
            f = open(tokens[1].strip(), "w")
            files = os.listdir(os.environ['PWD'])
            for key in files:
                f.write(key + "\n")

        elif args.startswith(">>"):       # case of dir >> somefile.txt
            tokens = args.split()
            f = open(tokens[1].strip(), "a")
            files = os.listdir(os.environ['PWD'])
            for key in files:
                f.write(key + "\n")

        else:
            contents = os.listdir(os.environ['PWD'] + "/" + args)
            for key in contents:
                print(key)

    def help_dir(self):
        print("Lists the contents of a given directory. If no arguments are supplied, current directory is used.")
        print("Usage: dir <directory>")

    def do_pause(self, args):
        try:
            input("Press Enter to continue...")     # rudimentary but functional pause.
        except:
            pass

    def help_pause(self):
        print("Pauses the shell and waits for user input.")

    def do_environ(self, args):
        # unfortunately, different logic needed for
        # each internal command when redirection is invoked.

        if "> " in args:            # overwrite redirection invoked.
            tokens = args.split()
            f = open(tokens[1], "w")
            for key in os.environ:
                f.write(key + "\n")

        elif ">> " in args:         # append redirection invoked.
            tokens = args.split()
            f = open(tokens[1], "a")
            for key in os.environ:
                f.write(key + "\n")

        else:                       # no redirection invoked.
            for l in os.environ:
                print(l)

    def help_environ(self):
        print("Lists all the environment variables.")

    def emptyline(self):
        pass

    def default(self, command):  # method called when command prefix not recognised (ie program invocation)

        if "&" in command:       # background execution is handled here with os.fork.
            try:                 # When tested with a python script, it terminates with an empty line
                        # (i.e, no visible prompt.) however, this seems to just be linux behaviour
                        # (the system shell acts the same way) and the prompt loop keeps working fine.
                        # you can enter a command on the empty line as normal or just hit enter to bring back
                        # the visible prompt.

                pid = os.fork()     # fork a new child process.
                if pid == 0:        # we are in the child process.
                    os.system(command[:-2])     # execute the command (less the "&").
                    sys.exit(0)                 # exit the child process with status 0 (success).

                else:               # else we are in the parent process.
                    return          # continue as normal.

            except:                 # system command call failed. return error and the command.
                print("Command not recognised internally or by Linux shell:")
                print(command[:-2])

        else:       # command invoked without background execution.
            try:
                os.system(command)

            except:
                print("Command not recognised internally or by Linux shell:")
                print(command)


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
        prompt.prompt = BOLD + BLUE + "~" + full_path + ENDC + ":" + BLUE + "~myshell" + ENDC + "$ "
        prompt.cmdloop(HEADER + "Starting prompt. Type '?' or 'help' for commands. Type 'help <command>' for help with a specific command.")



