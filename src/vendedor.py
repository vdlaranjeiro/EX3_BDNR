def create_vendedor(db):
    print('\nInsira as informações do vendedor')
    nome = input('Nome do vendedor ou da loja: ')

    verificacaoVendedor = 0
    while(verificacaoVendedor != 1):
        pessoaFisicaOuJuridica = input('Pessoa Física ou Jurídica? F/J ').upper()
        if(pessoaFisicaOuJuridica == 'F'):
            cpf = input('CPF: ')
            cnpj = ""
            verificacaoVendedor = 1
        elif(pessoaFisicaOuJuridica == 'J'):
            cnpj = input('CNPJ: ')
            cpf = ""
            verificacaoVendedor = 1
        else:
            print('Opção inválida. Selecione F para pessoa física ou J para pessoa jurídica.')

    enderecos = []
    keyEnderecos = 0
    while(keyEnderecos != 'N'):
        print('\nDigite seu endereço: ')
        cep = input('CEP: ')
        rua = input('Rua: ')
        numero = input('Número: ')
        bairro = input('Bairro: ')
        cidade = input('Cidade: ')
        estado = input('Estado: ')

        endereco = {
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }
        enderecos.append(endereco)
        keyEnderecos = input('\nDeseja inserir mais um endereço? S/N ').upper()

    contatos = {}
    contatos["telefones"] = []
    keyTelefones = 0
    while(keyTelefones != 'N'):
        telefone = input('DDD + Telefone: ')
        contatos["telefones"].append(telefone)
        keyTelefones = input('\nDeseja cadastrar mais um telefone? S/N ').upper()

    contatos["email"] = input('Email: ')
    senha = input('Senha: ')

    vendedor = {
        "nome": nome,
        "cpf": cpf,
        "cnpj": cnpj,
        "enderecos": enderecos,
        "contatos": contatos,
        "senha": senha
    }

    mycol = db.Vendedores
    insert = mycol.insert_one(vendedor)
    print(f'\nVendedor cadastrado no id: {insert.inserted_id}')

    return

def delete_vendedor(db, vendedor):

    excluirVendedor = input('Deseja realmente excluir sua conta? S/N ').upper()
    if(excluirVendedor == 'S'):
        myquery = {
            "$or": [
                {"cpf": vendedor['cpf']},
                {"cnpj": vendedor['cnpj']}
            ]
        }

        colecaoVendedores = db.Vendedores
        mydoc = colecaoVendedores.delete_one(myquery)
        print(f'Deletando o usuário {mydoc}')
        return True
    elif(excluirVendedor == 'N'):
        print('Operação cancelada')
        return False
    else:
        print('Opção não entendida')
        return False
    
def read_vendedor(db, vendedor):

    print("\nInformações do vendedor:")
    if len(vendedor["cpf"]): print(f'CPF: {vendedor["cpf"]}')
    if len(vendedor["cnpj"]): print(f'CPF: {vendedor["cnpj"]}')
    print(f"Nome: {vendedor['nome']}")

    print("Endereços:")
    for endereco in vendedor['enderecos']:
        print(f"\nCEP: {endereco['cep']}")
        print(f"Rua: {endereco['rua']}")
        print(f"Número: {endereco['numero']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Cidade: {endereco['cidade']}")
        print(f"Estado: {endereco['estado']}")

    print("\nContatos:")
    print(f"Email: {vendedor['contatos']['email']}")
    print("Telefones:")
    for telefone in vendedor['contatos']['telefones']:
        print(telefone)

    return

def update_vendedor(db, vendedor):

    print(f'Editando informações de {vendedor["nome"]}. Aperte ENTER para pular um campo')
    nomeCompleto = input('Novo nome: ')
    if len(nomeCompleto):
        vendedor["nome"] = nomeCompleto

    keyUpdateEnderecos = input('\nDeseja atualizar os endereços? S/N ').upper()
    if(keyUpdateEnderecos == 'S'):
        keyOpcaoEnderecos = 0
        while(keyOpcaoEnderecos != 'C'):
            print('1 - Adicionar um endereço')
            print('2 - Remover um endereço existente')
            keyOpcaoEnderecos = input('Escolha uma opção: (C para cancelar) ').upper()

            match keyOpcaoEnderecos:
                case '1':
                    endereco = {
                        "cep": input("CEP:"),
                        "rua": input('Rua: '),
                        "numero": input('Numero: '),
                        "bairro": input('Bairro: '),
                        "cidade": input('Cidade: '),
                        "estado": input('Estado: ')
                    }

                    vendedor["enderecos"].append(endereco)
                    print('Endereço adicionado!\n')
                case '2':
                    contadorEndereco = 1
                    for endereco in vendedor["enderecos"]:
                        print(f'\nEndereço {contadorEndereco}')
                        print(f"CEP: {endereco['cep']}")
                        print(f"Rua: {endereco['rua']}")
                        print(f"Número: {endereco['numero']}")
                        print(f"Bairro: {endereco['bairro']}")
                        print(f"Cidade: {endereco['cidade']}")
                        print(f"Estado: {endereco['estado']}")

                        contadorEndereco+=1
                    
                    enderecoEscolhido = input('Escolha o endereço que você deseja remover: ')
                    if enderecoEscolhido.isdigit():
                        enderecoEscolhido = int(enderecoEscolhido)
                        if enderecoEscolhido > contadorEndereco:
                            print('Endereço inválido\n')
                        else:
                            vendedor["enderecos"].pop(enderecoEscolhido - 1)
                            print('Endereço removido!\n')
                    else:
                        print('Endereço inválido\n')

    keyUpdateTelefones = input('\nDeseja atualizar os telefones? S/N ').upper()
    if(keyUpdateTelefones == 'S'):
        keyOpcaoTelefones = 0
        while(keyOpcaoTelefones != 'C'):
            print('1 - Adicionar um telefone')
            print('2 - Remover um telefone existente')
            keyOpcaoTelefones = input('Escolha uma opção: (C para cancelar) ').upper()

            match keyOpcaoTelefones:
                case '1':
                    novoTelefone = input('Digite o novo telefone (DDD + Número): ')
                    vendedor["contatos"]["telefones"].append(novoTelefone)
                    print('Telefone adicionado!')
                case '2':
                    contadorTelefones = 1
                    for telefone in vendedor["contatos"]["telefones"]:
                        print(f'Telefone {contadorTelefones}')
                        print(telefone)

                        contadorTelefones+=1

                    telefoneEscolhido = input('Escolha o telefone que você deseja remover: ')
                    if telefoneEscolhido.isdigit():
                        telefoneEscolhido = int(telefoneEscolhido)
                        if telefoneEscolhido > contadorTelefones:
                            print('Telefone inválido\n')
                        else:
                            vendedor["contatos"]["telefones"].pop(telefoneEscolhido - 1)
                            print('Telefone removido!\n')
                    else:
                        print('Telefone inválido\n')

    email = input('Novo email: ')
    if len(email):
        vendedor["contatos"]["email"] = email
    
    novasInformacoes = {"$set": vendedor}

    colecaoVendedores = db.Vendedores
    myquery = {
        "$or": [
            {"cpf": vendedor['cpf']},
            {"cnpj": vendedor['cnpj']}
        ]
    }
    colecaoVendedores.update_one(myquery, novasInformacoes)
    print('\nInformações atualizadas com sucesso!')
    
    return

