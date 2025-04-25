if __name__ == '__main__':
    s = "Friday"
    number = "trei"
    try:
        nb = int(number)
        print(nb)
    except ValueError as exc:
        print(f"Something went wrong: {exc}")

    print(f'It\'s {s} {number}rd')

    lst = [1, 2, 3, 4, 5, 5]
    second_lst = [6, 7]
    lst.extend(second_lst)
    print(lst)

    fruits = ['apple', 'orange', 'pear']
    for i, f in enumerate(fruits):
        print(f"{i = }, {f = }")

    for i in reversed(range(3, 10, 2)):
        print(i)

    t = (1, 2, 3, 4, 5)
    l = [(1, 2), (5, 6), (3, 19)]
    a = [(0, "ceva"), (1, "altceva")]

    for _, name in l:
        print(f"Point: {name = }")

    st = {"potatoes", "carrots", "tomatoes"}
    d = {"potatoes": 2, "carrots": 5, "tomatoes": 10, "onions": 12}
    print(d)

    for k, v in d.items():
        print(f"{k = } {v = }")

    for veg in d:
        print(f"{veg} {d[veg]}")

    if "carrots" in d:
        print("we have carrots")
    else:
        print("we have no carrots")

    for ch in s:
        print(ch)

    for veg in st:
        for ch in veg:
            print(ch)

    name = "Cora"
    print(name)
    name_lst = list(name)
    print("".join(name_lst))

    
