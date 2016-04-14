# PyINI
Python ini file manipulator

To open an ini file, pass a string or a file stream to the ini class.

Edit the ini as if the ini class is a dictionary full of dictionaries. \_\_default\_\_ maps to items without a group at the top of the ini file
For example
```python
>>> i = ini.ini("""
hallo = 123
password = 3334444555

[Stuff]
cat = 4000
dog = 9000

[Stuff2]
wut = 666
wut2 = 123
"""
>>> i["__default__"]["hallo"]
123
>>> i["__default__"]["hallo"] = 789
>>> i["__default__"]["hallo"]
789
>>> i["Stuff2"]["wut"] = "lol"
>>> i["Stuff2"]["newkey"] = "new key"
>>> print(i.dump())

hallo = 789
password = 3334444555

[Stuff]
cat = 4000
dog = 9000

[Stuff2]
wut = lol
wut2 = 123

newkey = new key
```
