import json

# ItemMenu
class ItemMenu:
    def __init__(self, nome, preco, descricao):
        self.__nome = nome
        self.__preco = preco
        self.__descricao = descricao

    def calcular_preco(self):
        return self.__preco

    def exibir_detalhes(self, exibir_descricao=False):
        if exibir_descricao:
            return f"Item: {self.__nome} | Preço: R${self.__preco:.2f} | Descrição: {self.__descricao}"
        else:
            return f"Item: {self.__nome} | Preço: R${self.__preco:.2f}"


    @property
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @property
    def descricao(self):
        return self.__descricao


# Subclasse: Bebida
class Bebida(ItemMenu):
    def __init__(self, nome, preco, descricao):
        super().__init__(nome, preco, descricao)

    def calcular_preco(self):
        return super().calcular_preco() * 1.1  # 10% de taxa de serviço


# Subclasse: Comida
class Comida(ItemMenu):
    def __init__(self, nome, preco, descricao):
        super().__init__(nome, preco, descricao)


# Subclasse: Sobremesa
class Sobremesa(ItemMenu):
    def __init__(self, nome, preco, descricao):
        super().__init__(nome, preco, descricao)


# Classe Pedido
class Pedido:
    def __init__(self):
        self.__itens = []

    def adicionar_item(self, item):
        self.__itens.append(item)

    def calcular_total(self):
        return sum(item.calcular_preco() for item in self.__itens)

    def exibir_pedido(self):
        detalhes = "\n".join(item.exibir_detalhes() for item in self.__itens)
        total = f"Total do pedido: R${self.calcular_total():.2f}"
        return f"{detalhes}\n{total}"

    def limpar_pedido(self):
        self.__itens = []


# Classe Restaurante
class Restaurante:
    def __init__(self):
        self.__menu = []
        self.__pedidos = []

    def adicionar_ao_menu(self, item):
        self.__menu.append(item)

    def exibir_menu(self):
        return "\n".join(f"{i+1}. {item.exibir_detalhes(exibir_descricao=True)}" for i, item in enumerate(self.__menu))

    def realizar_pedido(self, pedido):
        self.__pedidos.append(pedido)

    def salvar_pedidos(self, arquivo="pedidos.json"):
        with open(arquivo, "w") as f:
            pedidos_serializados = [
                {
                    "itens": [item.exibir_detalhes(exibir_descricao=False) for item in pedido._Pedido__itens],
                    "total": pedido.calcular_total()
                }
                for pedido in self.__pedidos
            ]
            json.dump(pedidos_serializados, f, indent=4)

    def carregar_menu(self, arquivo="menu.json"):
        try:
            with open(arquivo, "r") as f:
                dados_menu = json.load(f)
                for item in dados_menu:
                    if item["tipo"] == "Bebida":
                        self.adicionar_ao_menu(
                            Bebida(item["nome"], item["preco"], item["descricao"])
                        )
                    elif item["tipo"] == "Comida":
                        self.adicionar_ao_menu(
                            Comida(item["nome"], item["preco"], item["descricao"])
                        )
                    elif item["tipo"] == "Sobremesa":
                        self.adicionar_ao_menu(
                            Sobremesa(item["nome"], item["preco"], item["descricao"])
                        )
        except FileNotFoundError:
            print("Arquivo de menu não encontrado!")



def menu_interativo():
    restaurante = Restaurante()


    restaurante.adicionar_ao_menu(Bebida("Coca-Cola", 5.00, "Refrigerante gelado"))
    restaurante.adicionar_ao_menu(Bebida("Long neck HEINEKEN", 12.00, "Cerveja gelada"))
    restaurante.adicionar_ao_menu(Comida("X-salada", 40.00, "Pão brioche, hambúrguer, queijo cheedar, alface e tomate"))
    restaurante.adicionar_ao_menu(Comida("Porção batata frita", 25.00, "Batatas fritas crocantes"))
    restaurante.adicionar_ao_menu(Sobremesa("Milk-shake", 17.50, "Milk-shake cremoso de baunilha"))

    pedido_atual = Pedido()

    while True:
        print("\n=== BUTECO DO BARTHO ===")
        print("1. Exibir Menu")
        print("2. Adicionar Item ao Pedido")
        print("3. Ver Pedido Atual")
        print("4. Finalizar Pedido")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- Menu ---")
            print(f"{'ID':<4} {'Item':<20} {'Preço':>10} {'Descrição':<25}")
            print("-" * 70)
            for index, item in enumerate(restaurante._Restaurante__menu, 1):
                print(f"{index:<4} {item.nome:<20} R${item.preco:>9.2f} {item.descricao:<25}")
        elif opcao == "2":
            print("\n--- Adicionar ao Pedido ---")


            print(f"{'ID':<4} {'Item':<20} {'Preço':>10}")
            print("-" * 35)
            for index, item in enumerate(restaurante._Restaurante__menu, 1):
                print(f"{index:<4} {item.nome:<20} R${item.preco:>9.2f}")

            escolha = input("Digite o número do item que deseja adicionar: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(restaurante._Restaurante__menu):
                item_escolhido = restaurante._Restaurante__menu[int(escolha) - 1]
                pedido_atual.adicionar_item(item_escolhido)
                print(f"{item_escolhido.nome} adicionado ao pedido!")
            else:
                print("Opção inválida!")
        elif opcao == "3":
            print("\n--- Pedido Atual ---")
            print(pedido_atual.exibir_pedido())
        elif opcao == "4":
            print("\n--- Finalizando Pedido ---")
            restaurante.realizar_pedido(pedido_atual)
            restaurante.salvar_pedidos()
            print("Pedido finalizado e enviado para a cozinha!")
            pedido_atual.limpar_pedido()
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")



if __name__ == "__main__":
    menu_interativo()
