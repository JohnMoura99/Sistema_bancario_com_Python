
def menu():
    menu = """
    ==========MENU==========
    [0] Depositar
    [1] Sacar
    [2] Extrato
    [3] Nova conta 
    [4] Listar contas
    [5] Novo usuário
    [6] Sair
    =>"""
    return input((menu))

def depositar(saldo,valor, extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@") 
        
    return saldo, extrato

def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saque):
    excedeu_saldo= valor > saldo
    excedeu_limite= valor > limite
    excedeu_saque= numero_saques >= limite_saque
    
    if excedeu_saldo:
        print("\n@@@ Operação falhou! saldo suficiente. @@@")
    elif excedeu_limite:
         print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saque:
        print("\n@@@ Operação falhou! Limite de saque excedido")
    
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\t{valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
        print(f"\n=== numero de saques hoje: {numero_saques}/3 ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é invalido. @@@")
        
    return saldo, extrato, numero_saques
        
def exibir_extrato(saldo,/,*,extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações.") if not extrato else extrato
    print(extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("===========================================")

def criar_usuario(usuarios):
    cpf = input("informa o CPF(somente numeros) : ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já exite um usuário com esse CPF!@@@")
        return
    
    nome = input("informe o nome completo: ")
    data_nascimento = input("informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o Endereço(logadouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf":cpf, "endereco":endereco })

    print("===== usuário criado com sucesso =====")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação d econta encerrado!")
   
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print (linha)

def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "0":
            valor = float(input("informe o valor do depósito: "))
            
            saldo, extrato, = depositar(saldo, valor, extrato)
        
        elif opcao == "1":
            valor = float(input("informe o valor que deseja sacar: "))
            
            saldo, extrato, numero_saques = sacar(saldo=saldo,
                                   valor=valor,
                                   extrato=extrato,
                                   limite=limite, 
                                   numero_saques=numero_saques,
                                   limite_saque=LIMITE_SAQUE)
            
        elif opcao == "2":
            exibir_extrato(saldo,extrato=extrato) 
        
        elif opcao == "3":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "4":
            listar_contas(contas)

        elif opcao == "5":
            criar_usuario(usuarios)

        
        elif opcao == "6":
            break   
            
        else:
            print("Opção inválida, selecione novamete a opção desejada")
        


if __name__ == "__main__":
    main()










