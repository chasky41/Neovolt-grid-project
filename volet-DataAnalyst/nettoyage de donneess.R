#---------------------------Lire les données----------------------------
library(readxl) #library pour la lecture des fichiers
library(dplyr)
library(tidyr)


#------------------------------------ fihcier actif_si------------------------------------------------

#Importation de nos données:
actifs_si <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/actifs_si.csv",
                      sep = ",",
                      header = TRUE)
View(actifs_si)
#s'il y'a des lignes vides ou non
colSums(is.na(actifs_si))
#chercher les lignes dupliquées
sum(duplicated(actifs_si))
dim(actifs_si) #Le nombre de lignes et colonnes

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(actifs_si,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/actifs_si.csv")

#------------------------------------ fihcier cas_fraude_confirmes------------------------------------------------
#Importation de nos données:
cas_fraude_confirmes <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/cas_fraude_confirmes.csv",
                      sep = ",",
                      header = TRUE)
View(cas_fraude_confirmes)
dim(cas_fraude_confirmes) #Le nombre de lignes et colonnes

#s'il y'a des lignes vides ou non
colSums(is.na(cas_fraude_confirmes))
#chercher les lignes dupliquées
sum(duplicated(cas_fraude_confirmes))
#savoir le type de chaque colonne
str(cas_fraude_confirmes)

#changer le type de la colonne date_detection en format date
cas_fraude_confirmes$date_detection <- as.Date(cas_fraude_confirmes$date_detection)
str(cas_fraude_confirmes) #Vérification
class(cas_fraude_confirmes$date_detection)

# Enregistrer le fichier cas_fraude_confirmes dans ce chemin en Format csv
write.csv(cas_fraude_confirmes,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/cas_fraude_confirmes.csv")

#------------------------------------ fihcier clients------------------------------------------------
#Importation de nos données:
clients <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/clients.csv",
                                 sep = ",",
                                 header = TRUE)
View(clients)
dim(clients) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(clients))
clients <- na.omit(clients) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(clients))

dim(clients) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(clients)

#changer le type de la colonne date_entree en format date
clients$date_entree <- as.Date(clients$date_entree)
#changer le type de la colonne surface_m2 en float (numeric)
clients$surface_m2 <- as.numeric(clients$surface_m2)
str(clients) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(clients,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/clients.csv")

#------------------------------------ fihcier compteurs------------------------------------------------
#Importation de nos données:
compteurs <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/compteurs.csv",
                    sep = ",",
                    header = TRUE)
View(compteurs)
dim(compteurs) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(compteurs))
compteurs <- na.omit(compteurs) #supprimer les NA

#chercher les lignes dupliquées
sum(duplicated(compteurs))

dim(compteurs) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(compteurs)

#changer le type de la colonne date_pose en format date
compteurs$date_pose <- as.Date(compteurs$date_pose)
str(compteurs) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(compteurs,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/compteurs.csv")

#------------------------------------ fihcier incidents_reseau------------------------------------------------
#Importation de nos données:
incidents_reseau <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/incidents_reseau.csv",
                      sep = ",",
                      header = TRUE)
View(incidents_reseau)
dim(incidents_reseau) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(incidents_reseau))
incidents_reseau <- na.omit(incidents_reseau) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(incidents_reseau))

dim(incidents_reseau) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(incidents_reseau)

#changer le type de la colonne date_debut en format date
incidents_reseau$date_debut <- as.POSIXct(incidents_reseau$date_debut, format = "%Y-%m-%d %H:%M")
class(incidents_reseau$date_debut)
str(incidents_reseau$date_debut)
format(incidents_reseau$date_debut, "%Y-%m-%d %H:%M")
str(incidents_reseau) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(incidents_reseau,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/incidents_reseau.csv")

#------------------------------------ fihcier journaux_securite------------------------------------------------
#Importation de nos données:
journaux_securite <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/journaux_securite.csv",
                      sep = ",",
                      header = TRUE)
View(journaux_securite)
dim(journaux_securite) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(journaux_securite))
journaux_securite <- na.omit(journaux_securite) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(journaux_securite))

dim(journaux_securite) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(journaux_securite)

#changer le type de la colonne date_pose en format date
journaux_securite$horodatage <- as.POSIXct(journaux_securite$horodatage, format = "%Y-%m-%d %H:%M:%S")

class(journaux_securite$horodatage)
str(journaux_securite$horodatage)
format(journaux_securite$horodatage, "%Y-%m-%d %H:%M:%S")
str(journaux_securite) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(journaux_securite,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/journaux_securite.csv")

#------------------------------------ fihcier meteo------------------------------------------------
#Importation de nos données:
meteo <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/meteo.csv",
                      sep = ",",
                      header = TRUE)
View(meteo)
dim(meteo) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(meteo))
meteo <- na.omit(meteo) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(meteo))

dim(meteo) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(meteo)

#changer le type de la colonne date en format date
meteo$date <- as.Date(meteo$date)
str(meteo) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(meteo,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/meteo.csv")

#------------------------------------ fihcier releves_consommation------------------------------------------------

#Importation de nos données:
releves_consommation <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/releves_consommation.csv",
                  sep = ",",
                  header = TRUE)
View(releves_consommation)
dim(releves_consommation) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(releves_consommation))
releves_consommation <- na.omit(releves_consommation) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(releves_consommation))

# Supprimer les doublons
releves_consommation <- distinct(releves_consommation)

dim(releves_consommation) #Le nombre de lignes et colonnes apres le nettoyage

#savoir le type de chaque colonne
str(releves_consommation)

#changer le type de la colonne date en format date
releves_consommation$date <- as.Date(releves_consommation$date)
str(releves_consommation) #Vérification

# Enregistrer le fichier actifs_si dans ce chemin en Format csv
write.csv(releves_consommation,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/releves_consommation.csv")


#------------------------------------ fihcier reclamations------------------------------------------------


#Importation de nos données:
reclamations <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/reclamations.csv",
                                 sep = ",",
                                 header = TRUE)
View(reclamations)
dim(reclamations) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(reclamations))
reclamations <- na.omit(reclamations) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(reclamations))

#changer le type de la colonne date en format date
reclamations$date <- as.Date(reclamations$date)
str(reclamations) #Vérification

#Importation de nos données:
write.csv(reclamations,file = "C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees nettoyees/reclamations.csv")

#------------------------------------ fihcier releves_horaires_echantillon------------------------------------------------

#Importation de nos données:
releves_horaires_echantillon <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/releves_horaires_echantillon.csv",
                         sep = ",",
                         header = TRUE)

View(releves_horaires_echantillon)
dim(releves_horaires_echantillon) #Le nombre de lignes et colonnes avant le nettoyage 
#s'il y'a des lignes vides ou non
colSums(is.na(releves_horaires_echantillon))
releves_horaires_echantillon <- na.omit(releves_horaires_echantillon) #supprimer les NA
#chercher les lignes dupliquées
sum(duplicated(releves_horaires_echantillon))

dim(releves_horaires_echantillon) #Le nombre de lignes et colonnes apres le nettoyage

#changer le type de la colonne date en format date
releves_horaires_echantillon$date <- as.Date(releves_horaires_echantillon$date)
str(releves_horaires_echantillon) #Vérification


#changer le type de la colonne horodatage en format date
releves_horaires_echantillon$horodatage <- as.POSIXct(releves_horaires_echantillon$horodatage, format = "%Y-%m-%d %H:%M:%S")

class(releves_horaires_echantillon$horodatage)
str(releves_horaires_echantillon$horodatage)
format(releves_horaires_echantillon$horodatage, "%Y-%m-%d %H:%M:%S")
str(releves_horaires_echantillon) #Vérification



#Importation de nos données:
releves_horaires_echantillon <- read.csv("C:/Users/Lenovo/Desktop/school/ESIC/examen final/donnees/donnees/releves_horaires_echantillon.csv",
                         sep = ",",
                         header = TRUE)
