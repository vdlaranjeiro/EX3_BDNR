def create_produto(db, vendedor):
    print('\nInsira as informações do produto')
    nome = input('Nome: ')
    descricao = input('Descrição: ')

    validacaoValor = 0
    while(validacaoValor != 1):
        valor = input('Valor: ')
        try:
            valor = float(valor)
            validacaoValor = 1
        except ValueError:
            print('Insira um valor válido')
    
    validacaoQuantidade = 0
    while(validacaoQuantidade != 1):
        quantidade = input('Quantidade disponível: ')
        if(quantidade.isnumeric()):
            quantidade = int(quantidade)
            validacaoQuantidade = 1
        else:
            print('Insira um valor válido')

    ultimoId = db.Produtos.find_one(sort=[("_id", -1)]) 
    if not(ultimoId):
        produto = {
            "_id": 1,
            "_idVendedor": vendedor["_id"],
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "quantidade": quantidade
        }

        insert = db.Produtos.insert_one(produto)
        print(f'\nProduto cadastrado no id: {insert.inserted_id}')
    else:
        produto = {
            "_id": ultimoId["_id"] + 1,
            "_idVendedor": vendedor["_id"],
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "quantidade": quantidade
        }

        insert = db.Produtos.insert_one(produto)
        print(f'\nProduto cadastrado no id: {insert.inserted_id}')

    return

def delete_produto(db, vendedor):
    read_produto(db, vendedor)
    idProduto = int(input('\nDigite o código do produto que deseja excluir: '))

    myquery = {"_id": idProduto}
    colecaoProdutos = db.Produtos

    produto = colecaoProdutos.find_one(myquery)
    if(produto and produto["_idVendedor"] == vendedor["_id"]):
        colecaoProdutos.delete_one(myquery)
        print(f'Produto excluído!')
    else:
        print('Código inválido')
    return

def read_produto(db, vendedor):
    myquery = {"_idVendedor": vendedor['_id']}
    colecaoProdutos = db.Produtos

    produtos = colecaoProdutos.find(myquery)
    produtos = list(produtos)

    if not (produtos):
        print('\nVocê ainda não possui produtos cadastrados.')
    else:
        print("\nSeus produtos:")
        for produto in produtos:
            print(f'\nCódigo: {produto["_id"]}')
            print(f'Nome: {produto["nome"]}')
            print(f'Descrição: {produto["descricao"]}')
            print(f'Valor: {produto["valor"]}')
            print(f'Quantidade disponível: {produto["quantidade"]}')
    
    return

def update_produto(db, vendedor):
    read_produto(db, vendedor)
    idProduto = int(input('\nDigite o código do produto que deseja atualizar: '))

    myquery = {"_id": idProduto}
    colecaoProdutos = db.Produtos

    mydoc = colecaoProdutos.find_one(myquery)


    if not(mydoc):
        print('Não foram encontrados produtos com esse código')
    elif(mydoc and mydoc["_idVendedor"] == vendedor["_id"]):
        print(f'Editando informações do produto {mydoc["_id"]} - {mydoc["nome"]}. Aperte ENTER para pular um campo')
        nome = input('Nome: ')
        if len(nome):
            mydoc["nome"] = nome
        
        descricao = input('Descrição: ')
        if len(descricao):
            mydoc["descricao"] = descricao
        
        valor = input('Valor: ')
        if len(valor):
            validacaoValor = 0
            while(validacaoValor != 1):
                try:
                    mydoc["valor"] = float(valor)
                    validacaoValor = 1
                except ValueError:
                    valor = input('Insira um valor válido: ')
        quantidade = input('Quantidade: ')
        if len(quantidade):
            validacaoQuantidade = 0
            while(validacaoQuantidade != 1):
                if(quantidade.isnumeric()):
                    mydoc["quantidade"] = int(quantidade)
                    validacaoQuantidade = 1
                else:
                    quantidade = input('Insira uma quantidade válida: ')

        novasInformacoes = {"$set": mydoc}
        colecaoProdutos.update_one(myquery, novasInformacoes)
        print('\nInformações atualizadas com sucesso!')
    else:
        print('Código inválido.')

    return