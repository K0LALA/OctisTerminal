Bloc = ((True, False, True),
        (True, True, True))
        
blocI = ((True,),
         (True,))
         
BLOC = ((True, True),
        (True, True))

def gen_grille(w,h):
  return[[False for i in range(w)] for j in range(h)]

plateau=gen_grille(8,12)

def tourne(bloc, ccw=True):
  resultat=[]
  if ccw:
    for i in range(len(bloc[0])):
      ligne=[]
      for j in range(len(bloc)-1,-1,-1):
        ligne.append(bloc[j][i])
      resultat.append(ligne)
  else:
    for i in range(len(bloc[0])):
      ligne=[]
      for j in range(len(bloc)):
        ligne.append(bloc[j][i])
      resultat.append(ligne)
  return resultat
  
def affiche(bloc):
  for B in bloc:
    for b in B:
      print("#" if b else " ", end=" ")
    print("")
  for i in range(len(bloc[0])):
    print(i+1,end=" ")
  print("")

def nb_blocs(bloc):
  n=0
  for B in bloc:
    for b in B:
      if b:
        n+=1
  return n
  
def copie_grille(grille):
  return [[elt for elt in ligne] for ligne in grille]

def copie_cases(plateau, bloc, offsetX, offsetY):
  for i in range(len(bloc)):
    for j in range(len(bloc[0])):
      if bloc[i][j]:
        plateau[offsetY + i][offsetX + j] = bloc[i][j]

def supp_lignes(plateau, indices_lignes):
  vide = [False for _ in plateau[0]]
  indices_lignes.sort()
  for indice in indices_lignes:
    plateau[indice] = vide
    for i in range(indice, 0, -1):
      plateau[i] = plateau[i-1]

def lignes_finies(plateau):
  lignes_sup = []
  for i,L in enumerate(plateau):
    if not False in L:
      lignes_sup.append(i)
  supp_lignes(plateau, lignes_sup)

def titouan(plateau):
  for i in range(len(plateau)):
    if not False in plateau[0]:
      liste = [[False for _ in range(len(plateau[0]))]]
      liste.append([[x for x in plateau[k]] for k in range(i)])
      for j in range(i+1):
        plateau[j] = liste[j]

def tombe(plateau, bloc, x):
  """
  plateau -- le plateau a modifier, a effet de bord
  bloc -- le bloc a pose
  x -- la position x ou poser le bloc, concerne le bout le plus a gauche
  """
  # Changer en une seule verification
  x=min(x, len(plateau[0])-len(bloc[0]))
  nb_apres=nb_blocs(bloc)+nb_blocs(plateau)
  hauteur=0
  copie=[]
  while hauteur + len(bloc) <= len(plateau):
    copie=copie_grille(plateau)
    copie_cases(copie, bloc, x, hauteur)
    if nb_apres != nb_blocs(copie):
      if hauteur-1 < 0:
        print("Impossible de placer")
        return
      copie_cases(plateau, bloc, x, hauteur-1)
      return
    hauteur += 1
  copie_cases(plateau, bloc, x, hauteur-1)
  lignes_finies(plateau)


tombe(plateau, BLOC, 0)
tombe(plateau, blocI, 1)
tombe(plateau, BLOC, 2)
#tombe(plateau, BLOC, 4)
tombe(plateau, BLOC, 6)
#tombe(plateau, tourne(tourne(Bloc)), 1)
#tombe(plateau, tourne(tourne(Bloc)), 4)
#tombe(plateau, blocI, 7)
affiche(plateau)