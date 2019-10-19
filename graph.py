import consts

class Node:
    def __init__(self, name, category, prev_node=None):
        self.name = name
        self.category = category
        self.visited = False
        self.prev = prev_node
        self.next = None

    def get_name(self):
        return self.name

    def already_visited(self):
        return self.visited

    def get_prev_node(self):
        return self.prev

    def get_next_node(self):
        return self.next


class BotNode(Node):
    def __init__(self, name, category, greeting, prev_node=None):
        super(Node, self).__init__(name, category, prev_node)
        self.greeting = greeting

    def get_greeting(self):
        return self.greeting


class CityNode(Node):

    def __init__(self, name, month, category, dates, prev_node):
        super(CityNode, self).__init__(name)
        self.visited = None
        self.name = name
        self.category = category
        self.month = month
        self.dates = dates
        self.prev = prev_node
        self.next = None
        self.checkin = None
        self.checkout = None
        self.address = None
        self.url = None
        self.summary = None


class Graph:
    def __init__(self):
        self.head = None
        self.tail = None
        self.num_vertices = 0

    def add_vertex(self, node):
        self.num_vertices += 1

    def create_graph(self):
        bot = list(BotNode(name=key, category=key, prev_node=None, greeting=consts.BOT_MSGS[key])
                   for key in consts.BOT_MSGS.keys())
        print(bot)
        # self.add_node(bot)

    def add_node(self, new_node):
        if self.head is None:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node

    def get_node_from_list(self, node_list, name):
        print(node_list)

    def get_current_position(self):
        current_node = self.head
        while current_node.visited is True:
            current_node = current_node.next
        return current_node



