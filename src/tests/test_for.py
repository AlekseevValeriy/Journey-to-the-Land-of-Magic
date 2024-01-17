class C:
    def __init__(self):
        self._arr = ['y', 'a', 'n', 'd', 'e', 'x']

    def __iter__(self):
        return iter(self._arr)


class C2:
    def __iter__(self):
        i = 10
        while i < 15:
            yield i
            i += 1


print(*C())
print(*C2())