# Cli Utils

**Prototyping Stage**

### The Environment File
Although this utility is desinged to use as few dependecies as possible, it is also designed for scripts to be copied, and adjusted for user preference. The packages I've used are generally installed in any data science toolbox, and so should not be necessary for most users. However, for documentation purposes and separation, I include a yaml (for use in conda/mamba) file for people to generate an environment where everything works.

### Run a file from the internet
For many of these utilites it may be more convenient to run the scripts from the internet.
This means we don't have to download the whole utility and specify the file location.
This can be helpful so we can use the most up-to-date version, use just one or two specific scripts from the repository or when we want to specify a hard-coded location, for example when using a virtual machine.
We'll need the raw file from GitHub to do this (or whatever server you are holding it)
`python -c "$(curl -s https://raw.githubusercontent.com/beml201/b_utils/main/py_utils/ToCify.py?token=GHSAT0AAAAAACMNM6DQ2XPPYJ6DZSYNK7G4ZMX22O)" -s "mystring" --boolparam`
You can specify urls at the start of a bash script and call them if this is easier
```URL="https://raw.githubusercontent.com/beml201/b_utils/main/py_utils/ToCify.py?token=GHSAT0AAAAAACMNM6DQ2XPPYJ6DZSYNK7G4ZMX22O"
python -c "$(curl -s $URL)" -s "newstring" --boolparam```
