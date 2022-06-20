from pprintpp import pprint as pp
from db.database import Graph


class Estacionamento(object):
    def __init__(self):
        self.db = Graph(uri='bolt://18.212.21.103:7687',
                        user='neo4j', password='reluctance-fines-lives')

    def criarUsuario(self, pessoa):
        return self.db.execute_query('CREATE (c:Cliente {nome:$nome, telefone:$telefone, cpf:$cpf}) return c',
                                     {'nome': pessoa['nome'], 'telefone': pessoa['telefone'], 'cpf': pessoa['cpf']})

    def atualizarUsuario(self, pessoa): 
            return self.db.execute_query('MATCH (c:Cliente {nome:$nome}) SET c.telefone = $telefone RETURN c',
                                        {'nome': pessoa['nome'], 'telefone': pessoa['telefone']})

    def deletarUsuario(self, pessoa): 
        return self.db.execute_query('MATCH (c:Cliente {cpf:$cpf}) DELETE c',
                                     {'cpf': pessoa['cpf']})                                

    def buscarVagas(self, vaga):
        return self.db.execute_query('MATCH (v:Vaga{disponivel:$disponivel}) RETURN v',
                                    {'id': vaga['id'], 'disponivel': vaga['disponivel']})

    def reservarVaga(self, vaga):
        return self.db.execute_query('MATCH (v:Vaga {id:$id}) SET v.disponivel = false')
        #atualizaQtdVagas('-') 

    def pagar(self, vaga):
        return self.db.execute_query('MATCH (v:Vaga {id:$vaga}) SET v.disponivel = true')
        #atualizaQtdVagas('+')                                             

    def atualizaQtdVagas(self, incremento):
         if incremento == '+':
             return self.db.execute_query('MATCH (v:Vaga) SET v.qtdDisponivel = v.qtdDisponivel + 1')
         else:
             return self.db.execute_query('MATCH (v:Vaga) SET v.qtdDisponivel = v.qtdDisponivel - 1')    

    def criarVaga(self, vaga): 
         return self.db.execute_query('CREATE (v:Vaga {disponivel:$disponivel}) return v',
                                    {'disponivel': vaga['disponivel']})

    def buscaqtdDisponivel(self, main): 
        return self.db.execute_query('MATCH(:Servico)-[d:MAIN]->(:Vaga) RETURN d.qtdDisponivel',
                                    {'qtdDisponivel': main['qtdDisponivel']})                                

    def criarServico(self, servico):
        return self.db.execute_query('CREATE (s:Servico {cpf: $cpf, tempo:$tempo, precoUnitario:$precoUnitario, formaPag:$formaPag, total:$total}) return s',
                                     {'cpf': servico['cpf'], 'tempo': servico['tempo'], 'precoUnitario': servico['precoUnitario'], 'formaPag': servico['formaPag'], 'total':['total']})                           

    def atualizarQtdDisponivel(self, main):
        return self.db.execute_query('MATCH(:Servico)-[d:MAIN]->(:Vaga) SET d.qtdDisponivel = $qtdDisponivel RETURN d',
                                    {'qtdDisponivel': main['qtdDisponivel']}) 

    def deletarServico(self, servico):
       return self.db.execute_query('MATCH (s:Servico {id:$servico}) DELETE s')
                                                                      
    def calcularTotal(self, servico):
        return self.db.execute_query('MATCH (s:Servico {id:$id}) SET s.total = $tempo * $precoUnitario  RETURN s',
                                       {'tempo': servico['tempo'], 'precoUnitario': servico['precoUnitario'], 'formaPag': servico['formaPag'], 'total':['total']})
           

def divider():
    print('\n' + '-' * 80 + '\n')

obj = Estacionamento()

while 1:    
    option = input('1. Cliente\n2. Estacionamento\n')

    if option == '1':
        option = input('1. Cadastrar\n2. Atualizar telefone\n3. Excluir conta\n4. Buscar vagas\n5. Reservar Vaga\n6. Ler QR\n')
        if option == '1':
            nome = input('  nome: ')
            telefone = input('   telefone: ')
            cpf = input (' cpf: ')
            pessoa = {
                'nome': nome,
                'telefone': telefone,
                'cpf': cpf
            }
            aux = obj.criarUsuario(pessoa)
            divider() 

        elif option == '2':
            nome = input('  nome: ')
            telefone = input('   telefone: ')
            pessoa = {
                'nome': nome,
                'telefone': telefone
            }
            
            aux = obj.atualizarUsuario(pessoa)
            divider()

        elif option == '3':
            cpf = input('  cpf: ')
            pessoa = {
                'cpf': cpf
            }
            
            aux = obj.deletarUsuario(pessoa)
            divider()

        elif option == '4':
            vaga = {
                'id': ' ',
                'disponivel': 'true'
            }
            aux = obj.buscarVagas(vaga)
            print(aux)
            divider() 

        elif option == '5':
            numero = input('  id: ')
            vaga = {
                'id': id
            }
            aux = obj.reservarVaga(vaga)
            divider()

        elif option == '6':
            cpf = input( 'cpf: ') 
            tempo = input('  tempo: ')
            formaPag = input(' formaPag: ')
            servico = {
                'cpf': cpf,
                'tempo': tempo,
                'precoUnitario': 10,
                'formaPag': formaPag,
                'total': 0
            }
            aux = obj.criarServico(servico)
            divider()  
      

    elif option == '2':
        option = input('1. Cadastrar Vaga\n2. Atualizar vaga\n3. Excluir vaga\n4. Buscar vagas\n')
        if option == '1':
            disponivel = 'true'
            vaga = {
                'disponivel': disponivel
            }
            main = {
                'qtdDisponivel' : 1
            }
            aux = obj.criarVaga(vaga)
            aux2 = obj.buscaqtdDisponivel(main)
            divider()

    else:
        break

obj.db.close()