class Tree_node:
    id = 0
    parent_id = 0
    value = ""
    connect_Parent = True
    def __init__(self,value,num, parent_id):
        self.id = num
        self.parent_id = parent_id
        self.value = value
    def is_statment(self):
        statment = ["if","repeat","assign","read","write"]
        str = self.value.split("\n")
        for token in str:
            if token in statment:
                return True
        return False

    def get_id(self):
        return self.id