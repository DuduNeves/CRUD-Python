import requests
import json
import mysql.connector
import pymysql
from PySimpleGUI import PySimpleGUI as sg

banco = mysql.connector.connect(

    host="localhost",
    user="root",
    passwd="",
    database="quero2"

)

# LAYOUT JANELAS
def janela_menu():
    sg.theme('Reddit')
    layoutmenu = [
        [sg.Text('TABELAS')],
        [sg.Button('EMPRESA',size=(10,2)),sg.Button('PESSOAS',size=(10,2))]
    ]

    return sg.Window('Menu', layout=layoutmenu, size=(250,100), finalize=True)

def janela_empresa():
    sg.theme('Reddit')
    layoutempresa = [
        [sg.Text('ADICIONAR CADASTRO DE EMPRESA')],
        [sg.Text('NOME: ')],
        [sg.Input(key='nome')],
        [sg.Text('CEP:')],
        [sg.Input(key='endereco')],
        [sg.Text('NÚMERO: ')],
        [sg.Input(key='numero')],
        [sg.Text('COMPLEMENTO: ')],
        [sg.Input(key='complemento')],
        [sg.Text('TELEFONE:')],
        [sg.Input(key='telefone', password_char='*')],
        [sg.Button('CADASTRAR', key='CADASTRAR EMPRESA'), sg.Button('DELETAR', key="DELETARE"),sg.Button('ALTERAR', key="ALTERARE") ],
        [sg.Output(size=(60, 10), key='_outpute_')],
        [sg.Button('VOLTAR', key="VOLTAREMPRESAS"),sg.Button('LIMPAR', key="LIMPARE"),sg.Button('CONSULTAR', key="EXIBIRE")]
    ]

    return sg.Window('CADASTRO EMPRESA', layout=layoutempresa, finalize=True)

#-------------------------------------------FUNCINARIOS------------------------------------------------------------------
def janela_pessoa():

    sg.theme('Reddit')
    layoupessoa = [
        [sg.Text('ADICIONAR CADASTRO DE PESSOA')],
        [sg.Text('NOME: ')],
        [sg.Input(key='nomepessoa')],
        [sg.Text('Qual o cargo do funcionario cadastrado?\n 1-PROGRMADOR\n 2-GERENTE\n 3-VENDEDOR\n 4-ESTAGIARIO\n')],
        [sg.Input(key='cargo')],
        [sg.Text('SALARIO: ')],
        [sg.Input(key='salario')],
        [sg.Button('CADASTRAR', key="CADASTRAR PESSOA"), sg.Button('DELETAR', key="DELETARP"),sg.Button('ALTERAR', key="ALTERARP") ],
        [sg.Output(size=(60, 10), key='_outputp_')],
        [sg.Button('VOLTAR', key="VOLTARPESSOAS"),sg.Button('LIMPAR', key="LIMPARP"),sg.Button('CONSULTAR', key="EXIBIRP")]

    ]
    return sg.Window('CADASTRO PESSOA', layout=layoupessoa, finalize=True)

janela1, janela2, janela3 = janela_menu(), None, None

# loop para voltar para a janela inical depoisn de cadastrar as pessoas

while True:

    janela, evento, valores = sg.read_all_windows()


#-----------------------------------A FECHAR A JANELA QUANDO CLICAR N-O X------------------------------------------------------

    if evento == sg.WIN_CLOSED:
        break

#------------------------------------------------IR PARA A PROXIMA JANELA-----------------------------------------------------

    if janela == janela1 and evento == 'EMPRESA':
        janela2 = janela_empresa()
        janela1.hide()

    if janela == janela1 and evento == 'PESSOAS':
        janela3 = janela_pessoa()
        janela1.hide()

#------------------------------------VOLTAR QUANDO CLICAR NO BOTÃO VOLTAR-------------------------------------------------

    if janela == janela2 and evento == "VOLTAREMPRESAS":
        janela2.hide()
        janela1.un_hide()

    if janela == janela3 and evento == 'VOLTARPESSOAS':
        janela3.hide()
        janela1.un_hide()

#---------------------CASO O USUARIO CLIQUE EM CADASTRAR EMPRESA OU PESSOA-----------------------------------------------
    if janela == janela2 and evento == 'CADASTRAR EMPRESA':
        nome = valores['nome']
        endereco = valores['endereco']
        numero = valores['numero']
        complemento = valores['complemento']
        telefone = valores['telefone']

        sg.popup('EMPRESA CADASTRADA')

        cursor = banco.cursor()
        comando_SQL = """INSERT INTO empresas
        (nome, endereco, numero, complemento, telefone)
        VALUES (%s, %s, %s, %s, %s)"""

        valoresem = (str(nome), str(endereco), str(numero), str(complemento), str(telefone))

        cursor.execute(comando_SQL, valoresem)
        banco.commit()

        janela2.hide()
        janela1.un_hide()

    if janela == janela3 and evento == 'CADASTRAR PESSOA':
        nomepessoa = valores['nomepessoa']
        cargo = valores['cargo']
        salario = valores['salario']

        sg.popup('FUNCIONARIO CADASTRADO')

        cursor = banco.cursor()
        comando_SQL = """INSERT INTO pessoas
           (nomepessoa, cargo, salario)
           VALUES (%s, %s, %s)"""
        valorespe = (str(nomepessoa), str(cargo), float(salario))

        cursor.execute(comando_SQL, valorespe)
        banco.commit()

        janela3.hide()
        janela1.un_hide()

# ---------------------DELETAR--------------------------------

    if evento == 'DELETARE':

        nome = valores['nome']
        cursor = banco.cursor()
        delete = f'DELETE FROM empresas WHERE nome = "{nome}"'
        cursor.execute(delete)
        banco.commit()
        sg.popup('EMPRESA DELETADA')
        janela2.hide()
        janela1.un_hide()

    if evento == 'DELETARP':

        nomepessoa = valores['nomepessoa']
        cursor = banco.cursor()
        delete = f'DELETE FROM pessoas WHERE nomepessoa = "{nomepessoa}"'
        cursor.execute(delete)
        banco.commit()
        sg.popup('FUNCIONARIO DELETADA')
        janela3.hide()
        janela3.un_hide()

# ---------------------EXIBIR--------------------------------


    if janela == janela2 and evento == 'EXIBIRE':
        nome = valores['nome']
        cursor = banco.cursor()
        exibire = 'SELECT nome,endereco,numero, complemento, telefone from empresas'

        cursor.execute(exibire)
        resultadoe = cursor.fetchall()
        print('Lista de empresas cadastradas:')
        for c in resultadoe:
            print(c)
        janela2.un_hide()


    if janela == janela3 and evento == 'EXIBIRP':
        nome = valores['nomepessoa']
        cursor = banco.cursor()
        exibirp = 'SELECT nomepessoa,cargo,salario from pessoas'

        cursor.execute(exibirp)
        resultadop = cursor.fetchall()
        print('Lista de funcionarios cadastrados:')
        for c in resultadop:
            print(c)
        janela3.un_hide()


# ---------------------LIMPAR--------------------------------

    if evento == 'LIMPARE':
        janela.FindElement('_outpute_').Update(' ')

    if evento == 'LIMPARP':
        janela.FindElement('_outputp_').Update(' ')

# ---------------------MODIFICAR--------------------------------


    if janela == janela2 and evento == 'ALTERARE':
        nome = valores['nome']
        endereco = valores['endereco']

        cursor = banco.cursor()
        altere = f'UPDATE empresa SET nome = "{nome}" WHERE endereco = "{endereco}"'

        cursor.execute(altere)
        banco.commit()

        janela2.hide()
        janela1.un_hide()

    if janela == janela3 and evento == 'ALTERARP':
        nomepessoa = valores['nomepessoa']
        cargo = valores['cargo']

        cursor = banco.cursor()
        altere = f'UPDATE pessoas SET nomepessoa = "{nomepessoa}" WHERE cargo = "{cargo}"'

        cursor.execute(altere)
        banco.commit()

        janela3.hide()
        janela1.un_hide()



