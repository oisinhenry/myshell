# oisinhenry/myshell: a simple shell written in python
This repo is for personal version control of my CA216 shell assignment.

## TODO:
* ~~Implement i/o redirection on output.
`programname arg1 arg2 > outputfile` needs to work. Fair bit of logic needed in the `default` method for this.~~ Pretty much done but it's with system calls which might not be ideal.
* ~~Implement background execution of programs when the `&` is appended to commands. The shell needs to return to the command line immediately when this is invoked.~~ This is sort of done, but it could probably be cleaned up a lot.
* ~~Output redirection for the internal commands `dir environ echo help`~~
* ~~Write~~ Finish/clean up user manual
* ~~Return user manual when `help` command is entered with no arguments.~~
* Refactor into multiple python files / generally clean up code.
