from abc import ABC, abstractmethod
from datetime import datetime
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent

class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self#instancia propria do iterador, ele mesmo

    def __next__(self):
        try:
            conta = self.contas[self._index] #acessa o indice atual dentro do array de contas(contas que foi passada ao iterados), que foi passada, ai ele retorna agencia,numero,titular e saldo
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\t{conta.saldo:.2f}
            """
        except IndexError:
            return StopIteration #qaundo n tiver mais item de conta lança o stopiteration
        finally:
            self._index+=1


class Cliente:
    def __init__(self,endereço):
        self.endereço = endereço
        self.contas = []

    def realizar_transacao(self,conta, transacao):
        transacao_do_dia = conta.historico.transacoes_do_dia()
        if len(transacao_do_dia)>= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
       
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereço):
        super().__init__(endereço)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
    def __repr__(self) -> str:#metodo de representação
        return f"<Cliente: ({self.__class__.__name__} : ({self.cpf})>"
        #quando ele é executado, é dessa forma que esta no return que ele vai apresentar pro Python uma instancia desse objeto PessoaFisica
        #é bem parecido com o __str__, a diferença é que pro str é pra um dado mais legivel pra um humano(quando for mostrar algo ao usuario final),e o repr é pra essa questao de logs, vou salvar a informação do meu objeto em um arquivo de texto que vai ser consultado depois, ai quero a representação desse meu objeto em modo texto ai coloco esse __repr__, é legal ele ser um formato unico, pq dessa forma voce consegue identificar unicamente cada instancia de objeto, como a gente so pode ter um usuario por cpf entao coloquei esse texto cocatenando com o cpf. 

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
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:('{self.agencia}','{self.numero}','{self.cliente.nome}')>"

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
              "data": datetime.utcnow().strftime("%d-%m-%y %H:%M:%S"),
            
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
    #FAZER: GERADOR DE RELATORIO

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%y %H:%M:%S").date()#metodo do modulo datetime
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

  
  
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

#para no log sair quanto que depositei(valor), precisamos alterar a forma que nosso deposito,saque e as outras operações elas foram feitas, pra isso precisaria passar "valor" como argumento na função "def depositar", pra isso precisariar tirar as linhas de codigo  valor e transação e colocar no deposito da main

#apos encerrar e iniciar novamente no arquivo de texto os dados do cliente 1 permanece, porem eles não persistem, entao fica salvo no arquivo porem consigo criar outro cliente 1.
# para resolver isso tem que persistir a lista de cliente e de contas da main.
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ROOT_PATH / "log.txt","a") as arquivo:
             arquivo.write( f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}\n")
             
            #modo "a" pq se o arquivo existir ele vai pegar e adicionar novas linhas no final desse arquivo
       
        return resultado

    return envelope


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

@log_transacao
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

@log_transacao
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

@log_transacao
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
    #trasacoes = conta.historico.transacoes
    extrato = " "
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():#filtrar o deposito ou saque
        tem_transacao= True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=========================================")    

@log_transacao
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

@log_transacao
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
     #TODO: alterar implementação, para utilizar a classe ContaIterador
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
