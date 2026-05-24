from abc import ABC, abstractmethod
from datetime import datetime


# ==================== INTERFACE TRANSACAO ====================

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: "Conta") -> None:
        pass


# ==================== DEPOSITO E SAQUE ====================

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> None:
        sucesso = conta.depositar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: "Conta") -> None:
        sucesso = conta.sacar(self._valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ==================== HISTORICO ====================

class Historico:
    def __init__(self):
        self._transacoes: list = []

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })


# ==================== CONTA ====================

class Conta:
    def __init__(self, numero: int, cliente: "Cliente"):
        self._saldo: float = 0.0
        self._numero: int = numero
        self._agencia: str = "0001"
        self._cliente: "Cliente" = cliente
        self._historico: Historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: "Cliente", numero: int) -> "Conta":
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> "Cliente":
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("\nOperacao falhou! O valor informado e invalido.")
            return False
        if valor > self._saldo:
            print("\nOperacao falhou! Saldo insuficiente.")
            return False
        self._saldo -= valor
        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("\nOperacao falhou! O valor informado e invalido.")
            return False
        self._saldo += valor
        print(f"\nDeposito de R$ {valor:.2f} realizado com sucesso!")
        return True


# ==================== CONTA CORRENTE ====================

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: "Cliente", limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite: float = limite
        self._limite_saques: int = limite_saques

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def sacar(self, valor: float) -> bool:
        saques_realizados = len([
            t for t in self.historico.transacoes
            if t["tipo"] == "Saque"
        ])

        if valor > self._limite:
            print(f"\nOperacao falhou! O valor excede o limite de R$ {self._limite:.2f} por saque.")
            return False

        if saques_realizados >= self._limite_saques:
            print(f"\nOperacao falhou! Numero maximo de saques ({self._limite_saques}) excedido.")
            return False

        return super().sacar(valor)

    def __str__(self):
        return (
            f"Agência:\t{self.agencia}\n"
            f"C/C:\t\t{self.numero}\n"
            f"Titular:\t{self.cliente.nome}"
        )


# ==================== CLIENTE ====================

class Cliente:
    def __init__(self, endereco: str):
        self._endereco: str = endereco
        self._contas: list = []

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def contas(self) -> list:
        return self._contas

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)


# ==================== PESSOA FISICA ====================

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self._cpf: str = cpf
        self._nome: str = nome
        self._data_nascimento: str = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento


# ==================== FUNÇÕES AUXILIARES ====================

def menu() -> str:
    menu_texto = """
===== Bradesco =====
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q] Sair
=> """
    return input(menu_texto)


def filtrar_cliente(cpf: str, clientes: list) -> Cliente | None:
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None


def recuperar_conta_cliente(cliente: Cliente) -> Conta | None:
    if not cliente.contas:
        print("\nCliente nao possui conta!")
        return None
    # TODO: permitir escolha entre multiplas contas
    return cliente.contas[0]


def depositar(clientes: list) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente nao encontrado!")
        return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes: list) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente nao encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: list) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente nao encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n===== EXTRATO =====")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Nao foram realizadas movimentacoes.")
    else:
        for t in transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f}  ({t['data']})")

    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("===================")


def criar_cliente(clientes: list) -> None:
    cpf = input("Informe o CPF (somente numeros): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJa existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    clientes.append(cliente)
    print(f"\nCliente {nome} criado com sucesso!")


def criar_conta(numero_conta: int, clientes: list, contas: list) -> None:
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente nao encontrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(f"\nConta {numero_conta} criada para {cliente.nome}!")


def listar_contas(contas: list) -> None:
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
    print("\n===== CONTAS =====")
    for conta in contas:
        print(conta)
        print("-" * 20)


# ==================== MAIN ====================

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu().strip().lower()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nAte logo!")
            break
        else:
            print("\nOpcao invalida, tente novamente.")


if __name__ == "__main__":
    main()
