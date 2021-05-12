import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Aparentemente faz aparecer valores das porcentagens ao lado das barras(ctrl c + ctrl v da net com
#algumas alterações). h_v='v' vertical, 'h' horizontal
def show_values(axs, h_v="v", space=0.4,fontsize=10):
    def _show_on_single_plot(ax):
        if h_v == "v":
            for p in ax.patches:
                x = p.get_x() + p.get_width() / 2
                y = p.get_y() + p.get_height()
                value = abs(float(p.get_height()))
                ax.text(x, y, value, ha="center",fontsize=fontisize)
        elif h_v == "h":
            for p in ax.patches:
                #print(p.get_width())
                if p.get_width()>=0:
                    x = p.get_x() + p.get_width() + float(space)
                    ha='left'
                elif(p.get_width()<0):
                    x = p.get_x() + p.get_width() - float(space)
                    ha='right'
                else:
                    x=0
                    print("Erro")
                y = p.get_y() + p.get_height()
                value = format(abs(float(p.get_width())),'.2f').replace(".",",")
                ax.text(x, y, value, ha=ha,fontsize=fontsize)

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


#Recebe pd.Series soma das porcentagens homens+mulheres e retorna uma lista com a faixa de idades que está mais próxima de ser a mediana, o valor das porcentagens acumuladas até essa faixa e um contador útil para plotar a linha
def getMedian(soma):
    cumsum=soma.cumsum()
    for i in range(len(cumsum)):
        if cumsum[i]<50 and cumsum[i+1]>50:
            if abs(cumsum[i]-50)>abs(cumsum[i+1]-50):
                return (cumsum[i+1],cumsum.index[i+1],i+1)
            else:
                return (cumsum[i],cumsum.index[i],i)


#Pega dados. Eles são do censo 2010-IBGE e estão em relatório regional de 2017 (https://ippuc.org.br/mostrarpagina.php?pagina=496&idioma=1&ampliar=n%E3o)

dadosHomens=pd.read_csv('dadosHomens.csv',encoding="UTF-8").set_index('regiao')
dadosMulheres=pd.read_csv('dadosMulheres.csv',encoding="UTF-8").set_index('regiao')

#define constantes

idades= pd.Series(['0-4','5-9','10-14','15-19','20-24','25-29','30-34'\
                           ,'35-39','40-44','45-49','50-54','55-59','60-64',\
                           '65-69','70-74','75-79','80+'])
columns=["idades","homens","mulheres"]
plt.style.use('ggplot')

XXSMALL_SIZE=12
XSMALL_SIZE=14
SMALL_SIZE = 16
MEDIUM_SIZE = 20
BIGGER_SIZE = 24
FIG_SIZE=(15,10)
DPI=100
plt.rc('font', size=SMALL_SIZE)          # controls default text    sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

#cria diretório img se não existir
if not os.path.exists("img"):
    os.mkdir('img')

#Faz plots
print("Soma das porcentagens para cada região, deve estar próximo de 100")
for regiao in dadosHomens.index:
    plt.figure(figsize=FIG_SIZE,dpi=DPI)

    homens=pd.Series(-dadosHomens.loc[regiao],name='homens')
    mulheres=pd.Series(dadosMulheres.loc[regiao],name='mulheres')



    df2=pd.concat([homens,mulheres],axis=1).reset_index()
    df2.columns=columns
    AgeClass=idades[::-1].reset_index(drop=True)

    blue=sns.color_palette()[1]
    red=sns.color_palette("tab10")[3]
    bar_plot = sns.barplot(x='homens', y='idades', data=df2, order=AgeClass,color=blue,label="homens")





    bar_plot = sns.barplot(x='mulheres', y='idades', data=df2, order=AgeClass,color=red,label="mulheres")
    bar_plot.set_xlabel("Porcentagem da população")
    bar_plot.set_ylabel("Idade")

    #Faz mediana
    soma=abs(mulheres)+abs(homens)
    median=getMedian(soma)

    #Plota mediana, os ticks em y do plot vão de 1 em 1, de cima para baixo. Dessa forma, precisamos plotar o complementar do contador da função getMedian. Além disso, tomamos -0.5 de forma que a mediana fique no meio do caminho entre a faixa desejada e a próxima
    plt.axhline(len(soma)-1-median[2]-0.5,linestyle='--',color='k',label='mediana: '+format(median[0],'.2f')+"%")
    print(regiao+": "+str(-homens.sum()+mulheres.sum()),'mediana :'+median[1])

    show_values(bar_plot,h_v='h',space=0.1,fontsize=XXSMALL_SIZE)
    plt.xlim([-7,7])




    bar_plot.legend()
    bar_plot.set_title(regiao +" - 2010")

    #Arruma para ticks ficarem sempre positivos
    bar_plot.set_xticklabels([str(abs(x)) for x in bar_plot.get_xticks()])

    bar_plot.figure.savefig(os.path.join("img",regiao.replace(" ",'_')),dpi=DPI,figsize=FIG_SIZE)
    #plt.show(bar_plot)

    bar_plot.clear()
