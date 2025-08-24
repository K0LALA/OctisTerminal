from random import randint, uniform, random
from math import exp

# Definitions des blocs
blocs_dict = {  "un": ((1,),),
              
                "f": ((1, 1, 0),
                      (0, 1, 1), 
                      (0, 1, 0)),

                "i": ((1,),
                      (1,),
                      (1,),
                      (1,)),

                "o": ((1, 1, 1), 
                      (1, 0, 1),
                      (1, 1, 1)),

                "n": ((0, 1),
                      (0, 1),
                      (1, 1),
                      (1, 0)),

                "s": ((0, 1, 1),
                      (1, 1, 0)),

                "u": ((1, 0, 1),
                      (1, 1, 1)),

                "w": ((0, 0, 1),
                      (0, 1, 1),
                      (1, 1, 0)),

                "x": ((0, 1, 0),
                      (1, 1, 1),
                      (0, 1, 0)),
                                     
                "z": ((1, 1, 0),
                      (0, 1, 1)),
                
                "huit": ((0, 1, 1),
                         (0, 1, 0),
                         (0, 1, 1),
                         (1, 1, 0),
                         (1, 0, 0))}

RARE = 0.04
COMMUN = 0.11

chances_dict = {
  "un": RARE,
  "huit": RARE,
  "o": RARE,
  "f": COMMUN,
  "i": COMMUN,
  "n": COMMUN,
  "s": COMMUN,
  "u": COMMUN,
  "w": COMMUN,
  "x": COMMUN,
  "z": COMMUN
}

class NeuralNetwork:
  tailles = [210, 64, 32, 15]
  neurones = []
  poids = []
  biais = []

  def __init__(self, chemin_fichier=""):
    input_neurones = [0 for _ in range(self.tailles[0])]
    l2_neurones = [0 for _ in range(self.tailles[1])]
    l3_neurones = [0 for _ in range(self.tailles[2])]
    output_neurones = [0 for _ in range(self.tailles[3])]
    self.neurones.append(input_neurones)
    self.neurones.append(l2_neurones)
    self.neurones.append(l3_neurones)
    self.neurones.append(output_neurones)
    
    if len(chemin_fichier) > 0:
      # Lis les valeurs dans un fichier
      with open(chemin_fichier, "r") as fichier:
        tailles_ligne = fichier.readline()
        self.tailles = [int(taille) for taille in tailles_ligne.split(" ")]

        for couche in range(1, len(self.tailles)):
          couche_poids = []
          for neurone in range(self.tailles[couche]):
            ligne_poids = fichier.readline()
            poids = [float(poids_neurone) for poids_neurone in ligne_poids.split(' ')]
            neurone_poids = []
            for connexion in range(self.tailles[couche - 1]):
              neurone_poids.append(poids[connexion])
            couche_poids.append(neurone_poids)
          self.poids.append(couche_poids)

        for couche in range(1, len(self.tailles)):
          couche_biais = []
          ligne_biais = fichier.readline()
          biais = [float(biais_neurone) for biais_neurone in ligne_biais.split(" ")]
          for neurone in range(self.tailles[couche]):
            couche_biais.append(biais[neurone])
          self.biais.append(couche_biais)
    else:
      # Poids
      # Poids de la connexion entre le neurone input [j] et le neurone [i] de la première couche: weights[i][j]
      poids_1 = [[uniform(-1, 1) for _ in range(self.tailles[0])] for _ in range(self.tailles[1])]
      poids_2 = [[uniform(-1, 1) for _ in range(self.tailles[1])] for _ in range(self.tailles[2])]
      poids_3 = [[uniform(-1, 1) for _ in range(self.tailles[2])] for _ in range(self.tailles[3])]
      self.poids.append(poids_1)
      self.poids.append(poids_2)
      self.poids.append(poids_3)

      # Biais
      biais_l1 = [uniform(-1, 1) for _ in range(self.tailles[1])]
      biais_l2 = [uniform(-1, 1) for _ in range(self.tailles[2])]
      biais_output = [uniform(-1, 1) for _ in range(self.tailles[3])]
      self.biais.append(biais_l1)
      self.biais.append(biais_l2)
      self.biais.append(biais_output)

  def calcule_couche(self, taille_couche, couche_prec, poids, biais, activation):
    """
    taille_couche -- une liste de flottants
    couche_prec -- une liste de flottants
    poids -- une liste de flottants
    biais -- une liste de flottants
    activation -- une fonction prenant un flottant, retournant un flottant

    Calcule pour chaque neurone de la couche sa valeur, selon la couche precedente, les poids, les biais et la fonction d'activation
    """
    nouvelle_couche = []
    for i_neurone in range(taille_couche):
      somme_ponderee = biais[i_neurone]
      for i_neurone_prec, neurone_prec in enumerate(couche_prec):
        somme_ponderee += neurone_prec * poids[i_neurone][i_neurone_prec]
      nouvelle_couche.append(activation(somme_ponderee))
    return nouvelle_couche

  def calcule_reseau(self, input_neurones):
    self.neurones[0] = input_neurones
    #for i_couche in range(1, len(self.neurones)):
      #self.calcule_couche(self.tailles[i_couche], self.neurones[i_couche - 1], self.poids[i_couche - 1], self.biais[i_couche - 1], tanh if i_couche < len(self.neurones) - 1 else sigmoid)
    self.neurones[1] = self.calcule_couche(self.tailles[1], self.neurones[0], self.poids[0], self.biais[0], tanh)
    self.neurones[2] = self.calcule_couche(self.tailles[2], self.neurones[1], self.poids[1], self.biais[1], tanh)
    self.neurones[3] = self.calcule_couche(self.tailles[3], self.neurones[2], self.poids[2], self.biais[2], sigmoid)
    return self.neurones[3]

  def write(self, chemin_fichier):
    with open(chemin_fichier, "w") as fichier:
      # Format du fichier:
      # Taille de chaque couche sur une seule ligne (4 couches dans tous les cas)
      tailles_ligne = ""
      for taille in self.tailles:
        tailles_ligne += str(taille) + " "
      fichier.write(tailles_ligne[:-1] + "\n")

      # Poids de chaque connexion
      # Sur chaque ligne, poids pour un neurone avec tous ceux de la couche precedente
      for couche in range(1, len(self.neurones)):
        for neurone in range(len(self.neurones[couche])):
          ligne_poids = ""
          for connexion in range(len(self.neurones[couche - 1])):
            ligne_poids += str(self.poids[couche - 1][neurone][connexion]) + " "
          fichier.write(ligne_poids[:-1] + "\n")

      # Biais de chaque neurone
      # Sur chaque ligne, biais pour chaque neurone de la couche
      for couche in range(1, len(self.neurones)):
        ligne_biais = ""
        for neurone in range(len(self.neurones[couche])):
          ligne_biais += str(self.biais[couche - 1][neurone]) + " "
        fichier.write(ligne_biais[:-1] + "\n")

      fichier.close()
  
neural_network = NeuralNetwork("nn")


def check_chances(chances_dico):
  """
  chances_dico -- un dictionnaire de flottants

  verifie si la somme de tous les elements du dictionnaire donne 1
  """
  chances = chances_dico.values()
  s = 0
  for chance in chances:
    s += chance
  return s == 1.00

def gen_grille(largeur,hauteur):
  """
  largeur -- la largeur de la grille
  hauteur -- la hauteur de la grille

  retourne une liste de listes de False de largeur et hauteur donnees
  """
  return[[0 for _ in range(largeur)] for _ in range(hauteur)]
  
def choix_blocs(blocs_dico, chances_dico, nb):
  """
  blocs_dico -- un dictionnaire de listes de listes
  chances_dico -- un dictionnaire de flottants
  nb -- un entier

  retourne un nombre de blocs aleatoires suivant le dictionnaire de chances
  """
  blocs = blocs_dico.keys()
  blocs_ponderes = []
  for bloc in blocs:
    chance = 100 * chances_dico.get(bloc)
    for _ in range(int(chance)):
      blocs_ponderes.append(bloc)
  blocs_choisis = []
  for _ in range(nb):
    indice = randint(0, len(blocs_ponderes) - 1)
    blocs_choisis.append(blocs_dict.get(blocs_ponderes[indice]))
  return blocs_choisis
  
def affiche(bloc, numeros=True, offset=0):
  """
  bloc -- une liste de listes de booleens
  numeros -- un booleen

  affiche le bloc dans la console avec les nombres en abscisse si demande
  """
  index = len(bloc)
  for ligne in bloc:
    print(" " * offset, end=" ")
    for case in ligne:
      #□
      print("■" if case else " ", end=" ")
    if numeros:
      print(index, end=" ")
      index -= 1
    print("")
  if numeros:
    print("", end=" ")
    for i in range(len(bloc[0])):
      print(i+1, end=" ")
    print("")
    
def affiche_blocs(blocs):
  """
  blocs -- une liste de listes de listes

  Affiche une liste de différents blocs sur une meme ligne
  """
  for i in range(max([len(bloc) for bloc in blocs])):
    for bloc in blocs:
      if i >= len(bloc):
        print(" " * 2 * len(bloc[0]) + " " * 10, end=" ")
        continue
      for case in bloc[i]:
        print("■" if case else " ", end=" ")
      print(" " * 10, end=" ")
    print(" ")
    
def affiche_bloc_plateau(plateau, bloc, position):
  """
  plateau -- une liste de listes
  bloc -- une liste de listes
  position -- entier

  Affiche le bloc au dessus du plateau avec la position actuelle
  """
  affiche(bloc, numeros=False, offset=position)
  print("\n")
  affiche(plateau)

def tourne(bloc, cw=True):
  """
  bloc -- une liste de listes (ou tuple de tuples) de booleens
  ccw -- booleen, sens de la rotation, horaire par defaut

  retourne une liste de liste du bloc tourne, avec les dimensions adaptees

  >>> tourne(((1, 1, 0), (0, 1, 1), (0, 1, 0)))
  [[0, 0, 1], [1, 1, 1], [0, 1, 0]]
  >>> tourne(((1, 1, 0), (0, 1, 1), (0, 1, 0)), cw=False)
  [[0, 1, 0], [1, 1, 1], [1, 0, 0]]
  >>> tourne(((1, 1, 1),))
  [[1], [1], [1]]
  >>> tourne(((1, 0, 1), (1, 1, 1)), cw=False)
  [[1, 1], [0, 1], [1, 1]]
  >>> tourne(((1, 0, 1), (1, 1, 1)), cw=True)
  [[1, 1], [1, 0], [1, 1]]
  """
  resultat=[]
  for i in range(cw - 1, cw * 2 * len(bloc[0])-len(bloc[0]) + cw - 1, cw * 2 - 1):
    ligne = []
    for j in range(-cw, len(bloc) - cw * 2 * len(bloc) - cw, 1 - cw * 2):
      ligne.append(bloc[j][i])
    resultat.append(ligne)
  return resultat

def compte_blocs(bloc):
  """
  bloc -- une liste de listes de booleens

  renvoie le nombre de 1 dans le bloc

  >>> compte_blocs([[1, 0], [0, 1]])
  2
  >>> compte_blocs([[0],[0]])
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
  >>> copie_grille([[1, 0], [0, 1]])
  [[1, 0], [0, 1]]
  """
  return [[case for case in ligne] for ligne in grille]

def ajoute_bloc(plateau, bloc, offset_x, offset_y):
  """
  plateau -- une liste de listes de booleens
  bloc -- une liste de listes de booleens
  offsetX -- un entier
  offsetY -- un entier

  modifie plateau en ajoutant le bloc sur le plateau avec un decalage a partir du bas gauche du bloc
  """
  for i in range(len(bloc)):
    for j in range(len(bloc[0])):
      if bloc[i][j]:
        plateau[offset_y + i][offset_x + j] = bloc[i][j]

def tombe(plateau, bloc, x):
  """
  plateau -- le plateau a modifier, a effet de bord
  bloc -- le bloc a pose
  x -- la position x ou poser le bloc, concerne le bout le plus a gauche
  
  fait tomber un bloc sur le plateau avec un abscisse donne
  """
  total_blocs = compte_blocs(bloc) + compte_blocs(plateau)
  hauteur = 0
  while hauteur + len(bloc) <= len(plateau):
    copie = copie_grille(plateau)
    ajoute_bloc(copie, bloc, x, hauteur)
    if total_blocs != compte_blocs(copie):
      if hauteur - 1 < 0:
        return -1
      break
    hauteur += 1
  ajoute_bloc(plateau, bloc, x, hauteur - 1)

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

def tombe_lignes_finies(plateau, indices_lignes):
  """
  plateau -- une liste de listes de booleens
  indice_lignes -- une liste d'indices des lignes a supprimer

  supprime les lignes aux indices donnes et fait descendre les lignes dessus
  """
  vide = [0 for _ in plateau[0]]
  indices_lignes.sort()
  for indice in indices_lignes:
    for i in range(indice, 0, -1):
      plateau[i] = plateau[i-1]
    plateau[0] = vide

def lignes_finies(plateau):
  """
  plateau -- une liste de listes de booleens

  supprime les lignes finies du plateau et fait descendre les lignes dessus
  """
  lignes_completes = detect_lignes(plateau)
  tombe_lignes_finies(plateau, lignes_completes)

def tour(plateau, blocs):
  # Afficher les choix possibles
  affiche_blocs(blocs)
  
  # 1. Choisir un bloc
  bloc_indice = -1
  while bloc_indice == -1:
    bloc_indice_input = input(f"Choisissez votre bloc [{1};{len(blocs)}]: ")
    if len(bloc_indice_input) == 0:
      bloc_indice = 1
      break
    bloc_indice = int(bloc_indice_input)
    if not 1 <= bloc_indice <= len(blocs):
      bloc_indice = -1
  
  bloc = blocs[bloc_indice-1]
  
  # Afficher le bloc choisi au milieu du plateau
  milieu = (len(plateau[0]) - len(bloc[0])) // 2 + 2
  affiche_bloc_plateau(plateau, bloc, milieu)
      
  # 2. Choisir une orientation
  cw = -1
  while cw == -1:
    cw_input = input("Choisissez un sens de rotation, 0=anti-horaire, 1=horaire: ")
    if len(cw_input) == 0:
      cw = -2
      break
    cw = int(cw_input)
    if cw != 0 and cw != 1:
      cw = -1
      
  if cw != -2:
    nb_tours = -1
    while nb_tours == -1:
      nb_tours_input = input("Choisissez un nombre de tours pour la rotation [0;4]: ")
      if len(nb_tours_input) == 0:
        nb_tours = 1
        break
      nb_tours = int(nb_tours_input)
      if not 0 < nb_tours < 4:
        nb_tours = -1
        
    for _ in range(nb_tours):
      bloc = tourne(bloc, cw=bool(cw))
      
    milieu = (len(plateau[0]) - len(bloc[0])) // 2 + 1
    affiche_bloc_plateau(plateau, bloc, (milieu - 1) * 2)
  
  
  # 3. Choisir une abscisse
  debut = 1
  fin = len(plateau[0]) - len(bloc[0]) + 1
  position = -1
  while position == -1:
    position_input = input(f"Choisissez une position pour le bloc [{debut};{fin}]: ")
    if len(position_input) == 0:
      position = milieu - 1
      break
    position = int(position_input)
    if not debut <= position <= fin:
      position = -1
      
  if tombe(plateau, bloc, position - 1) != -1:
    lignes_finies(plateau)
    affiche(plateau)
    blocs.pop(bloc_indice - 1)
    return 1
  return -1

def formatte_bloc(bloc, w, h):
  """
  bloc -- une liste de listes d'entiers
  w -- un entier
  h -- un entier

  renvoie une liste de listes d'entiers contenant les valeurs de bloc mais etant de longueur h et de longueur interne w, on remplace par 0 les valeurs qui n'existent pas
  """
  bloc_format = []
  for i in range(len(bloc)):
    ligne = []
    for j in range(len(bloc[0])):
      ligne.append(bloc[i][j])
    ligne.append([0 for _ in range(w - len(bloc[0]))])
    bloc_format.append(ligne)
  
  vide = [0 for _ in range(w)]
  for _ in range(h - len(bloc)):
    bloc_format.append(vide)

  return bloc_format

def applati(liste):
  """
  liste -- une liste de listes

  renvoie cette une liste sans sous-liste

  >>> applati([[1, 2], 3, [4, 5, [6, 7, 8]]])
  [1, 2, 3, 4, 5, 6, 7, 8]
  >>> applati([[1, 1, 0, []], [0, 1, 1, []], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
  [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  >>> applati([((0, 1, 1), (0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 0, 0)), ((0, 0, 1), (0, 1, 1), (1, 1, 0))])
  [0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0]
  """
  nouvelle_liste = []
  for l in liste:
    if type(l) is list or type(l) is tuple:
      if len(l) > 0:
        nouvelle_liste += applati(l)
    else:
      nouvelle_liste.append(l)
  return nouvelle_liste

def tanh(x):
  return (exp(x) - exp(-x)) / (exp(x) + exp(-x))

def sigmoid(x):
  return 1.0 / (1.0 + exp(-x))

def indice_max(liste):
  """
  liste -- une liste de flottants

  retourne l'indice de l'element maximum de la liste
  """
  indice = 0
  maxi = liste[0]
  for i, l in enumerate(liste[1:]):
    if l > maxi:
      maxi = l
      indice = i
    if l == maxi:
      indice = indice if random() > 0.5 else i
  return indice

def liste_vers_dictionnaire(liste):
  """
  liste -- liste de flottants

  renvoie un dictionnaire contenant toutes les valeurs de la liste en clés (14 decimales, presque impossible qu'elles soient identiques), et l'indice de cette valeur en valeur du dico
  """
  dico = dict()
  for i, l in enumerate(liste):
    dico[l] = i
  return dico

def meilleur_bloc(liste, blocs):
  """
  liste -- une liste de flottants
  blocs -- une liste de blocs

  renvoie l'indice du bloc à choisir parmi ceux disponibles

  >>> meilleur_bloc([0.2, 0.1, 0.7], [0, 1, 2])
  2
  """
  dico = liste_vers_dictionnaire(liste)
  # On classe les choix du plus confiant au moins confiant, elles correspondent aux cles du dictionnaire
  cles = sorted(liste, reverse=True)
  for c in cles:
    if dico[c] < len(blocs):
      return dico[c]
  return 0

def meilleure_position(liste, bloc, plateau):
  """
  liste -- une liste de flottants

  retourne la "meilleure" position valide
  """
  dico = liste_vers_dictionnaire(liste)
  # On classe les choix du plus confiant au moins confiant, elles correspondent aux cles du dictionnaire
  cles = sorted(liste, reverse=True)
  print(liste)
  # On trouve les extremites possibles du bloc dans le plateau
  debut = 0
  fin = len(plateau[0]) - len(bloc[0])
  for c in cles:
    if debut <= dico[c] <= fin:
      return dico[c]

def tour_robot(plateau, blocs, blocs_adversaire):
  """
  plateau -- une liste de listes de booleens
  blocs -- une liste de listes de booleens
  blocsAdversaire -- une liste de listes de booleens

  Joue le tour du robot en fonction du plateau, de nos blocs et de ceux de l'adversaire
  """

  blocs_format = []
  bloc_vide = [0 for _ in range(15)]
  for bloc in blocs:
    blocs_format.append(formatte_bloc(bloc, 3, 5))
  if len(blocs_format) < 3:
    blocs_format.append(bloc_vide * (3 - len(blocs)))
  blocs_adversaire_format = []
  for bloc in blocs_adversaire:
    blocs_adversaire_format.append(formatte_bloc(bloc, 3, 5))
  if len(blocs_adversaire_format) < 3:
    blocs_adversaire_format.append(bloc_vide * (3 - len(blocs_adversaire)))

  input_neurones = blocs_format + blocs_adversaire_format + plateau
  input_neurones = applati(input_neurones)

  output_neurones = neural_network.calcule_reseau(input_neurones)

  # Choisi en suivant le réseau de neurones
  indice_bloc = meilleur_bloc(output_neurones[:3], blocs)
  bloc = blocs[indice_bloc]
  nb_rotations = indice_max(output_neurones[3:7])
  for _ in range(nb_rotations):
    bloc = tourne(bloc)
  position = meilleure_position(output_neurones[7:15], bloc, plateau)
  print(indice_bloc, nb_rotations, position)

  affiche_bloc_plateau(plateau, bloc, position)

  if tombe(plateau, bloc, position) != -1:
    lignes_finies(plateau)
    affiche(plateau)
    blocs.pop(indice_bloc)
    return 1
  return -1


def jeu(w, h):
  joueur1 = True
  j1_blocs = choix_blocs(blocs_dict, chances_dict, 3)
  j2_blocs = choix_blocs(blocs_dict, chances_dict, 3)
  plateau = gen_grille(w, h)
  
  print("Joueur 1 de jouer :")
  r = 1
  while r == 1:
    if joueur1:
      r = tour(plateau, j1_blocs)
    else:
      r = tour_robot(plateau, j2_blocs, j1_blocs)

    if r == -1:
      break

    if len(j1_blocs) == 0:
      j1_blocs = choix_blocs(blocs_dict, chances_dict, 3)
    if len(j2_blocs) == 0:
      j2_blocs = choix_blocs(blocs_dict, chances_dict, 3)

    joueur1 = not joueur1
    print("Joueur " + ("1" if joueur1 else "2") + " de jouer :")
 
  print("=" * 50)
  print("Joueur " + ("1" if joueur1 else "2") + " a perdu !")
  print("=" * 50)

def main():
  print("Bienvenue sur Octis !")
  print(" _____     _   _     ")
  print("|     |___| |_|_|___ ")
  print("|  |  |  _|  _| |_ -|")
  print("|_____|___|_| |_|___|")
  print("Ce jeu consiste en un Tetris en tour par tour où le but est de faire perdre l'adversaire.")
  print("Pour cela, il faut lui faire poser un bloc au dessus de la limite")

  commencer = " "
  while len(commencer) > 0:
    commencer = input("Êtes-vous prêt à commencer ? [O/n]:").lower().strip()
    if commencer == "n":
      return
    if commencer == "o":
      break
    
  jeu(8, 15)

if __name__ == "__main__":
    # On teste toutes les fonctions avant de commencer
    import doctest
    assert doctest.testmod(verbose=False).failed == 0
    
    assert not check_chances(chances_dict), "Les chances ne coincident pas :/"

    # On appelle la fonction principale
    main()
