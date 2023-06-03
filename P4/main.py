import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

simulacao = pd.DataFrame()

path = os.path.abspath(__file__)

## Valores enunciado
DIAS = 20

CUSTO_A = 60
CUSTO_B = 135

VALOR_VENDA_A = 150
VALOR_VENDA_B = 280

LIMITE_ESTOQUE_X = 300
LIMITE_ESTOQUE_Y = 250

POLITICA_COMPRA_ESTOQUE_X = 500
POLITICA_COMPRA_ESTOQUE_Y = 400

list_dias = np.arange(DIAS) + 1

simulacao["dia"] = list_dias

demanda_a= []
demanda_b = []

producao_a = []
producao_b = []

# estoque = [X,Y]
estoque_inicial = [np.random.randint(LIMITE_ESTOQUE_X, LIMITE_ESTOQUE_X + POLITICA_COMPRA_ESTOQUE_X),np.random.randint(LIMITE_ESTOQUE_Y, LIMITE_ESTOQUE_Y + POLITICA_COMPRA_ESTOQUE_Y)]
estoque_x = []
estoque_y = []

lucro_a = []
lucro_b = []

for index, row in simulacao.iterrows():    
    
    ##### Distribuição probabilidade de demanda e produção 
    demanda_a.append(np.random.choice([70,80,90,100,120,130], p=[0.1,0.25,0.2,0.3,0.1,0.05])) 
    demanda_b.append(np.random.choice([80,95,110,130,140,160], p=[0.15,0.20,0.25,0.30,0.05,0.05])) 
    producao_a.append(np.random.choice([60,75,80,150,180,200],p=[0.1, 0.2, 0.25, 0.25, 0.1, 0.1]))
    producao_b.append(np.random.choice([60,75,90,110,130,170], p=[0.1,0.2,0.2,0.3,0.1,0.1]))
    
    ##### Cálculo de estoque no início de cada dia
    if index == 0:
        estoque_x.append(estoque_inicial[0])
        estoque_y.append(estoque_inicial[1])

    else:
        estoque_remanescente_x = estoque_x[index - 1] - 2 * (producao_a[index] + producao_b[index])
        if (estoque_remanescente_x) <= LIMITE_ESTOQUE_X:
            if (estoque_remanescente_x) < 0:
                estoque_x.append(POLITICA_COMPRA_ESTOQUE_X)
            else:
                estoque_x.append((estoque_remanescente_x) + POLITICA_COMPRA_ESTOQUE_X)
        else:
            estoque_x.append(estoque_remanescente_x)

        estoque_remanescente_y = estoque_y[index - 1] - producao_a[index - 1] - (3*producao_b[index - 1])

        if estoque_remanescente_y <= LIMITE_ESTOQUE_Y:
            if estoque_remanescente_y < 0:
                if index == 1:
                    estoque_y.append(0)
                else:
                    estoque_y.append(POLITICA_COMPRA_ESTOQUE_Y)
            else:
                estoque_y.append(estoque_remanescente_y + POLITICA_COMPRA_ESTOQUE_Y)
        else:
            estoque_y.append(estoque_remanescente_y)

    ##### Lucro
    if demanda_a[index] <= producao_a[index]:
        lucro_a.append((demanda_a[index] * VALOR_VENDA_A) - (producao_a[index] * CUSTO_A))
    else:
        lucro_a.append((producao_a[index] * VALOR_VENDA_A) - (producao_a[index] * CUSTO_A))

    if demanda_b[index] <= producao_b[index]:
        lucro_b.append((demanda_b[index] * VALOR_VENDA_B) - (producao_b[index] * CUSTO_B))
    else:
        lucro_b.append((producao_b[index] * VALOR_VENDA_B) - (producao_b[index] * CUSTO_B))


        

## Construindo planilha
simulacao["demanda A"] = np.array(demanda_a)
simulacao["demanda B"] = np.array(demanda_b)
simulacao["producao A"] = np.array(producao_a)
simulacao["producao B"] = np.array(producao_b)
simulacao["estoque inicio do dia X"] = np.array(estoque_x)
simulacao["estoque inicio do dia Y"] = np.array(estoque_y)
simulacao["receita A"] = np.array(lucro_a)
simulacao["receita B"] = np.array(lucro_b)
simulacao.set_index(simulacao["dia"], inplace=True)
simulacao.drop("dia", axis=1, inplace=True)


## Construindo gráficos
width = 0.15

### Produção x Demanda
fig, axs = plt.subplots(2, 1, sharey=True, sharex=True)
fig.set_figheight(10)
fig.set_figwidth(15)


for ax in axs:
    ax.set_xticks(list_dias)
    ax.set_xlabel("Dias")
    ax.set_ylabel("Quantidade")

fig.suptitle('Produção x Demanda', fontsize=16)

axs[0].bar(list_dias + width, simulacao["demanda A"], width=width*2.5, color="blue", label="Demanda")
axs[0].bar(list_dias - width, simulacao["producao A"], width=width*2.5, color="red", label="Produção")
axs[0].set_title("Produto A")

axs[1].bar(list_dias + width, simulacao["demanda B"], width=width*2.5, color="blue")
axs[1].bar(list_dias - width, simulacao["producao B"], width=width*2.5, color="red")
axs[1].set_title("Produto B")

fig.legend()
fig.savefig(os.path.realpath(__file__).replace(__file__.split("\\")[-1], "producao_x_demanda.png"))

plt.clf()

### Receita
plt.title("Receita")
plt.bar(list_dias + width, simulacao["receita A"], width=width * 2, color="blue", label="A")
plt.bar(list_dias - width, simulacao["receita B"], width=width * 2,  color="red", label="B")
plt.xlabel("Dias")
plt.ylabel("Receita (R$)")
plt.xticks(list_dias)
plt.legend()
plt.savefig(os.path.realpath(__file__).replace(__file__.split("\\")[-1], "receita.png"))


analise = pd.DataFrame()
total = float(simulacao["receita A"].sum()) + float(simulacao["receita B"].sum())
analise["Receita Total"] = [total]
analise["Dias com produção menor que demanda"] = int(simulacao[(simulacao["producao A"] < simulacao["demanda A"]) | (simulacao["producao B"] < simulacao["demanda B"])].count().max())
analise.set_index(analise["Receita Total"])

with pd.ExcelWriter(os.path.realpath(__file__).replace(__file__.split("\\")[-1], "simulacao.xlsx")) as writer:
    simulacao.to_excel(writer, startcol=0, sheet_name="Simulação")
    analise.to_excel(writer, startcol=12, sheet_name="Simulação")