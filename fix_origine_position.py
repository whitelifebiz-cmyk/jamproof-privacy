# -*- coding: utf-8 -*-
"""
fix_origine_position.py - JamProof, politique de confidentialite
26 octobre 2026

Ajoute un paragraphe a la section 2 pour dire d'ou vient la position.

La politique n'etait pas fausse : elle n'a jamais pretendu au satellite,
et « aucune coordonnee n'est envoyee a un service de cartographie ou de
geocodage » reste vrai. Mais elle restait muette sur l'origine de la
position, alors que la page Confidentialite de l'app, elle, le dit
desormais. Deux documents qui parlent de la meme chose doivent dire la
meme chose, avec les memes mots, et c'est celui-ci qui est opposable.

Contexte : le flux de position passe par le Fused Location Provider des
services Google Play, qui croise GPS, reseaux Wi-Fi et antennes mobiles.
L'app n'a aucune permission Wi-Fi et ne scanne rien elle-meme, mais le
systeme scanne pour son compte. Un utilisateur le voit dans les details
de batterie de son telephone : il doit retrouver l'explication ici.

La date de derniere mise a jour est avancee au 26 octobre : une
politique de confidentialite qui change porte la date du changement.

Un script plutot qu'une edition directe, et pour ce fichier-ci plus que
pour tout autre : c'est cette page que VS Code avait un jour ecrasee
avec le site vitrine, l'onglet actif n'etant pas celui qu'on croyait.
"""
import datetime
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))
FICHIER = os.path.join(RACINE, 'index.html')
HORO = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

ANCIEN_PARAGRAPHE = """  <p>Le signal GPS sert uniquement à mesurer une vitesse et une distance. Aucune coordonnée n'est envoyée à un service de cartographie ou de géocodage. Les rapports PDF sont créés sur l'appareil ; vous seul décidez de les partager, par courriel, messagerie ou tout autre moyen de votre choix.</p>"""

NOUVEAU_PARAGRAPHE = """  <p>Le signal GPS sert uniquement à mesurer une vitesse et une distance. Aucune coordonnée n'est envoyée à un service de cartographie ou de géocodage. Les rapports PDF sont créés sur l'appareil ; vous seul décidez de les partager, par courriel, messagerie ou tout autre moyen de votre choix.</p>

  <p>La position est fournie par le service de localisation d'Android, qui combine le GPS et, si la précision de localisation Google est activée sur votre appareil, les réseaux Wi-Fi et les antennes mobiles à proximité. Ce traitement relève de Google et de vos propres réglages, que vous pouvez modifier à tout moment dans les paramètres de votre téléphone. JamProof n'en reçoit qu'une position, qu'elle ne transmet à personne.</p>"""

ANCIENNE_DATE = "Dernière mise à jour : 11 octobre 2026"
NOUVELLE_DATE = "Dernière mise à jour : 26 octobre 2026"


def main():
    with open(FICHIER, encoding='utf-8', newline='') as fh:
        c = fh.read()

    for ancien, nouveau, etiquette in (
        (ANCIEN_PARAGRAPHE, NOUVEAU_PARAGRAPHE, 'paragraphe sur la position'),
        (ANCIENNE_DATE, NOUVELLE_DATE, 'date de mise a jour'),
    ):
        n = c.count(ancien)
        if n != 1:
            raise ValueError("%s : motif trouve %d fois au lieu d'une seule"
                             % (etiquette, n))
        c = c.replace(ancien, nouveau)

    # Le nouveau texte doit etre present, et les balises equilibrees.
    if 'les réseaux Wi-Fi et les antennes mobiles à proximité' not in c:
        raise ValueError('le nouveau paragraphe est absent apres remplacement')
    if c.count('<p>') != c.count('</p>'):
        raise ValueError('balises <p> desequilibrees : %d ouvrantes, %d fermantes'
                         % (c.count('<p>'), c.count('</p>')))

    shutil.copy2(FICHIER, '%s.backup_%s' % (FICHIER, HORO))
    with open(FICHIER, 'w', encoding='utf-8', newline='') as fh:
        fh.write(c)
    print('ecrit   index.html : origine de la position + date au 26 octobre')


if __name__ == '__main__':
    try:
        main()
    except ValueError as err:
        print("ECHEC, rien n'a ete ecrit : %s" % err)
        sys.exit(1)
