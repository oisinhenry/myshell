# oisinhenry/myshell: a simple shell written in python
This repo is for personal version control of my CA216 shell assignment.

## TODO:
* ~~Implement i/o redirection on output.
`programname arg1 arg2 > outputfile` needs to work. Fair bit of logic needed in the `default` method for this.~~
* ~~Output redirection for the internal commands `dir environ echo help`~~
* ~~Write~~ Finish/clean up user manual
* ~~Return user manual when `help` command is entered with no arguments.~~
* ~~Implement better `pause` command. (Currently errors on keyboard interrupt).~~ Still a bit of a hack fix this.
* ~~Implement better `clr` command without using system calls.~~
* ~~Fix background execution of commands in the `default` method.~~ 
* **Refactor into multiple python files / generally clean up code.** This is now basically priority number one as most of the other functionality is complete.
