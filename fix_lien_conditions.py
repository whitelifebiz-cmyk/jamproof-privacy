# -*- coding: utf-8 -*-
"""
fix_lien_conditions.py - JamProof, 26 octobre 2026

Ajoute dans le pied de page de la politique de confidentialite un lien
vers conditions.html, qui renvoie deja vers elle. Les deux documents
doivent etre atteignables l'un depuis l'autre : la politique est l'URL
declaree dans la Play Console, c'est par elle qu'un lecteur arrive.

Ce depot est en CRLF, contrairement aux fichiers Dart de l'app. Un motif
qui couvre plusieurs lignes doit donc etre construit avec la fin de
ligne du fichier, sinon il ne correspond jamais. Le script la detecte.
"""
import datetime, os, shutil, sys

RACINE = os.path.dirname(os.path.abspath(__file__))
FICHIER = os.path.join(RACINE, 'index.html')
HORO = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

ANCIEN = """  <footer>
    <p>© 2026 Whitelife Studio · JamProof v1.0<br>
    Dernière mise à jour : 26 octobre 2026</p>
  </footer>"""

NOUVEAU = """  <footer>
    <p>© 2026 Whitelife Studio · JamProof v1.0<br>
    Dernière mise à jour : 26 octobre 2026</p>
    <p><a href="conditions.html">Conditions générales d'utilisation</a></p>
  </footer>"""

if not os.path.exists(os.path.join(RACINE, 'conditions.html')):
    print("ECHEC, rien n'a ete ecrit : conditions.html est absent")
    sys.exit(1)

with open(FICHIER, encoding='utf-8', newline='') as fh:
    c = fh.read()

fin = '\r\n' if '\r\n' in c else '\n'
ancien = ANCIEN.replace('\n', fin)
nouveau = NOUVEAU.replace('\n', fin)

n = c.count(ancien)
if n != 1:
    print("ECHEC, rien n'a ete ecrit : pied de page trouve %d fois "
          "(fin de ligne detectee : %r)" % (n, fin))
    sys.exit(1)

c = c.replace(ancien, nouveau)
if c.count('<p>') != c.count('</p>'):
    print("ECHEC, rien n'a ete ecrit : balises <p> desequilibrees")
    sys.exit(1)
if 'conditions.html' not in c:
    print("ECHEC, rien n'a ete ecrit : le lien est absent apres remplacement")
    sys.exit(1)

shutil.copy2(FICHIER, '%s.backup_%s' % (FICHIER, HORO))
with open(FICHIER, 'w', encoding='utf-8', newline='') as fh:
    fh.write(c)
print('ecrit   index.html : lien vers les conditions ajoute')
