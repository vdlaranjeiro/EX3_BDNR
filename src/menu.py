from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis
import json

from usuario import *
from vendedor import *
from produto import *

#Conexão com o mongodb
uri = "mongodb+srv://<username>:<password>@ecommerce.wmpyahq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

global db
db = client.EX2

#Conexão com o redis
conexaoRedis = redis.Redis(
  host='redis-16471.c308.sa-east-1-1.ec2.cloud.redislabs.com',
  port=16471,
  password='')

usuarioEncontrado = None
vendedorEncontrado = None

while True:
    print('\nSeja bem-vindo(a)')
    print('1 - Fazer Login')
    print('2 - Criar uma conta')
    opcaoInicial = input('Selecione uma opção. (S para sair) ').upper()

    acao = 0
    match opcaoInicial:
        case '1':
            email = input('\nDigite seu email: ')
            senha = input('Digite sua senha: ')

            colecaoUsuarios = db.Usuarios
            colecaoVendedores = db.Vendedores

            usuarioEncontrado = colecaoUsuarios.find_one({"contatos.email": email})
            vendedorEncontrado = colecaoVendedores.find_one({"contatos.email": email})

            if(usuarioEncontrado):
                if(usuarioEncontrado["senha"] == senha):
                    print(f"\nBem-vindo(a), {usuarioEncontrado['nome']}")
                    conexaoRedis.setex(f"user-{usuarioEncontrado['contatos']['email']}", 300, usuarioEncontrado['nome'])
                    break
                else:
                    print('\nEmail ou senha incorretos.')
            elif(vendedorEncontrado):
                if(vendedorEncontrado["senha"] == senha):
                    print(f"\nBem-vindo(a), {vendedorEncontrado['nome']}")
                    conexaoRedis.setex(f"user-{vendedorEncontrado['contatos']['email']}", 300, vendedorEncontrado['nome'])
                    break
                else:
                    print('\nEmail ou senha incorretos.')
            else:
                print('\nEmail ou senha incorretos.')

        case '2':
            while(acao != 'V'):
                print('\n1 - Se cadastrar como usuário.')
                print('2 - Se cadastrar como um vendedor')
                opcaoCadastro = input('Selecione um tipo de usuário. (V para voltar) ').upper()

                match opcaoCadastro:
                    case '1':
                        create_usuario(db, conexaoRedis)
                        break
                    case '2':
                        create_vendedor(db)
                        break
                    case 'V':
                        break
        case 'S':
            break

if(usuarioEncontrado):
    chaveUsuario = f"user-{usuarioEncontrado['contatos']['email']}"

    while True:
        print('\n1 - Listar suas informações')
        print('2 - Atualizar suas informações')
        print('3 - Favoritos')
        print('4 - Realizar uma compra')
        print('5 - Excluir sua conta')

        opcaoUsuario = input('Selecione uma opção. (S para sair) ').upper()
        logado = checar_login_usuario(conexaoRedis, chaveUsuario)
        if logado:
            match opcaoUsuario:
                case '1':
                    read_usuario(usuarioEncontrado)
                case '2':
                    update_usuario(db, usuarioEncontrado)
                case '3':
                    update_favoritos_usuario(db, conexaoRedis, chaveUsuario, usuarioEncontrado)
                case '4':
                    compra_usuario(db, conexaoRedis, chaveUsuario, usuarioEncontrado)
                case '5':
                    usuarioDeletado = delete_usuario(db, conexaoRedis, chaveUsuario, usuarioEncontrado)
                    if usuarioDeletado: break
                case 'S':
                    break
        else:
            break

elif(vendedorEncontrado):
    chaveVendedor = f"user-{vendedorEncontrado['contatos']['email']}"

    while True:
        print('\n1 - Listar suas informações')
        print('2 - Atualizar suas informações')
        print('3 - Excluir sua conta')
        print('4 - Listar seus produtos')
        print('5 - Cadastrar um novo produto')
        print('6 - Atualizar informações de um produto')
        print('7 - Excluir um produto')

        opcaoVendedor = input('Selecione uma opção. (S para sair) ').upper()

        logado = checar_login_usuario(conexaoRedis, chaveVendedor)
        if logado:
            match opcaoVendedor:
                case '1':
                    read_vendedor(db, vendedorEncontrado)
                case '2':
                    update_vendedor(db, vendedorEncontrado)
                case '3':
                    vendedorDeletado = delete_vendedor(db, vendedorEncontrado)
                    if vendedorDeletado: break
                case '4':
                    read_produto(db, vendedorEncontrado)
                case '5':
                    create_produto(db, vendedorEncontrado)
                case '6':
                    update_produto(db, vendedorEncontrado)
                case '7':
                    delete_produto(db, vendedorEncontrado)
                case 'S':
                    break
        else:
            break
                
print('\nAté mais!')
