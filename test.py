def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


i = "1"
j = ""
print(is_int(i), is_int(j))
