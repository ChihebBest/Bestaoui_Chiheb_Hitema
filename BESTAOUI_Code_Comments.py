import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import LabelEncoder

#Custom functions

'''
- La première fonction représente un traitement qui prend en argument un fichier CSV et crée un DataFrame depuis ce fichier
- Supprimer la ligne (axis = 0) des en-têtes en gardant uniquement les valeurs du DataFrame en mettant à jour les index
- Stocker la colonne des ID dans la variable globale ID
- Supprimer la colonne (axis = 1) des ID
- La fonction retourne le nouveau DataFrame modifié
''' 
def Treatment_1(name):
    global ID
    df = pd.read_csv(name, sep=";", header=None)
    df.columns = df.iloc[0, :].tolist()
    df = df.drop(0, axis = 0).reset_index(drop = True)
    ID = df.id
    df = df.drop('id', axis =  1)
    return df

'''
- La deuxième fonction représente un traitement qui prend en argument un Dataframe et modifie ses valeurs pour les convertir en valeurs numériques
- La première étape est de créer un objet LabelEncoder qui servira à transformer les chaines de caractères en valeurs numériques
- Créer une liste avec les noms des colonnes 5,7 et une autre liste avec les noms des autres colonnes
- Parcourir les colonnes et pour chacune parcourir les index :
  - Au niveau des colonnes numeric_list (créée dans le traitement 1) autres que la colonne 5 et 7:
      - Remplacer la valeur "unknown" par 0
  - Au niveau de la colonne 7:
      - Remplacer la valeur par le premier caractère de la chaine
  - Au niveau des label_list (noms des colonnes 5 et 7)
      - Créer une nouvelle colonne en mettant le nom de la colonne de l'itération et rajouter le mot '_encoded' avant 
        d'appliquer la fonction fit_transform de l'objet LabelEncoder pour convertir les chaines en valeurs numériques
- Supprimer la colonne 'market_share'
- Supprimer les deux colonnes 5 et 7
- Modifier les valeurs du DataFrame en valeurs réelles float
'''

def Treatment_2(df):
    lb_make = LabelEncoder()      #Let's transform our string categorical data to numeric categorical data !    
    label_list = df.columns[5:7].tolist()
    wa = df.columns[7]
    numeric_list = df.columns[~df.columns.isin(df.columns[5:8])].tolist()
    for x in df.columns: 
        for w in df.index:
            if x in numeric_list:
                if df[x][w] == 'unknown':
                    df[x][w] = 0
            elif x in wa:
                df[x][w] = df[x][w][0]
            elif x in label_list:
                df[str(x)+'_encoded'] = lb_make.fit_transform(df[x])
    if 'market_share' in df.columns.tolist():
        df = df.drop('market_share', axis = 1)
    df = df.drop(label_list, axis = 1)
    for x in df.columns:
        df[x] = df[x].astype(float)    
    return df

'''
- La troisème fonction représente un traitement qui prend en argument 
  un DataFrame (qui doit au préalable être modifié par le traitement 2) pour remplacer 
  toutes les valeurs NaN et les valeurs nulles et négatives de la colonne 'prod_cost' par la moyenne de cette colonne
'''

#Improve this treatment :)
def Treatment_3(df):

    #Convertir les élements en valeurs float
    df['prod_cost'] = pd.to_numeric(df['prod_cost'],errors='coerce')

    #Toute valeur négative ou nulle passe à NaN
    df.loc[df['prod_cost'] <= 0 ] = np.nan

    #Remplacer les NaN par la moyenne de la colonne
    df['prod_cost'] = df['prod_cost'].fillna(df['prod_cost'].mean())

    return df


#Files    
name_1 = 'mower_market_snapshot.csv'



if (__name__ == "__main__"):
    
    df15 = Treatment_1('/content/drive/My Drive/mower_market_snapshot.csv')
    #df15.head()
    
    df16 = Treatment_2(df15)
    #df16.head()
    
    df17 = Treatment_3(df16)
    #df17.head()
    #df17.groupby('prod_cost').sum()