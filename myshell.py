from cmd import Cmd
import os
import sys
# Oisin Henry
# 17312911


class myPrompt(Cmd):                # main class for the prompt. inherits from cmd.Cmd

    def do_help(self, args):

        if args and ">" not in args:    # case of help <command> for specific help.
            # print(myPrompt.help_dir(self))
            print(myPrompt.help_parser(self, args), end="")
            return ""

        if args.startswith("> "):   # help invoked with overwrite redirection.
            tokens = args.split()
            f = open(tokens[1].strip(), "w")
            readfile = open(readmepath, "r")
            f.write(readfile.read())

        elif args.startswith(">>"):  # help invoked with append redirection.
            tokens = args.split()
            f = open(tokens[1].strip(), "a")
            readfile = open(readmepath, "r")
            f.write(readfile.read())

        else:                        # help invoked without redirection. return user manual.
            os.system("more " + readmepath)

    def do_quit(self, args):        # first few simple commands. each command needs an 'args' parameter
        print("Bye")                # even if it's not used, otherwise errors are thrown.
        return True

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

    def do_cd(self, d=""):
        if d != "":         # directory supplied as an argument.
            try:
                os.chdir(d)
                full_path = os.getcwd()
                os.environ["PWD"] = os.getcwd()     # update PWD env variable
                prompt.prompt = "shell=" + BOLD + BLUE + full_path + ENDC + "$ "
                # this just updates the prompt prefix on screen.
                # ALL CAPS variables are just global colour codes for terminal.

            except:
                print("Directory " + "'" + d + "'" + " does not exist in this location. Do 'help cd' for help.")

        else:               # no arguments supplied. use current dir.
            print(os.getcwd())

    def do_clr(self, args):
        sys.stderr.write("\x1b[2J\x1b[H")   # linux escape sequence to clear the terminal.

    def do_dir(self, args):
        # logic is cumbersome here because of multiple cases. 4 possibilities between argument/no argument
        # and ">" or ">>".
        try:
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

            elif args.startswith(">>"):       # case of dir >> somefile.txt (i.e. current dir)
                tokens = args.split()
                f = open(tokens[1].strip(), "a")
                files = os.listdir(os.environ['PWD'])
                for key in files:
                    f.write(key + "\n")

            else:
                contents = os.listdir(os.environ['PWD'] + "/" + args)
                for key in contents:
                    print(key)
        except:
            print("Directory not found.")

    def do_pause(self, args):
        try:
            input("Press Enter to continue...")     # rudimentary but functional pause.
        except:     # keyboard interrupts could break this without a try/except
            pass

    def do_environ(self, args):
        # unfortunately, different logic needed for
        # each internal command when redirection is invoked.

        if args.startswith("> "):            # overwrite redirection invoked.
            tokens = args.split()
            f = open(tokens[1], "w")
            for key in os.environ:
                f.write(key + ": " + os.environ[key] + "\n")

        elif args.startswith(">>"):         # append redirection invoked.
            tokens = args.split()
            f = open(tokens[1], "a")
            for key in os.environ:
                f.write(key + ": " + os.environ[key] + "\n")

        else:                       # no redirection invoked.
            for l in os.environ:
                print(l+":", os.environ[l])


    def emptyline(self):    # method to avoid the shell re-entering the last command when no input is given.
        pass                # just a small quirk of the Cmd module that had to be dealt with

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

    # this is called when "help <command>" is used for specific help with a command.
    def help_parser(self, args):    # better way of implementing specific help because the Cmd way of writing
        if args == "quit":          # a method for each one clashes with the regular "help" command override.
            return "Exit the application.\n"
        elif args == "echo":
            return "Return a given string. Usage: echo <string>\n"
        elif args == "cd":
            return "Change the current directory. If no arguments are supplied, print working directory.\nUsage: cd <directory>\n"
        elif args == "clr":
            return "Clears the terminal.\n"
        elif args == "dir":
            return "Lists the contents of a given directory. If no arguments are supplied, current directory is used.\nUsage: dir <directory>\n"
        elif args == "pause":
            return "Pauses the shell and waits for user input.\n"
        elif args == "environ":
            return "Lists all the environment variables.\n"


# global variables for ease of access to ANSI escape sequences
# for colour coding in the terminal
HEADER = '\033[95m'
BLUE = '\033[94m'
ENDC = '\033[0m'
BOLD = '\033[1m'


if __name__ == '__main__':      # main function where prompt is created and run
    prompt = myPrompt()
    full_path = os.getcwd()     # path string for start of prompt
    readmepath = os.environ['PWD'] + "/readme"  # dynamic path for readme so "help" can be invoked even after changing dir

    if len(sys.argv) > 1:                   # here is the logic for command line invocation with batch file argument.
        with open(sys.argv[1]) as file:
            for line in file.readlines():
                prompt.onecmd(line)

    else:                                   # else just prompt user for input.
        prompt.prompt = "shell=" + BOLD + BLUE + full_path + ENDC + "$ "    # prompt is colour coded to differentiate it from the regular linux shell.
        prompt.cmdloop(HEADER + "Starting prompt. Type '?' or 'help' for commands. Type 'help <command>' for help with a specific command.")



