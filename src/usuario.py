from datetime import datetime
import json
import uuid

def create_usuario(db, conexaoRedis):
    print('\nInsira as informações do usuário')
    cpf = input('CPF: ')
    nomeCompleto = input('Nome completo: ')

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
    favoritos = []
    compras = []

    usuario = {"cpf": cpf, "nome": nomeCompleto, "enderecos": enderecos, "contatos": contatos, "senha": senha, "favoritos": favoritos, "compras": compras}
    
    mycol = db.Usuarios
    insert = mycol.insert_one(usuario)
    
    print(f'\nUsuário cadastrado no id: {insert.inserted_id}')
    return

def delete_usuario(db, conexaoRedis, chaveUsuario, usuario):
    confirmacaoExclusao = input('Deseja realmente excluir sua conta? S/N ').upper()

    if(confirmacaoExclusao == 'S'):
        myquery = {"cpf": usuario['cpf']}
        colecaoUsuarios = db.Usuarios

        colecaoUsuarios.delete_one(myquery)
        conexaoRedis.delete(chaveUsuario)
        conexaoRedis.delete(f"{chaveUsuario}-favoritos")
        conexaoRedis.delete(f"{chaveUsuario}-compras")

        print('Conta excluída com sucesso!')
        return True
    elif(confirmacaoExclusao == 'N'):
        print('Operação cancelada')
        return False
    else:
        print('Opção não entendida')
        return False

def read_usuario(usuario):  
    print("\nInformações do usuário:")
    print(f"CPF: {usuario['cpf']}")
    print(f"Nome: {usuario['nome']}")

    print("Endereços:")
    for endereco in usuario['enderecos']:
        print(f"\nCEP: {endereco['cep']}")
        print(f"Rua: {endereco['rua']}")
        print(f"Número: {endereco['numero']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Cidade: {endereco['cidade']}")
        print(f"Estado: {endereco['estado']}")

    print("\nContatos:")
    print(f"Email: {usuario['contatos']['email']}")
    print("Telefones:")
    for telefone in usuario['contatos']['telefones']:
        print(telefone)

    print("\nFavoritos:")
    for favorito in usuario['favoritos']:
        print(f'\nNome: {favorito["nome"]}')
        print(f'Descrição: {favorito["descricao"]}')
        print(f'Valor: {favorito["valor"]}')

    print("\nCompras:")
    for compra in usuario['compras']:
        print(f'\nNome: {compra["nome_produto"]}')
        print(f'Descrição: {compra["descricao_produto"]}')
        print(f'Quantidade: {compra["quantidade"]}')
        print(f'Valor: {compra["valor_compra"]}')
        print(f'Data: {compra["data_compra"]}')
    
    return

def update_usuario(db, mydoc):
    
    print(f'Editando informações de {mydoc["nome"]}. Aperte ENTER para pular um campo')
    nomeCompleto = input('Novo nome: ')
    if len(nomeCompleto):
        mydoc["nome"] = nomeCompleto

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
                        "cep": input('CEP: '),
                        "rua": input('Rua: '),
                        "numero": input('Numero: '),
                        "bairro": input('Bairro: '),
                        "cidade": input('Cidade: '),
                        "estado": input('Estado: ')
                    }

                    mydoc["enderecos"].append(endereco)
                    print('Endereço adicionado!\n')
                case '2':
                    contadorEndereco = 1
                    for endereco in mydoc["enderecos"]:
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
                            mydoc["enderecos"].pop(enderecoEscolhido - 1)
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
                    mydoc["contatos"]["telefones"].append(novoTelefone)
                    print('Telefone adicionado!')
                case '2':
                    contadorTelefones = 1
                    for telefone in mydoc["contatos"]["telefones"]:
                        print(f'Telefone {contadorTelefones}')
                        print(telefone)

                        contadorTelefones+=1

                    telefoneEscolhido = input('Escolha o telefone que você deseja remover: ')
                    if telefoneEscolhido.isdigit():
                        telefoneEscolhido = int(telefoneEscolhido)
                        if telefoneEscolhido > contadorTelefones:
                            print('Telefone inválido\n')
                        else:
                            mydoc["contatos"]["telefones"].pop(telefoneEscolhido - 1)
                            print('Telefone removido!\n')
                    else:
                        print('Telefone inválido\n')

    email = input('Novo email: ')
    if len(email):
        mydoc["contatos"]["email"] = email
    
    novasInformacoes = {"$set": mydoc}
    colecaoUsuarios = db.Usuarios
    usuario = {"cpf": mydoc['cpf']}
    colecaoUsuarios.update_one(usuario, novasInformacoes)
    print('\nInformações atualizadas com sucesso!')

    return

def compra_usuario(db, conexaoRedis, chaveUsuario, usuario):

    nomeProduto = input('Qual produto deseja comprar? ')
    colecaoProdutos = db.Produtos
    queryProduto = {"nome": {"$regex": nomeProduto, "$options": "i"}}
    produtos = colecaoProdutos.find(queryProduto)
    produtos = list(produtos)

    if not(produtos):
        print('Produto não encontrado')
    else:
        for produto in produtos:
            print('\nProdutos encontrados:')
            print(f'\nCódigo: {produto["_id"]}')
            print(f'Nome: {produto["nome"]}')
            print(f'Descrição: {produto["descricao"]}')
            print(f'Valor: {produto["valor"]}')

        verificacaoCodigoProduto = 0
        produtoEscolhido = {}
        while(verificacaoCodigoProduto != 1):
            idProdutoEscolhido = input('Digite o código do produto que deseja comprar: ')
            if(idProdutoEscolhido.isnumeric()):
                produtoEscolhido = next((produto for produto in produtos if produto["_id"] == int(idProdutoEscolhido)), None)
                if(produtoEscolhido):
                    verificacaoCodigoProduto = 1
                else:
                    print('Código inválido')
            else:
                print('Código inválido')

        verificacaoQuantidadeProduto = 0
        quantidadeDisponivel = produtoEscolhido["quantidade"]
        while(verificacaoQuantidadeProduto != 1):
            print(f'\nQuantidade disponível: {quantidadeDisponivel}')
            quantidadeEscolhida = input('Quantas unidades deseja comprar? ')

            if(quantidadeEscolhida.isnumeric()):
                quantidadeEscolhida = int(quantidadeEscolhida)
                if(quantidadeEscolhida > quantidadeDisponivel):
                    print('Quantidade indisponível')
                else:
                    verificacaoQuantidadeProduto = 1
            else:
                print('Digite uma quantidade válida.')

        print(f'\nSua compra: ')
        print(f'Produto: {produtoEscolhido["nome"]}')
        print(f'Quantidade: {quantidadeEscolhida}')
        print(f'Valor: {produtoEscolhido["valor"] * quantidadeEscolhida}')

        confirmarCompra = input('\nConfirmar compra? S/N ').upper()
        if(confirmarCompra == 'S'):
            dataAtual = datetime.now()
            compra = {
                "_id": str(uuid.uuid4()),
                "id_produto": produtoEscolhido["_id"],
                "nome_produto": produtoEscolhido["nome"],
                "descricao_produto": produtoEscolhido["descricao"],
                "quantidade": quantidadeEscolhida,
                "valor_compra": produtoEscolhido["valor"] * quantidadeEscolhida,
                "data_compra": dataAtual.strftime('%d/%m/%Y %H:%M')
            }
            
            #Atualização da lista no redis
            compra = json.dumps(compra)
            conexaoRedis.rpush(f"{chaveUsuario}-compras", compra)

            #Atualização da coleção no mongodb com os dados do redis
            comprasUsuarioRedis = conexaoRedis.lrange(f"{chaveUsuario}-compras", 0, -1)
            comprasUsuario = []

            if(comprasUsuarioRedis):
                for compra in comprasUsuarioRedis:
                    compra = json.loads(compra)
                    comprasUsuario.append(compra)

            queryUsuario = {"cpf": usuario['cpf']}
            novasInformacoes = {"$set": {'compras': comprasUsuario}}

            colecaoUsuarios = db.Usuarios
            colecaoUsuarios.update_one(queryUsuario, novasInformacoes)

            #Atualização da variável local do usuário logado
            usuario["compras"] = comprasUsuario

            #Atualização da coleção de produtos com a nova quantidade
            queryProduto = {"_id": produtoEscolhido["_id"]}
            novasInformacoes = {"$set": {
                "quantidade": produtoEscolhido["quantidade"] - quantidadeEscolhida
            }}
            colecaoProdutos.update_one(queryProduto, novasInformacoes)

            print('Compra realizada com sucesso! ')

        elif(confirmarCompra == 'N'):
            print('Compra cancelada.')

    return

def checar_login_usuario(conexaoRedis, chaveUsuario):
    if(conexaoRedis.exists(chaveUsuario)):
        return True
    
    print('\nSua sessão expirou. Faça o login novamente')
    return False

def update_favoritos_usuario(db, conexaoRedis, chaveUsuario, usuario):
    while True:
        favoritosRedis = conexaoRedis.lrange(f"{chaveUsuario}-favoritos", 0, -1)
        favoritos = []

        if(favoritosRedis):
            for favorito in favoritosRedis:
                favorito = json.loads(favorito)
                favoritos.append(favorito)

        if not(favoritos):
            print('\nVocê ainda não possui nenhum item marcado como favorito.')
        else:
            print("\nSeus favoritos: ")
            for favorito in favoritos:
                print(f'\nCódigo: {favorito["id_produto"]}')
                print(f'Nome: {favorito["nome"]}')
                print(f'Descrição: {favorito["descricao"]}')
                print(f'Valor: {favorito["valor"]}')

        keyUpdateFavoritos = input('\nDeseja atualizar os favoritos? S/N ').upper()
        if(keyUpdateFavoritos == 'S'):
            keyOpcaoFavoritos = 0
            while True:
                print('1 - Adicionar um favorito')
                print('2 - Remover um item favorito')
                keyOpcaoFavoritos = input('Escolha uma opção: (C para cancelar) ').upper()
                match keyOpcaoFavoritos:
                    case '1':
                        nomeProduto = input('Qual produto você deseja adicionar? (digite o nome) ')
                        queryProduto = {"nome": {"$regex": nomeProduto, "$options": "i"}}
                        colecaoProdutos = db.Produtos
                        produtos = colecaoProdutos.find(queryProduto)

                        produtos = list(produtos)
                        if not(produtos):
                            print('Não foram encontrados produtos com essas informações')
                            break
                        else:
                            for produto in produtos:
                                print(f'\nCódigo: {produto["_id"]}')
                                print(f'Nome: {produto["nome"]}')
                                print(f'Descrição: {produto["descricao"]}')
                                print(f'Valor: {produto["valor"]}')

                            idProdutoEscolhido = input('Digite o código do produto escolhido: ')
                            if(idProdutoEscolhido.isnumeric()):
                                produtoEscolhido = next((produto for produto in produtos if produto["_id"] == int(idProdutoEscolhido)), None)
                                if(produtoEscolhido):
                                    favorito = {
                                    "_id": str(uuid.uuid4()),
                                    "id_produto": produtoEscolhido["_id"],
                                    "nome": produtoEscolhido["nome"],
                                    "descricao": produtoEscolhido["descricao"],
                                    "valor": produtoEscolhido["valor"]
                                    }

                                    #Atualização da lista no redis
                                    favorito = json.dumps(favorito)
                                    conexaoRedis.rpush(f"{chaveUsuario}-favoritos", favorito)
                                    print(f'{produtoEscolhido["nome"]} adicionado aos favoritos')
                                    break
                                else:
                                    print('Código inválido')
                                    break
                            else:
                                print('Código inválido')
                                break
                    case '2':
                        if not(favoritos):
                            print('\nNão há itens nos favoritos para remover')
                            break
                        else:
                            idFavoritoEscolhido = input('Digite o código do favorito que deseja remover: ')
                            if idFavoritoEscolhido.isnumeric():
                                idFavoritoEscolhido = int(idFavoritoEscolhido)
                                favoritoEscolhido = next((favorito for favorito in favoritos if favorito["id_produto"] == idFavoritoEscolhido), None)
                                if favoritoEscolhido:

                                    #Atualização da lista no redis
                                    favoritoEscolhido = json.dumps(favoritoEscolhido) 
                                    conexaoRedis.lrem(f"{chaveUsuario}-favoritos", 1, favoritoEscolhido)  
                                    print('Favorito removido')
                                    break
                                else:
                                    print('Código inválido')
                                    break
                            else:
                                print('Código inválido')
                                break
        elif(keyUpdateFavoritos == 'N'):
            break

    #Atualização da coleção no mongodb com os dados do redis
    favoritosRedis = conexaoRedis.lrange(f"{chaveUsuario}-favoritos", 0, -1)
    favoritos = []

    if(favoritosRedis):
        for favorito in favoritosRedis:
            favorito = json.loads(favorito)
            favoritos.append(favorito)
    queryUsuario = {"cpf": usuario['cpf']}
    novasInformacoes = {"$set": {'favoritos': favoritos}}

    colecaoUsuarios = db.Usuarios
    colecaoUsuarios.update_one(queryUsuario, novasInformacoes)

    #Atualização da variável local do usuário logado
    usuario["favoritos"] = favoritos                         
    return
