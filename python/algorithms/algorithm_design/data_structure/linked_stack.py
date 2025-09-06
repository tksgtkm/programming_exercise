class Node:

    def __init__(self, item, _next=None):
        self.item = item
        self.next = _next

class Stack:

    def __init__(self):
        self.first = None
        self.n = 0

    def push(self, x) -> None:
        self.first = Node(x, self.first)
        self.n += 1

    def pop(self):
        if self.is_empty():
            raise IndexError('Stack underflow')
        else:
            x = self.first.item
            self.first = self.first.next
            self.n -= 1
            return x
        
    def is_empty(self) -> bool:
        return self.n == 0
    
    def __iter__(self):
        current = self.first
        while current is not None:
            yield current.item
            current = current.next

    def print(self) -> None:
        for x in self:
            print(x, end = ' ')
        print()