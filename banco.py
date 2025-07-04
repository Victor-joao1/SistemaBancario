import textwrap

# Lista de usuários e contas
usuarios = []
contas = []

# ---------- FUNÇÕES DE OPERAÇÕES BANCÁRIAS ----------

# DEPÓSITO — argumentos mistos (positional-only e keyword-only)
def deposito(saldo, valor, /, *, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("✅ Depósito realizado com sucesso!")
    else:
        print("❌ Valor inválido para depósito.")
    return saldo, extrato

# SAQUE — todos os argumentos keyword-only
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("❌ Valor inválido.")
    elif valor > saldo:
        print("❌ Saldo insuficiente.")
    elif valor > limite:
        print("❌ Valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("❌ Número máximo de saques atingido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("✅ Saque realizado com sucesso!")
    return saldo, extrato, numero_saques

# EXTRATO
def exibir_extrato(saldo, /, *, extrato):
    print("\n====== EXTRATO ======")
    print(extrato if extrato else "Nenhuma movimentação.")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=====================\n")

# ---------- FUNÇÕES DE USUÁRIO E CONTA ----------

# Buscar usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

# Cadastrar novo usuário
def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()

    # Verifica se só tem números e se não está duplicado
    if not cpf.isdigit():
        print("❌ CPF inválido.")
        return
    if filtrar_usuario(cpf, usuarios):
        print("❌ Já existe um usuário com esse CPF.")
        return

    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Endereço (logradouro - bairro - cidade/UF): ").strip()

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("✅ Usuário cadastrado com sucesso!")

# Cadastrar nova conta bancária
def cadastrar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas.append({
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        })
        print("✅ Conta criada com sucesso!")
    else:
        print("❌ Usuário não encontrado. Cadastre-o primeiro.")

# ---------- PROGRAMA PRINCIPAL ----------

def main():
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    numero_conta = 1

    while True:
        opcao = input(textwrap.dedent("""
        ======== MENU ========
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo Usuário
        [nc] Nova Conta
        [q] Sair
        => """)).lower()

        if opcao == "d":
            valor = float(input("Valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato=extrato)

        elif opcao == "s":
            valor = float(input("Valor do saque: "))
            saldo, extrato, numero_saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            cadastrar_usuario(usuarios)

        elif opcao == "nc":
            cadastrar_conta(AGENCIA, numero_conta, usuarios)
            numero_conta += 1

        elif opcao == "q":
            print("👋 Saindo...")
            break

        else:
            print("❌ Opção inválida!")

# Executa o sistema
main()
