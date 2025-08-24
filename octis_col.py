from random import randint

# Definitions des blocs
blocs_dict = {  "un": ((1,),),

                "f": ((1, 1, 0),
                      (0, 1, 1),
                      (0, 1, 0)),

                "i": ((1, 1, 1, 1),),

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


def check_chances(chances_dico):
  """
  chances_dico -- dictionnaire de flottants

  vérifie si la somme de tous les éléments du dictionnaire donne 1
  """
  chances = chances_dico.values()
  s = 0
  for chance in chances:
    s += chance
  return s == 1.00

def gen_grille(largeur,hauteur):
  """
  largeur -- entier
  hauteur -- entier

  renvoie un plateau rempli de -1 de la largeur et de la hauteur données
  """
  return [[-1 for _ in range(largeur)] for _ in range(hauteur)]

def choix_blocs(blocs_dico, chances_dico):
  """
  blocs_dico -- dictionnaire de listes de listes
  chances_dico -- dictionnaire de flottants

  retourne une liste de 3 blocs aléatoires en suivant le dictionnaire de chances
  """
  blocs = blocs_dico.keys()
  blocs_ponderes = []
  for bloc in blocs:
    chance = 100 * chances_dico.get(bloc)
    for _ in range(int(chance)):
      blocs_ponderes.append(bloc)
  blocs_choisis = []

  for _ in range(3):
    indice = randint(0, len(blocs_ponderes) - 1)
    blocs_choisis.append(blocs_dict.get(blocs_ponderes[indice]))
  return blocs_choisis

def choix_couleurs():
  """
  renvoie une liste d'indices de 3 couleurs en suivant le code ANSI
  Liste des couleurs possibles:
  Rouge (31)
  Vert (32)
  Orange (33)
  Bleu (34)
  Violet (35)
  Cyan (36)
  """
  return [randint(31, 36) for _ in range(3)]

def print_couleur(texte, couleur, end="\n"):
  """
  texte -- chaine de caractères
  couleur -- entier
  end -- (optionel) chaine de caractères

  affiche dans la console le texte avec une couleur en suivant le code ANSI
  """
  print(f"\033[{couleur}m{texte}\033[0m", end=end)

def affiche_bloc(bloc, couleur, offset=0):
  """
  blocs -- tuples de tuples de booléens

  affiche un bloc avec une certaine couleur ANSI et un décalage sur la gauche
  """
  for ligne in bloc:
    print(" " * (offset - 1), end=" ")
    for case in ligne :
      if case:
        print_couleur("■", couleur, end=" ")
      else:
        print(" ", end=" ")
    print("")

def affiche_choix_blocs(blocs, couleurs):
  """
  blocs -- liste de tuples de tuples de booléens
  couleurs -- liste d'entiers

  affiche une liste de blocs colorés sur la même ligne
  """
  for i in range(max([len(bloc) for bloc in blocs])):
    for i_bloc, bloc in enumerate(blocs):
      if i >= len(bloc):
        print(" " * 2 * len(bloc[0]) + " " * 10, end=" ")
        continue
      for case in bloc[i]:
        if case:
          print_couleur("■", couleurs[i_bloc], end=" ")
        else:
          print(" ", end=" ")
      print(" " * 10, end=" ")
    print(" ")

def affiche_plateau(plateau):
  """
  plateau -- liste de listes d'entiers

  affiche le plateau dans la console avec les numéros sur le côté et les blocs colorés
  """
  for indice, ligne in enumerate(plateau):
    print("", end=" ")
    for case in ligne:
      if case == -1:
        print(" ", end=" ")
      else:
        print_couleur("■", case, end=" ")
    print(len(plateau)-indice)
  print("", end=" ")
  for i in range(len(plateau[0])):
    print(i+1, end=" ")
  print("")

def affiche_bloc_plateau(plateau, bloc, couleur, position):
  """
  plateau -- liste de listes d'entiers
  bloc -- tuple de tuples de booléens
  couleur -- entier
  position -- entier

  affiche le bloc coloré au-dessus du plateau
  """
  affiche_bloc(bloc, couleur, offset=position)
  print("\n")
  affiche_plateau(plateau)

def tourne(bloc, cw=True):
  """
  bloc -- tuple de tuples de booléens
  ccw -- booléen

  tourne le bloc, avec les dimensions adaptees et dans le sens spécifié

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
  resultat = []
  for i in range(cw - 1, cw * 2 * len(bloc[0])-len(bloc[0]) + cw - 1, cw * 2 - 1):
    ligne = []
    for j in range(-cw, len(bloc) - cw * 2 * len(bloc) - cw, 1 - cw * 2):
      ligne.append(bloc[j][i])
    resultat.append(ligne)
  return resultat

def compte_blocs(bloc):
  """
  bloc -- tuple de tuples de booléens

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

def compte_plateau(plateau):
  """
  plateau -- liste de listes d'entiers

  renvoie le nombre d'entiers différents de -1

  >>> compte_plateau([[-1, 31], [34, -1]])
  2
  >>> compte_plateau([[31],[-1]])
  1
  """
  nombre=0
  for ligne in plateau:
    for case in ligne:
      if case != -1:
        nombre += 1
  return nombre

def copie_grille(grille):
  """
  grille -- liste de listes de booleens
  
  renvoie une copie de la grille
  >>> copie_grille([[1, 0], [0, 1]])
  [[1, 0], [0, 1]]
  """
  return [[case for case in ligne] for ligne in grille]

def ajoute_bloc(plateau, bloc, couleur, offset_x, offset_y):
  """
  plateau -- liste de listes de booléens
  bloc -- liste de listes de booléens
  couleur -- entier
  offsetX -- entier
  offsetY -- entier

  modifie plateau en y ajoutant le bloc coloré avec un décalage a partir du coin en bas à gauche du bloc

  >>> ajoute_bloc([[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]], ((1, 0), (1, 1)), 30, 1, 2)
  [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, 30, -1, -1], [-1, 30, 30, -1]]
  """
  for i in range(len(bloc)):
    for j in range(len(bloc[0])):
      if bloc[i][j]:
        plateau[offset_y + i][offset_x + j] = couleur
  return plateau

def tombe(plateau, bloc, couleur, x):
  """
  plateau -- liste de listes d'entiers
  bloc -- tuple de tuples de booléens
  x -- entier

  fait tomber le bloc sur le plateau, en tenant compte de ceux éxistant, à une abscisse x donnée
  """
  total_blocs = compte_blocs(bloc) + compte_plateau(plateau)
  hauteur = 0
  while hauteur + len(bloc) <= len(plateau):
    copie = copie_grille(plateau)
    ajoute_bloc(copie, bloc, couleur, x, hauteur)
    if total_blocs != compte_plateau(copie):
      if hauteur - 1 < 0:
        return -1
      break
    hauteur += 1
  ajoute_bloc(plateau, bloc, couleur, x, hauteur - 1)

def detecte_lignes_finies(plateau):
  """
  plateau -- liste de listes d'entiers

  détecte et renvoie une liste des indices de toutes les lignes complétées sur le plateau
  """
  lignes_completes = []
  for indice, ligne in enumerate(plateau):
    if not -1 in ligne:
      lignes_completes.append(indice)
  return lignes_completes

def tombe_lignes_finies(plateau, indices_lignes):
  """
  plateau -- liste de listes d'entiers
  indices_lignes -- liste d'indices des lignes à supprimer

  supprime les lignes aux indices donnés et fait descendre les lignes dessus
  """
  vide = [-1 for _ in plateau[0]]
  indices_lignes.sort()
  for indice in indices_lignes:
    for i in range(indice, 0, -1):
      plateau[i] = plateau[i-1]
    plateau[0] = vide

def supprime_lignes_finies(plateau):
  """
  plateau -- liste de listes d'entiers

  supprime les lignes finies du plateau et fait descendre les lignes dessus
  """
  lignes_completes = detecte_lignes_finies(plateau)
  tombe_lignes_finies(plateau, lignes_completes)

def tour(plateau, blocs, couleurs):
  # Afficher les choix possibles
  affiche_choix_blocs(blocs, couleurs)

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
  couleur = couleurs[bloc_indice-1]

  milieu = (len(plateau[0]) - len(bloc[0])) // 2 + 1
  affiche_bloc_plateau(plateau, bloc, couleur, milieu * 2 - 1)

  # 2. Choisir une orientation
  cw = -1
  while cw == -1:
    cw_input = input("Choisissez un sens de rotation, 0=anti-horaire, 1=horaire: ")
    if len(cw_input) == 0:
      cw = -2
      break
    cw = int(cw_input)
    if cw != 1 and cw != 0:
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
    affiche_bloc_plateau(plateau, bloc, couleur, milieu * 2 - 1)


  # 3. Choisir une abscisse
  debut = 1
  fin = len(plateau[0]) - len(bloc[0]) + 1
  position = -1
  while position == -1:
    position_input = input(f"Choisissez une position pour le bloc [{debut};{fin}]: ")
    if len(position_input) == 0:
      position = milieu
      break
    position = int(position_input)
    if not debut <= position <= fin:
      position = -1

  if tombe(plateau, bloc, couleur, position - 1) != -1:
    supprime_lignes_finies(plateau)
    affiche_plateau(plateau)
    blocs.pop(bloc_indice - 1)
    couleurs.pop(bloc_indice-1)
    return 1
  return -1


def jeu(w, h):
  joueur1 = True
  j1_blocs = choix_blocs(blocs_dict, chances_dict)
  j1_couleurs = choix_couleurs()
  j2_blocs = choix_blocs(blocs_dict, chances_dict)
  j2_couleurs = choix_couleurs()
  plateau = gen_grille(w, h)

  print("Joueur 1 de jouer :")
  while tour(plateau, j1_blocs if joueur1 else j2_blocs, j1_couleurs if joueur1 else j2_couleurs) == 1:
    joueur1 = not joueur1

    if len(j1_blocs) == 0:
      j1_blocs = choix_blocs(blocs_dict, chances_dict)
      j1_couleurs = choix_couleurs()

    if len(j2_blocs) == 0:
      j2_blocs = choix_blocs(blocs_dict, chances_dict)
      j2_couleurs = choix_couleurs()

    print("Joueur " + ("1" if joueur1 else "2") + " de jouer :")

  print("=" * 50)
  print("Joueur " + ("1" if joueur1 else "2") + " a perdu !")
  print("=" * 50)

def main():
  print_couleur("Bienvenue sur Octis", 34)
  print(" _____     _   _     ")
  print("|     |___| |_|_|___ ")
  print("|  |  |  _|  _| |_ -|")
  print("|_____|___|_| |_|___|")
  print("Ce jeu consiste en un Tetris en tour par tour où le but est de faire perdre l'adversaire.")
  print("Pour cela, il faut lui faire poser un bloc au dessus de la limite")

  commencer = " "
  while len(commencer) > 0:
    commencer = input("Êtes-vous prêt à commencer ? [O/n]:")
    if commencer == "n" or commencer == "N":
      return
    if commencer == "O" or commencer == "o":
      break

  jeu(8, 15)

if __name__ == "__main__":
    # On teste toutes les fonctions avant de commencer
    import doctest
    assert doctest.testmod(verbose=False).failed == 0

    assert not check_chances(chances_dict), "Les chances ne coincident pas :/"

    # On appelle la fonction principale
    main()
