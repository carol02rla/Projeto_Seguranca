class FileHandler:

    data = None

    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = file.read()

    def get_users(self):
        lines = self.data.splitlines()
        users = []
        for line in lines:
            users.append(line.split(" ")[-1])

        return users

    def get_matriculas(self):
        lines = self.data.splitlines()
        mat = []
        for line in lines:
            mat.append(line.split(" ")[0])

        return mat
    
    def get_nomes(self):
        lines = self.data.splitlines()
        mat = []
        for line in lines:
            mat.append(line.split(" ")[1])

        return mat