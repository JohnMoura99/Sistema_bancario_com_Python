from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self,endereço):
        self.endereço = endereço
        self.contas = []

    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereço):
        super().__init__(endereço)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:  
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente) #retorna uma instancia de conta#construtor
    
    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self,valor):
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor>saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! O valor informado excede o saldo. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso !!! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é invalido. @@@")

        return False   

    def depositar(self,valor):
        if valor > 0:
            self.saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! o valor informado é invalido. @@@") 
            return False
        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques= limite_saques

    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] ==  Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques 

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
              "tipo": transacao.__class__.__name__,
              "valor": transacao.valor,
              "data": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
            
            }
        )
  
  
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self,conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)##


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)##


def menu():
    menu = """\n
    =============== MENU ===============
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar Contas
    [6]\tNovo usuário
    [0]\tSair
    ==>"""
    return input(menu)

def filtrar_cliente(cpf, clientes):
    clientes_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrado[0] if clientes_filtrado else None
#cliente.cpf é uma instancia da classe Cliente

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0] #ele passando da  validação acima, rertona para o depositar  a primeira conta


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("informe o valor do depósito: "))
    transacao = Deposito(valor) #instancia da classe #com essa trasação informa que de fato o que quer fazer é um deposito

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return#Se conta for None, a função retorna, encerrando o processo de depósito.

    cliente.realizar_transacao(conta, transacao)#instancia da classe Cliente#metodo da classe Cliente.
    #vai pegar a atransação e pegar o metodo para realizar a transação


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============== EXTRATO ==============")
    trasacoes = conta.historico.transacoes

    extrato = " "
    if not trasacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for trasacao in trasacoes:
            extrato += f"\n{trasacao['tipo']}:\n\tR${trasacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=========================================")    


def criar_cliente(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("informe a data de nascimento (dd-mm-aaaa): ")
    endereço = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereço=endereço)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)#atuliza a lista de contas do cliente

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
     for conta in contas:
         print("=" * 100)
         print(str(conta))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)
        
        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "6":
            criar_cliente(clientes)

             
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,clientes,contas)

        elif opcao == "5":
            listar_contas(contas)
        
        elif opcao == "0":
            print("Saindo...")
            print("Sistema fechado")
            break
            

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")



main()
