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

    bombas_ao_redor = 0
    for i in range(max(0, linha-1), min(tamanho, linha+2)):
        for j in range(max(0, coluna-1), min(tamanho, coluna+2)):
            if lista[i*tamanho + j].bomba:
                bombas_ao_redor += 1

    return bombas_ao_redor

def PrimeiroClique(num):
    for i in range(bombas):
        BombaAleatoria(lista,num)
    for indice,element in enumerate(lista):
        element.config(command=partial(Clique,lista[indice]))

def FimDeJogo():
    resetGame()

def Clique(botao):
    if (botao.bomba == True):
        botao.config(background="#ff0000")
        print("Você perdeu")
        temporizador = threading.Timer(1, FimDeJogo)
        temporizador.start()
    else:
        bombas_ao_redor = contar_bombas_ao_redor(botao, lista)
        botao.config(background="#ffffff", text=str(bombas_ao_redor))

class Quadrado(tk.Button):
    bomba = False

def resetGame():
    for indice, element in enumerate(lista):
        element.bomba = False
        element.config(background="#00ff00",command=lambda:PrimeiroClique(indice),text="")

for linha in range(tamanho):
    for coluna in range(tamanho):
            botao = Quadrado(janela, compound='top', height=4, width=10, command=lambda:PrimeiroClique(linha*5+coluna), background="#00ff00")
            botao.grid(row=linha, column=coluna)
            lista.append(botao)

janela.mainloop()