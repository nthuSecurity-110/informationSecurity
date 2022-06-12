fullstring = "StackAbuse"
substring = "tack"

try:
    print(fullstring.find(substring))
    print("Found!")
except ValueError:
    print("Not found!")
    