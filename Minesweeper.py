import tkinter as tk
from random import randint
from functools import partial
import threading
import sys

janela = tk.Tk()
lista = []

tamanho = int(input("Digite o tamanho do jogo: "))

bombas = int(input("Digite a quantidade de bombas: "))
janela.geometry(""+str(80*tamanho)+"x"+str(81*tamanho)+"")
janela.title("Minesweeper")

def getLinha(botao, lista, tamanho):
    for i, b in enumerate(lista):
        if b == botao:
            return i // tamanho
        
def getColuna(botao, lista, tamanho):
    for i in range(len(lista)):
        if lista[i] == botao:
            return i % tamanho

def FimDeJogo():
    resetGame()
    
def BombaAleatoria(lista,num):
    aux = randint(0,(tamanho*tamanho)-1)
    if (lista[aux].bomba == False and aux != num):
            lista[aux].bomba = True
    else:
        BombaAleatoria(lista,num)

def contar_bombas_ao_redor(botao, lista):
    linha, coluna = None, None

    for i, b in enumerate(lista):
        if b == botao:
            linha, coluna = divmod(i, tamanho)
            break

    if linha is not None:
        bombas_ao_redor = 0
        for i in range(max(0, linha-1), min(tamanho, linha+2)):
            for j in range(max(0, coluna-1), min(tamanho, coluna+2)):
                if lista[i*tamanho + j].bomba:
                    bombas_ao_redor += 1
    else:
        bombas_ao_redor = 0

    return bombas_ao_redor

def PrimeiroClique(num):
    for i in range(bombas):
        BombaAleatoria(lista,num)
    for indice,element in enumerate(lista):
        element.config(command=partial(Clique,lista[indice]))
    Clique(lista[num])

def Clique(botao):
    if botao is not None:
        if (botao.bomba == True):
            botao.config(background="#ff0000")
            print("Você perdeu")
            temporizador = threading.Timer(1, FimDeJogo)
            temporizador.start()
        else:
            if not botao.clicado:
                botao.clicado = True
                bombas_ao_redor = contar_bombas_ao_redor(botao, lista)
                botao.config(background="#ffffff", text=str(bombas_ao_redor))
                AbrirZeros(botao)
                
def AbrirZeros(botao):
    botaocima = get_button_above(botao,tamanho,lista)
    botaobaixo = get_button_below(botao,tamanho,lista)
    botaoesquerda = get_button_left(botao,tamanho,lista)
    botaodireita = get_button_right(botao,tamanho,lista)
    if(contar_bombas_ao_redor(botaocima,lista) == 0):
        Clique(botaocima)
    if(contar_bombas_ao_redor(botaobaixo,lista) == 0):
        Clique(botaobaixo)
    if(contar_bombas_ao_redor(botaoesquerda,lista) == 0):
        Clique(botaoesquerda)
    if(contar_bombas_ao_redor(botaodireita,lista) == 0):
        Clique(botaodireita)
    
              
def get_button_above(botao,tamanho, lista):
    linha = getLinha(botao,lista,tamanho)
    coluna = getColuna(botao,lista,tamanho)
    cima = (linha - 1) * tamanho + coluna
    return lista[cima] if linha > 0 else None

def get_button_below(botao, tamanho, lista):
    linha = getLinha(botao,lista,tamanho)
    coluna = getColuna(botao,lista,tamanho)
    abaixo = (linha + 1) * tamanho + coluna
    return lista[abaixo] if linha < tamanho - 1 else None

def get_button_left(botao, tamanho, lista):
    linha = getLinha(botao,lista,tamanho)
    coluna = getColuna(botao,lista,tamanho)
    esquerda = linha * tamanho + (coluna - 1)
    return lista[esquerda] if coluna > 0 else None

def get_button_right(botao, tamanho, lista):
    linha = getLinha(botao,lista,tamanho)
    coluna = getColuna(botao,lista,tamanho)
    direita = linha * tamanho + (coluna + 1)
    return lista[direita] if coluna < tamanho - 1 else None

class Quadrado(tk.Button):
    bomba = False
    clicado= False

def resetGame():
    for indice, element in enumerate(lista):
        element.bomba = False
        element.clicado = False
        element.config(background="#00ff00",command=lambda:PrimeiroClique(indice),text="")

for linha in range(tamanho):
    for coluna in range(tamanho):
            botao = Quadrado(janela, compound='top', height=4, width=10, command=partial(PrimeiroClique,(linha*tamanho+coluna)), background="#00ff00")
            botao.grid(row=linha, column=coluna)
            lista.append(botao)

janela.mainloop()
