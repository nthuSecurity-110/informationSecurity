L=['i','ip','ipp','ippp']

for item in L:
    exec("aaa = input('Please input missing parameter(" + item +"):')")
    print(f'item: {aaa}')