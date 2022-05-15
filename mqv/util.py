class UserSystemDelimiter:

    WINDOWS = "\\"
    LINUX = "/"

usd = UserSystemDelimiter.LINUX

def concatPath(root, other):
    if root.endswith(usd):
        root = root[:-1]

    if other.startswith(usd):
        other = other[1:]

    return root + usd + other

def concatPaths(*args):
    path = args[0]

    if path.endswith(usd):
        path = path[:-1]

    for i in range(1, len(args)):
        cur = args[i]
        
        if cur.endswith(usd):
            cur = cur[:-1]

        if cur.startswith(usd):
            cur = cur[1:]

        path += usd + cur

    return path



