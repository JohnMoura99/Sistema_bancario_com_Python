menu = """ 

    [0] Depositar
    [1] Sacar
    [2] Extrato
    [3] Sair

=>"""


saldo = 0
limite_diario = 500
extrato_depositos = []
extrato_saques = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = int(input(menu))

    if opcao == 0:
        print("Depósito")
        valor_deposito = int(input("Qual o valor que deseja depositar? "))
        if valor_deposito > 0:
            saldo+= valor_deposito
            extrato_depositos.append(valor_deposito) 
        else:
            print("Valor invalido,o valor do depósito deve ser positivo!")
    elif opcao == 1:
        print("Saque")
        if numero_saques < LIMITE_SAQUES:
            valor_saque = int(input("Qual o valor deseja sacar? "))
            if valor_saque <= saldo and valor_saque <= limite_diario:
                saldo-= valor_saque
                extrato_saques.append(valor_saque)
                numero_saques += 1
            elif valor_saque > limite_diario:
                print("Limite de saque diario excedito. O limite é R$ 500,00 por saque.")
            else:
                print("Saldo insuficiente para realizar o saque.")
        else:
            print("Limite diário de saques excedido.")    
            
        
    elif opcao == 2:
        print("Extrato")
        print("=====Depositos realizados:=====") 
        for deposito in extrato_depositos:
            print(f"Depósito: R$ {deposito:.2f}")
        print("=====Saques realizados:======")
        for saque in extrato_saques:
            print(f"Saque: R$ {saque:.2f}")
        print(f"Saldo atual: R$ {saldo:.2f}")
        
        
    elif opcao == 3:
        print("Sair")
        break

    else:
        print("Operação invalida, por favor selecione novamente a operação desejada.")



