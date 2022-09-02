from urllib import response
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas,Atividades, db_session

app= Flask(__name__)
api= Api(app)

class Pessoa(Resource):
    def get(self, nome):
        Pessoa= Pessoas.query.filter_by(nome=nome).first()
        try:
            response= {
                'nome': Pessoa.nome,
                'idade': Pessoa.idade,
                'id': Pessoa.id
            }
        except AttributeError:
            response = {'status': 'erro', 'messagem': 'Pessoa não encontrada'}
        return response

    def put(self, nome):
        pessoa= Pessoas.query.filter_by(nome=nome).first()
        print(pessoa.nome)
        dados =request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade= dados['idade']
        pessoa.save()
        response={
            'id': pessoa.id,
            'nome'  : pessoa.nome,
            'idade': pessoa.idade,
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso '.format(pessoa.nome)
        db_session.delete(pessoa)
        db_session.commit()
        return {'status':'successo', 'mensagem':mensagem}

class ListaPessoa(Resource):
    def get(self):
        pessoas= Pessoas.query.all()
        response= [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response

    def post(self):
        dados= request.json
        pessoa= Pessoas(nome=dados['nome'], idade= dados['idade'])
        pessoa.save()
        response={
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


class Atividade(Resource):
    def get(self):
       atividade= Atividades.query.all()
       response= [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividade]
       return response
    def post(self):
        dados= request.json
        pessoa= Pessoas.query.filter_by(nome=dados['pessoa']).first()
       
        if pessoa:
            print(pessoa)
            atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
            atividade.save()
            response={
                'id': atividade.id,
                'nome': atividade.nome,
                'pessoa': atividade.pessoa.nome
            }
        else:
            response = {'status':'erro', 'mensagem':'pessoa não existe'}
             
        return response

class ListarAtividades(Resource):
    def get(self, nome):
        pessoa= Pessoas.query.filter_by(nome=nome).first()
        listaAtividades= Atividades.query.filter_by(pessoa=pessoa)
        lista=[i.nome for i in  listaAtividades]
        response={
             'nome': pessoa.nome,
             'atividades': lista
        }
        return response
        



api.add_resource(ListaPessoa, '/pessoa')
api.add_resource(Atividade, '/atividade')       
api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListarAtividades, '/pessoaAtividade/<string:nome>')

if __name__ == '__main__':
    app.run(debug=True)
