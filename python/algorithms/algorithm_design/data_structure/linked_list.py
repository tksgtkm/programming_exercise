class Node:

    def __init__(self, item, _next=None):
        self.item = item
        self.next = _next

class List:

    def __init__(self):
        self.head = None
    
    def is_empty(self) -> bool:
        return self.head is None
    
    def __contains__(self, x):
        return self.search(x) is not None
    
    def search(self, x) -> Node:
        p = self.head

        while p is not None and p.item != x:
            p = p.next
        
        return p
    
    def insert(self, x) -> None:
        self.head = Node(x, self.head)
    
    def delete(self, x) -> None:
        pred = None
        p = self.head

        while p is not None and p.item != x:
            pred = p
            p = p.next

        if p is not None:
            if pred is None:
                self.head = p.next
            else:
                pred.next = p.next
            p.next = None
        print('deleted: ', x)

    def delete_r(self, x) -> None:
        self.head = self._delete_r(self.head, x)
    
    def _delete_r(self, n, x) -> Node:
        if n is None:
            return None
        elif n.item == x:
            return n.next
        else:
            n.next = self._delete_r(n.next, x)
            return n
        
    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.item
            current = current.next

    def print(self) -> None:
        for x in self:
            print(x, end = ' ')
        print()

l = List()
l.insert(1)
l.insert(2)
l.insert('3')
l.print()

print(l.search(2).item)

l.delete(2)
l.print()

l.search(2)