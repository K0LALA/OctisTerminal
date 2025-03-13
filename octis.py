Bloc = ((True, False, True),
        (True, True, True))
        
blocI = ((True,),
         (True,))
         
carre = ((True, True),
        (True, True))

def gen_grille(largeur,hauteur):
  """
  largeur -- la largeur de la grille
  hauteur -- la hauetur de la grille

  retourne une liste de listes de False de largeur et hauteur donnees
  """
  return[[False for _ in range(largeur)] for _ in range(hauteur)]

plateau=gen_grille(8,12)

def tourne(bloc, ccw=True):
  """
  bloc -- une liste de listes (ou tuple de tuples) de booleens
  ccw -- booleen, sens de la rotation, horaire par defaut

  retourne une liste de liste du bloc tourne, avec les dimensions adaptees

  >>> tourne(((True, False), (False,True)))
  [[False, True], [True, False]]
  >>> tourne(((True, True, True),), ccw=False)
  [[True], [True], [True]]
  """
  resultat=[]
  for i in range(len(bloc[0])):
    ligne = []    
    for j in range(-ccw, len(bloc) - 2 * len(bloc) * ccw - ccw, 1 - 2 * ccw):
      ligne.append(bloc[j][i])
    resultat.append(ligne)
  return resultat
  
def affiche(bloc, numeros=True):
  """
  bloc -- une liste de listes de booleens
  numeros -- un booleen

  affiche le bloc dans la console avec les nombres en abscisse si demande
  """
  for ligne in bloc:
    for case in ligne:
      print("#" if case else " ", end=" ")
    print("")
  if numeros:
    for i in range(len(bloc[0])):
      print(i+1, end=" ")
    print("")

def compte_blocs(bloc):
  """
  bloc -- une liste de listes de booleens

  renvoie le nombre de True dans le bloc

  >>> compte_blocs(((True, False), (False, True)))
  2
  >>> compte_blocs(((False,),(False,)))
  0
  """
  nombre=0
  for ligne in bloc:
    for case in ligne:
      if case:
        nombre += 1
  return nombre
  
def copie_grille(grille):
  """
  grille -- une liste de listes de booleens
  
  renvoie une copie de la grille
  >>> copie_grille(((True, False), (False, True)))
  [[True, False], [False, True]]
  """
  return [[case for case in ligne] for ligne in grille]

def copie_cases(plateau, bloc, offsetX, offsetY):
  """
  plateau -- une liste de listes de booleens
  bloc -- une liste de listes de booleens
  offsetX -- un entier
  offsetY -- un entier

  modifie plateau en ajoutant le bloc (seulement True) sur le plateau avec un decalage a partir du bas gauche du bloc
  """
  for i in range(len(bloc)):
    for j in range(len(bloc[0])):
      if bloc[i][j]:
        plateau[offsetY + i][offsetX + j] = bloc[i][j]

def supp_lignes(plateau, indices_lignes):
  """
  plateau -- une liste de listes de booleens
  indice_lignes -- une liste d'indices des lignes a supprimer

  supprime les lignes aux indices donnes et fait descendre les lignes dessus
  """
  vide = [False for _ in plateau[0]]
  indices_lignes.sort()
  for indice in indices_lignes:
    plateau[indice] = vide
    for i in range(indice, 0, -1):
      plateau[i] = plateau[i-1]

def detect_lignes(plateau):
  """
  plateau -- une liste de listes de booleens

  detecte et renvoie une liste des indices de toutes les lignes completees sur le plateau
  """
  lignes_completes = []
  for indice, ligne in enumerate(plateau):
    if not False in ligne:
      lignes_completes.append(indice)
  return lignes_completes

def lignes_finies(plateau):
  """
  plateau -- une liste de listes de booleens

  supprime les lignes finies du plateau et fait descendre les lignes dessus
  """
  lignes_completes = detect_lignes(plateau)
  supp_lignes(plateau, lignes_completes)

def tombe(plateau, bloc, x):
  """
  plateau -- le plateau a modifier, a effet de bord
  bloc -- le bloc a pose
  x -- la position x ou poser le bloc, concerne le bout le plus a gauche

  fait tomber un bloc sur le plateau avec un abscisse donne
  """
  # Changer en une seule verification avant la fonction
  x=min(x, len(plateau[0]) - len(bloc[0]))
  x=max(0, x)

  total_blocs = compte_blocs(bloc) + compte_blocs(plateau)
  hauteur = 0
  copie = []
  while hauteur + len(bloc) <= len(plateau):
    copie = copie_grille(plateau)
    copie_cases(copie, bloc, x, hauteur)
    if total_blocs != compte_blocs(copie):
      if hauteur - 1 < 0:
        return -1
      copie_cases(plateau, bloc, x, hauteur - 1)
      return
    hauteur += 1
  copie_cases(plateau, bloc, x, hauteur - 1)
  lignes_finies(plateau)


def main():
  tombe(plateau, carre, 0)
  tombe(plateau, blocI, 1)
  tombe(plateau, carre, 2)
  tombe(plateau, carre, 6)
  affiche(plateau)

if __name__ == "__main__":
    # On teste toutes les fonctions avant de commencer
    import doctest
    doctest.testmod(verbose=False)

    # On appelle la fonction principale
    main()