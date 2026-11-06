# Trombinoscope Patriotes pour l’Europe

Annuaire indépendant du groupe au Parlement européen, 10e législature. Recherche, filtres par pays et parti, chefs de délégation, coordinateurs documentés, affichage compact et cartes d’entraînement.

## Mettre à jour

1. Sur le site, ouvrez **Mettre à jour les données** et exportez le fichier JSON.
2. Modifiez les informations en conservant les identifiants du Parlement. Importez le JSON sur le site pour vérifier les fiches. Cet import ne modifie que l’onglet courant : rien n’est publié.
3. Exportez le JSON validé puis remplacez `members.json` dans ce dépôt : ouvrez le fichier, cliquez sur le crayon, collez le contenu et enregistrez le commit.
4. GitHub Pages publie la modification. Vérifiez le site après le déploiement.

Le CSV est prévu pour consulter la liste dans un tableur. Seul le JSON peut être réimporté. Les données sont figées à leur date de récupération ; aucune synchronisation ni tâche planifiée n’est activée.

### Champs d’une fiche

| Champ | Contenu |
| --- | --- |
| `id` | Identifiant numérique du député, sous forme de texte |
| `name`, `lastName` | Nom complet et nom de famille pour le tri |
| `country`, `party` | Pays (nom anglais du Parlement) et parti national |
| `membershipCheckedAt` | Date de récupération de la liste : YYYY-MM-DD |
| `role`, `isBureau` | Fonction et appartenance confirmée au bureau |
| `roleSource`, `roleCheckedAt` | Source officielle et date de consultation |
| `headOfDelegation` | `true` si la fonction est confirmée, sinon `false` |
| `headSource`, `headCheckedAt` | Source officielle et date de consultation |
| `coordinators` | Liste d’objets : `committee`, `source`, `sourceDate`, `checkedAt` |

Exemple de coordinateur (à adapter à une source réelle) :

```json
{"committee":"CULT","source":"https://www.europarl.europa.eu/…","sourceDate":"2026-02-12","checkedAt":"2026-11-06"}
```

Les liens de sources acceptés pointent vers les sites officiels du Parlement ou des groupes. Les dates des documents peuvent être antérieures à la consultation. La couverture des fonctions est **partielle** : l’absence de badge ne prouve pas l’absence de fonction. Les membres d’une commission ne sont jamais automatiquement considérés comme coordinateurs.

### Rafraîchir les membres depuis un ordinateur

Python 3, sans dépendance supplémentaire :

```sh
python refresh_members.py
python refresh_members.py --write
```

La première commande affiche les entrées et sorties sans modifier le fichier. La seconde actualise le JSON local. Vérifiez les différences puis envoyez-les sur GitHub. Les fonctions existantes sont conservées par identifiant et doivent être revérifiées séparément. Les nouveaux membres n’héritent d’aucune fonction. Pour ESN, ajoutez leur portrait officiel dans `photos/<id>.jpg`.

## Sources et limites

Liste : Parlement européen. Fonctions : pages des groupes et documents du Parlement, avec source et date dans les fiches. Les places en hémicycle ne sont pas renseignées.

Entraînement : quiz à 3 ou 4 noms. Les photos suivent les filtres ; les propositions aléatoires proviennent de tout le groupe et ont le même sexe renseigné dans les données du Parlement. Le score est calculé automatiquement, sans possibilité de répondre deux fois à une question. Les erreurs peuvent être rejouées. Une fiche sans sexe renseigné est exclue du quiz. Les résultats restent dans l’onglet et ne sont pas enregistrés. La préférence d’affichage compact est conservée dans le navigateur.

## Données du quiz

`gender` contient `MALE`, `FEMALE` ou une chaîne vide, selon `hasGender` dans la fiche officielle de l’API Open Data du Parlement. `genderSource` conserve le lien de cette fiche. Ne pas déduire cette valeur d’un prénom ou d’une photo. Un groupe d’au moins trois noms de même sexe est nécessaire au quiz ; les filtres portent sur les photos interrogées, pas sur les propositions.

Les libellés « Coordinateur des votes » et « Coordinateur adjoint des votes » désignent les fonctions de chief whip et deputy whip. Ils sont distincts des coordinateurs de commission.
