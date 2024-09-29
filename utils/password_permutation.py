import inflect
import random


class PasswordPermutation:
    """
    Classe para gerar permutações de senhas a partir de palavras ou nomes.

    Atributos:
    -----------
    inflect_object : inflect.engine
        Objeto da biblioteca inflect para manipulação de palavras, como conversão para plural.
    random_state : int
        Valor opcional que define o estado da semente aleatória usada para geração de variações.

    Métodos:
    --------
    __init__(random_state=42):
        Inicializa a classe com um objeto inflect e define o estado da semente aleatória.
    get_permutations_from_database(database_path, max_num=10):
        Gera uma lista de permutações de palavras a partir de um arquivo de texto.
    get_possible_passwords_from_names(username, name, max_num=10):
        Gera uma lista de possíveis senhas com base em um nome e nome de usuário fornecidos.
    """

    def __init__(self, random_state=42):
        """
        Inicializa o objeto PasswordPermutation com um motor inflect e define a semente aleatória.

        Parâmetros:
        -----------
        random_state : int, opcional
            Valor da semente aleatória para garantir reprodutibilidade (padrão: 42).
        """
        self.inflect_object = inflect.engine()
        random.seed(random_state)

    def get_permutations_from_database(self, database_path, max_num=10):
        """
        Gera permutações de palavras contidas em um arquivo de texto.

        Para cada palavra no arquivo, este método cria diversas variações, incluindo:
        - Inicial maiúscula.
        - Palavra invertida.
        - Inversão com inicial maiúscula.
        - Troca de letras por números (ex: "o" por "0", "l" por "1").
        - Pluralização.
        - Todas as combinações possíveis de letras maiúsculas.

        Parâmetros:
        -----------
        database_path : str
            Caminho para o arquivo de texto contendo as palavras de origem.
        max_num : int, opcional
            Número máximo de permutações a serem retornadas (padrão: 10).

        Retorna:
        --------
        list
            Uma lista contendo até max_num de permutações de senhas.
        """
        with open(database_path) as file:
            lines = file.readlines()
            lines = [line.removesuffix("\n") for line in lines]

        new_lines = set()

        for line in lines:
            # Adiciona palavra com inicial maiúscula
            upper_case_line = line.replace(line[0], line[0].upper(), 1)
            new_lines.add(upper_case_line)

            # Adiciona palavra inversa
            reverse_line = line[::-1]
            new_lines.add(reverse_line)

            # Adiciona palavra inversa com inicial maiúscula
            upper_case_reversed = upper_case_line[::-1]
            new_lines.add(upper_case_reversed)

            # Adiciona palavra com troca de letras por números parecidos
            change_letters_line = (
                line.replace("o", "0")
                .replace("O", "0")
                .replace("l", "1")
                .replace("z", "2")
                .replace("s", "5")
                .replace("S", "5")
            )
            new_lines.add(change_letters_line)

            # Adiciona palavra no plural
            plural_line = self.inflect_object.plural(line)
            new_lines.add(plural_line)

            # Adiciona todas as possibilidades de letra maiúscula na palavra
            for i in range(len(line)):
                new_line = line[:i] + line[i].upper() + line[i + 1 :]
                new_lines.add(new_line)

        return random.sample(list(new_lines), k=max_num)

    def get_possible_passwords_from_names(self, username, name, max_num=10):
        """
        Gera uma lista de possíveis senhas a partir de um nome de usuário e um nome completo.

        As variações incluem:
        - Combinações de nome e números.
        - Iniciais do nome.
        - Variações com letras maiúsculas e minúsculas.
        - Nome invertido.
        - Combinações de iniciais e sobrenomes.
        - Adição de hífens e números.

        Parâmetros:
        -----------
        username : str
            Nome de usuário para base das combinações de senhas.
        name : str
            Nome completo da pessoa (primeiro nome e último nome).
        max_num : int, opcional
            Número máximo de possíveis senhas a serem retornadas (padrão: 10).

        Retorna:
        --------
        list
            Uma lista de possíveis senhas.
        """
        first_name, last_name = name.split(" ")[0], name.split(" ")[-1]
        initials = "".join([name[0] for name in name.split()])

        passwords = set()

        passwords.add(username)

        # Adicionando números ao nome de usuário
        for i in range(10):
            passwords.add(f"{username}{i}")

        # Adicionando variações com números
        for i in range(1, 4):
            passwords.add(f"{username}{i * '1'}")

        # Variações com nome e números
        for i in range(1, 4):
            passwords.add(f"{name}{i * '1'}")

        # Variação com Nome e 2 números
        name_with_capital_initial = first_name.lower().replace(name.lower()[0], name[0], 1)
        for i in range(1, 4):
            for j in range(1, 4):
                passwords.add(f"{name_with_capital_initial}{i}{j}")

        # Iniciais
        passwords.add(initials.lower())
        passwords.add(initials.upper())

        # Nomes com letras maiúsculas
        passwords.add(first_name.lower() + last_name.lower())
        passwords.add(first_name.upper() + last_name.lower())
        passwords.add(first_name.lower() + last_name.upper())
        passwords.add(first_name.upper() + last_name.upper())

        # Combinações de partes do nome
        passwords.add(first_name + last_name)
        passwords.add(last_name + first_name)
        passwords.add(last_name[::-1])  # Último nome invertido
        passwords.add(first_name[::-1])  # Primeiro nome invertido

        # Combinando iniciais e sobrenome
        passwords.add(initials + last_name.lower())
        passwords.add(initials + last_name.upper())

        # Variantes com hífen
        passwords.add(f"{first_name}-{last_name}")
        passwords.add(f"{last_name}-{first_name}")

        # Adicionando combinações comuns
        common_variants = [
            f"{first_name[0]}{last_name}",
            f"{last_name[0]}{first_name}",
            f"{first_name[0]}{last_name[0]}",
            f"{username}{first_name}",
            f"{username}{last_name}",
        ]

        passwords.update(common_variants)
        passwords = list(passwords)
        passwords.sort()

        max_num = min(max_num, len(passwords))
        
        return random.sample(passwords, k=max_num)
