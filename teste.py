import pymysql
# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, AdminLoginForm
import teste

def conectar_pymysql():
    try:
        # Conectar ao banco de dados
        conexao = pymysql.connect(
            host='127.0.0.1',  # Endereço do servidor MySQL
            user='root',  # Seu nome de usuário MySQL
            password='',  # Sua senha MySQL
            database='user_management_app'  # Nome do banco de dados
        )

        print("Conexão bem-sucedida ao banco de dados MySQL")

        # Aqui você pode executar consultas
        with conexao.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print("Você está conectado ao banco de dados:", database_name)

    except pymysql.MySQLError as e:
        print("Erro ao conectar ao MySQL", e)
    finally:
        conexao.close()
        # print("Conexão ao MySQL foi fechada.")


# Chamar a função
# conectar_pymysql()

def cadastrar(nome, email, senha):
    try:
        conexao = pymysql.connect(
            host='127.0.0.1',  # Endereço do servidor MySQL
            user='root',  # Seu nome de usuário MySQL
            password='',  # Sua senha MySQL
            database='user_management_app'  # Nome do banco de dados
        )

        cursor = conexao.cursor()
        sql = "INSERT INTO cadastro (Nome,Email, Senha) VALUES (%s, %s, %s)"
        valores = (nome, email, senha)
        cursor.execute(sql, valores)
        conexao.commit()
        print(cursor.rowcount, "registro(s) inserido(s).")

    except pymysql.MySQLError as e:
        print("Erro ao inserir dados", e)
    finally:
        cursor.close()
        conexao.close()
        # print("Conexão ao MySQL foi fechada.")


def login(email, senha):
    try:
        conexao = pymysql.connect(
            host='127.0.0.1',  # Endereço do servidor MySQL
            user='root',  # Seu nome de usuário MySQL
            password='',  # Sua senha MySQL
            database='user_management_app'  # Nome do banco de dados
        )

        cursor = conexao.cursor()

        sql = f'''SELECT Nome FROM cadastro WHERE email = "{email}" AND senha = "{senha}"'''
        cursor.execute(sql)


        # Capturando o resultado da consulta
        resultado = cursor.fetchone()  # Para obter apenas um resultado
        # Ou
        # resultado = cursor.fetchall()  # Para obter todos os resultados

        # Agora você pode usar o resultado da consulta

        if resultado:
            #nome = resultado['Nome']

            return resultado[0]

        else:
            print('Nenhum resultado encontrado.')


    except pymysql.MySQLError as e:
        print("Erro ao inserir dados", e)
    finally:
        cursor.close()
        conexao.close()
        # print("Conexão ao MySQL foi fechada.")


# Chamar a função para inserir um cliente
# login('aa@a.com', 'aa')

def allDB():
    try:
        conexao = pymysql.connect(
            host='127.0.0.1',  # Endereço do servidor MySQL
            user='root',  # Seu nome de usuário MySQL
            password='',  # Sua senha MySQL
            database='user_management_app'  # Nome do banco de dados
        )

        cursor = conexao.cursor()

        sql = f'''SELECT Email, Nome FROM cadastro'''
        cursor.execute(sql)


        # Capturando o resultado da consulta
        resultado = cursor.fetchall()  # Para obter apenas um resultado
        # Ou
        # resultado = cursor.fetchall()  # Para obter todos os resultados

        # Agora você pode usar o resultado da consulta

        if resultado:
            #nome = resultado['Nome']
            users_db = {}

            # Itera sobre cada tupla e popula o dicionário
            for result in resultado:
                # Desempacota apenas os dois primeiros valores, ignorando o resto
                email, name = result[0], result[1]
                users_db[email] = {'name': name}
            return users_db




    except pymysql.MySQLError as e:
        print("Erro ao inserir dados", e)
    finally:
        cursor.close()
        conexao.close()
        # print("Conexão ao MySQL foi fechada.")

# allDB()