

class PriorityTable:
    def __init__(self, token_types: list[str] = []):
        self.table = {}
        self.lowest_priority = 0

        for token_type in token_types:
            self.push(token_type)

    def push(self, token_type):
        self.table[token_type] = self.lowest_priority
        self.lowest_priority += 1
    
    def __getitem__(self, key):
        if key:
            return self.table[key]
        else:
            return self.lowest_priority
