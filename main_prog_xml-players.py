import os
import xml.etree.ElementTree as ET

# Temps à rajouter au début et à la fin de chaque clip
rajout = 5

# Définir le dossier d'entrée et de sortie
dossier_entree = './xml-import'
dossier_sortie = './xml-export'

# Fonction pour ajuster les plages de temps
def ajuster_temps(instances, ajustement=rajout):
    for instance in instances:
        start_time = float(instance.find('start').text)
        end_time = float(instance.find('end').text)

        # Ajuster le début et la fin de chaque plage de temps
        instance.find('start').text = str(start_time - ajustement)
        instance.find('end').text = str(end_time + ajustement)

# Fonction pour fusionner les instances qui se chevauchent et ont le même "code"
def fusionner_instances(instances):
    instances = sorted(instances, key=lambda x: float(x.find('start').text))
    fusionnes = []
    instance_courante = instances[0]

    for instance in instances[1:]:
        # Vérifier s'il y a un chevauchement ET si le code est identique
        if (float(instance.find('start').text) <= float(instance_courante.find('end').text) and
            instance.find('code').text == instance_courante.find('code').text):

            # Fusionner en ajustant la fin
            instance_courante.find('end').text = str(max(float(instance_courante.find('end').text),
                                                        float(instance.find('end').text)))

            # Concaténer les informations supplémentaires si nécessaire
            for label in instance.findall('label'):
                instance_courante.append(label)

        else:
            # Si pas de chevauchement ou "code" différent, ajouter l'instance courante à la liste fusionnée
            fusionnes.append(instance_courante)
            instance_courante = instance

    # Ajouter la dernière instance à la liste fusionnée
    fusionnes.append(instance_courante)
    return fusionnes

# Fonction pour traiter un fichier XML donné
def traiter_fichier_xml(fichier_entree, fichier_sortie):
    # Charger le fichier XML
    tree = ET.parse(fichier_entree)
    root = tree.find('ALL_INSTANCES')

    # Extraire toutes les instances
    instances = root.findall('instance')

    # Étape 1 : Ajuster les plages de temps
    ajuster_temps(instances)

    # Étape 2 : Fusionner les instances qui se chevauchent et ont le même "code"
    instances_fusionnees = fusionner_instances(instances)

    # Remplacer l'ancien contenu par les instances fusionnées
    root.clear()  # On efface toutes les anciennes instances
    for instance in instances_fusionnees:
        root.append(instance)

    # Sauvegarder le fichier XML modifié
    tree.write(fichier_sortie)

# Fonction pour traiter tous les fichiers XML dans le dossier d'entrée
def traiter_tous_les_fichiers(dossier_entree, dossier_sortie):
    # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    # Parcourir tous les fichiers dans le dossier d'entrée
    for fichier in os.listdir(dossier_entree):
        if fichier.endswith(".xml"):
            fichier_entree = os.path.join(dossier_entree, fichier)
            fichier_sortie = os.path.join(dossier_sortie, fichier)

            print(f"Traitement du fichier : {fichier_entree}")
            traiter_fichier_xml(fichier_entree, fichier_sortie)
            print(f"Fichier transformé enregistré dans : {fichier_sortie}")

# Exécuter le programme
traiter_tous_les_fichiers(dossier_entree, dossier_sortie)
