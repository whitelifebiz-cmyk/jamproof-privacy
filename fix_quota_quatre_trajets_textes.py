# -*- coding: utf-8 -*-
"""
fix_quota_quatre_trajets_textes.py - JamProof, 27 octobre 2026

Le quota gratuit passe de dix a quatre trajets. Voir
fix_quota_quatre_trajets.py dans le depot de l'app pour l'arbitrage :
quatre pour rendre la fraude sans interet, et un nombre pair pour ne pas
bloquer l'utilisateur entre son aller et son retour.

Les deux documents citent le chiffre en toutes lettres et doivent suivre.
Un document opposable qui annonce dix trajets quand l'application en donne
quatre est une promesse non tenue.

Les conditions prevoyaient deja ce cas : « le nombre de trajets gratuits
et le tarif peuvent etre modifies pour les nouveaux utilisateurs ».

La date de derniere mise a jour est avancee sur les deux. Celle des
conditions portait le 1er novembre, une date future qui n'avait plus lieu
d'etre.

Ce depot est en CRLF. Les motifs ci-dessous tiennent sur une seule ligne,
donc la fin de ligne n'intervient pas — mais ne pas l'oublier pour un
motif multiligne, qui ne correspondrait jamais.
"""
import datetime
import os
import shutil
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))
HORO = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
AUJOURDHUI = '27 octobre 2026'

PAIRES = [
    ('index.html',
     "L'application propose 10 trajets gratuits, puis un abonnement mensuel.",
     "L'application propose 4 trajets gratuits, puis un abonnement mensuel.",
     'politique, section 4'),

    ('index.html',
     "Dernière mise à jour : 26 octobre 2026",
     "Dernière mise à jour : %s" % AUJOURDHUI,
     'date de la politique'),

    ('conditions.html',
     "L'application permet d'enregistrer dix trajets sans paiement.",
     "L'application permet d'enregistrer quatre trajets sans paiement.",
     'conditions, section 4'),

    ('conditions.html',
     "Dernière mise à jour : 1er novembre 2026",
     "Dernière mise à jour : %s" % AUJOURDHUI,
     'date des conditions'),
]


def main():
    etat = {}
    for fichier, ancien, nouveau, etiquette in PAIRES:
        chemin = os.path.join(RACINE, fichier)
        c = etat.get(chemin)
        if c is None:
            with open(chemin, encoding='utf-8', newline='') as fh:
                c = fh.read()
        n = c.count(ancien)
        if n != 1:
            raise ValueError("%s : motif trouve %d fois au lieu d'une seule"
                             % (etiquette, n))
        etat[chemin] = c.replace(ancien, nouveau)

    for chemin, contenu in etat.items():
        nom = os.path.basename(chemin)
        for interdit in ('10 trajets', 'dix trajets'):
            if interdit in contenu:
                raise ValueError('%s cite encore « %s »' % (nom, interdit))
        if contenu.count('<p>') != contenu.count('</p>'):
            raise ValueError('%s : balises <p> desequilibrees' % nom)

    for chemin, contenu in etat.items():
        shutil.copy2(chemin, '%s.backup_%s' % (chemin, HORO))
        with open(chemin, 'w', encoding='utf-8', newline='') as fh:
            fh.write(contenu)
        print('ecrit   %s' % os.path.basename(chemin))


if __name__ == '__main__':
    try:
        main()
    except ValueError as err:
        print("ECHEC, rien n'a ete ecrit : %s" % err)
        sys.exit(1)
