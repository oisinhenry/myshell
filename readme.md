# oisinhenry/myshell: a simple shell written in python
This repo is for personal version control of my CA216 shell assignment.

## TODO:
* ~~Implement i/o redirection on output.
`programname arg1 arg2 > outputfile` needs to work. Fair bit of logic needed in the `default` method for this.~~ Pretty much done but it's with system calls which might not be ideal.
* ~~Output redirection for the internal commands `dir environ echo help`~~
* ~~Write~~ Finish/clean up user manual
* ~~Return user manual when `help` command is entered with no arguments.~~
* Refactor into multiple python files / generally clean up code. (DO THIS)
* Implement better `pause` command. (Currently errors on keyboard interrupt).
* Implement better `clr` command without using system calls.
* Fix background execution of commands in the `default` method.
