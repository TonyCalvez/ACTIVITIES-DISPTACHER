import pandas as pd
from math import *
from munkres import Munkres
import numpy as np
import warnings

#Make with ❤ for Jeanne.

nomdufichier = 'jeanne.xlsx'

warnings.filterwarnings('ignore')

dfchoice = pd.read_excel(nomdufichier, sheet_name=1)
dfmatiere = pd.read_excel(nomdufichier, sheet_name=2)

#Trier par période
matierelist = {}
dfchoicematiere = {}
for nomperiode in dfmatiere['période'].unique():
    matierelist[nomperiode] = dfmatiere[dfmatiere['période'] == nomperiode]['EC'].tolist()
    dfchoicematiere[nomperiode] = dfchoice[matierelist[nomperiode]]

    nbeleves= len(dfchoice['élèves'])
    nbmatieres = len(matierelist[nomperiode])
    nbduplication = nbeleves/nbmatieres


    colonnenumero = 0

    for i in range(ceil(nbduplication)):
        for matiere in matierelist[nomperiode]:
                if colonnenumero < nbeleves:
                    dfchoicematiere[nomperiode][str(matiere) + ' ' + str(colonnenumero)] = dfchoicematiere[nomperiode][matiere]
                    colonnenumero = 1 + colonnenumero
                else:
                    break


    for column in dfchoicematiere[nomperiode].columns:
        if len(str(column).split())==1:
            dfchoicematiere[nomperiode] = dfchoicematiere[nomperiode].drop(columns=column)

    print(dfchoicematiere[nomperiode])

    #algorithme hongrois similaire aux algo de mariage vu à l'ENSTA

    matrix = dfchoicematiere[nomperiode].values.tolist()

    m = Munkres()
    indexes = m.compute(matrix)

    indexnumero = 0
    listeelevesactivites = []
    listeactivite = []
    for index in indexes:
        for column in dfchoicematiere[nomperiode].columns:
                if str(index[1]) == str(column.split()[1]):
                    listeelevesactivites.append([dfchoice['élèves'][indexnumero],int(column.split()[0])])
                    listeactivite.append(int(column.split()[0]))
        indexnumero = indexnumero + 1

    indexnumero = 0
    listeelevecontent = []
    listecontent = []
    for listeeleveactivite in listeelevesactivites:
        try:
            if (listeeleveactivite[1] == dfchoice.columns[(dfchoice == 1).iloc[indexnumero]][0]) or  (listeeleveactivite[1] == dfchoice.columns[(dfchoice == 1).iloc[indexnumero]][1]):
                listeelevecontent.append([listeeleveactivite[0], '1'])
                listecontent.append(1)
            elif (listeeleveactivite[1] == dfchoice.columns[(dfchoice == 2).iloc[indexnumero]][0]) or (listeeleveactivite[2] == dfchoice.columns[(dfchoice == 1).iloc[indexnumero]][1]):
                listeelevecontent.append([listeeleveactivite[0], '2'])
                listecontent.append(2)
            elif listeeleveactivite[1] == (dfchoice.columns[(dfchoice == 3).iloc[indexnumero]][0] or dfchoice.columns[(dfchoice == 3).iloc[indexnumero]][1]):
                listeelevecontent.append([listeeleveactivite[0], '3'])
                listecontent.append(3)
            else:
                listeelevecontent.append([listeeleveactivite[0], 'Choix Manuel'])
        except:
            #print('Verifiez le choix de élève n°', listeeleveactivite[0], 'car il pose problème....')
            pass
        indexnumero = indexnumero + 1



    for column in matierelist[nomperiode]:
        print('Nous avons: ', listeactivite.count(column), 'élèves pour la matière', column)


    print('Nous avons: ', listecontent.count(1), ' super content')
    print('Nous avons: ', listecontent.count(2), ' content')
    print('Nous avons: ', listecontent.count(3), ' a revoir')

    print('Nous avons: ', len(listeelevesactivites), ' élèves')

    print('Les paires pour la période ', nomperiode, 'sont : ')
    print(listeelevesactivites)

    exporter = np.array(listeelevesactivites)
    np.savetxt(str(nomperiode)+'.csv', exporter, delimiter=',', fmt='%i')

