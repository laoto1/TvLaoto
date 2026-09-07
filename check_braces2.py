import re

with open('app/src/main/java/com/tvlaoto/ui/screens/HomeScreen.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's count braces ignoring strings and comments
def count_braces(s):
    in_string = False
    in_comment = False
    in_multiline = False
    opens = 0
    closes = 0
    i = 0
    while i < len(s):
        c = s[i]
        if in_string:
            if c == '"' and s[i-1] != '\\':
                in_string = False
        elif in_comment:
            if c == '\n':
                in_comment = False
        elif in_multiline:
            if c == '*' and i+1 < len(s) and s[i+1] == '/':
                in_multiline = True
                i += 1
        else:
            if c == '"':
                in_string = True
            elif c == '/' and i+1 < len(s) and s[i+1] == '/':
                in_comment = True
                i += 1
            elif c == '/' and i+1 < len(s) and s[i+1] == '*':
                in_multiline = True
                i += 1
            elif c == '{':
                opens += 1
            elif c == '}':
                closes += 1
        i += 1
    return opens, closes

o, c = count_braces(text)
print("Actual Open:", o, "Actual Close:", c)
