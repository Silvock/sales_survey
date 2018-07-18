import pandas as pd
def verif_presence_nan_in_df(data, namedf=''):
    """Determine si le dataframe contient des valeurs nulles
    Parameters
    ----------
    data : DataFrame
        The first parameter.
    namedf : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.
    
    """

    if data.isnull().values.any() == False:
        print("Il n'y a pas de valeur manquante dans {}".format(namedf))
    else:
        print('Présence de valeurs manquante dans {}'.format(namedf))

def verif_doublon(data, namedf=''):
    """Vérifie la présence de doublons
    Parameters
    ----------
    data : DataFrame
        The first parameter.
    namedf : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.
    
    """
    data_ss_doublon = data.drop_duplicates()
    if data.shape == data_ss_doublon.shape:
        print("Absence de doublon, il n'y a pas de retraitement à faire pour {}".format(namedf))
    else:
        print('Suppression des doublons ?')


def distribution_empirique(data,variable='',freqcumul=False):
    """Construit un tableau de distribution empirique
    Parameters
    ----------
    data : DataFrame
        The first parameter.
    variable : str
        The second parameter : Caractère ou nom de la colonne à traiter.
    freqcumul : bool
        The third parameter : True si on souhaite obtenir la colonne des fréquences cumulées, False par défaut

    Returns
    -------
        DataFrame
    
    
    """
    if freqcumul==False:
        effectifs = data[variable].value_counts()

        modalites = effectifs.index # l'index de effectifs contient les modalités
        tab = pd.DataFrame(modalites, columns = [variable]) #création du tableau à partir des modalités

        tab["n"] = effectifs.values

        tab["f"] = tab["n"] / len(data) # len(data) renvoie la taille de l'échantillon
        return tab
        print('Colonne des fréquences cumulées non construite')
    else:
        effectifs = data[variable].value_counts()

        modalites = effectifs.index # l'index de effectifs contient les modalités
        tab = pd.DataFrame(modalites, columns = [variable]) #création du tableau à partir des modalités

        tab["n"] = effectifs.values

        tab["f"] = tab["n"] / len(data) # len(data) renvoie la taille de l'échantillon

        tab = tab.sort_values(variable) # tri des valeurs de la variable X (croissant)
        tab["F"] = tab["f"].cumsum() # cumsum calcule la somme cumulée
        return tab

def make_cont_tab(data, var1, var2, qual2=False):
    """Construit un tableau de contingenge et au choix un heatmap
    Parameters
    ----------
    data : DataFrame
        The first parameter.
    var1 : str
        The second parameter : Premier caractère ou nom de la colonne à traiter.
    var2 :
        The third parameter : Second caractère ou nom de la colonne à traiter.
    qual2 : bool
        The fourth parameter : True si on souhaite obtenir la heatmap des xi en cas de 2 varaibles qualitatives, False par défaut

    Returns
    -------
        DataFrame (+ Seaborn Figure)
    
    
    
    
    """
    import seaborn as sns
    if qual2==True:
        X = str(var1)

        Y = str(var2)


        c = data[[X,Y]].pivot_table(index=X,columns=Y,aggfunc=len)

        cont = c.copy()


        tx = data[X].value_counts()

        ty = data[Y].value_counts()


        cont.loc[:,"Total"] = tx

        cont.loc["total",:] = ty

        cont.loc["total","Total"] = len(data)



        tx = pd.DataFrame(tx)


        ty = pd.DataFrame(ty)

        tx.columns = ["foo"]

        ty.columns = ["foo"]

        n = len(data)

        indep = (tx.dot(ty.T) / n)


        c = c.fillna(0) # on remplace les valeurs nulles par des 0

        mesure = (c-indep)**2/indep

        xi_n = mesure.sum().sum()

        d = (mesure/xi_n)
        a = sns.heatmap(d, annot=c)
        a.set_title('Tableau de contingence coloré')


        return cont, a,d
    else:
        X = str(var1)

        Y = str(var2)


        c = data[[X,Y]].pivot_table(index=X,columns=Y,aggfunc=len)

        cont = c.copy()


        tx = data[X].value_counts()

        ty = data[Y].value_counts()


        cont.loc[:,"Total"] = tx

        cont.loc["total",:] = ty

        cont.loc["total","Total"] = len(data)

        return cont

def eta_squared(x,y):
    """Permet de savoir si une variable quantitative ou qualitative sont corrélées
    Parameters
    ----------
    x : Series
        The first parameter.
    y : Series
        The second parameter.

    Returns
    -------
    Coefficient de corrélation
    
    
    """
    moyenne_y = y.mean()
    classes = []
    for classe in x.unique():
        yi_classe = y[x==classe]
        classes.append({'ni': len(yi_classe),
                        'moyenne_classe': yi_classe.mean()})
    SCT = sum([(yj-moyenne_y)**2 for yj in y])
    SCE = sum([c['ni']*(c['moyenne_classe']-moyenne_y)**2 for c in classes])
    return SCE/SCT
