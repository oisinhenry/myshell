from cmd import Cmd
import os

class myPrompt(Cmd):
    def do_exit(self, key):
        print("Bye")
        return True
    def help_exit(self):
        print("Exit the application.")

    def do_echo(self, s):
        print(s)
    def help_echo(self):
        print("Return a given string")

    def do_cd(self, d=""):
        if d != "":
            os.chdir(d)
        else:
            print(os.getcwd())


if __name__ == '__main__':
    prompt = myPrompt()
    prompt.prompt = "$ "
    prompt.cmdloop("Starting prompt. Type ? to list commands.")



