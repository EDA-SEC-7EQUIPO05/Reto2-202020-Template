  
"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
import csv
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta. Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def initCatalog():
    catalogo=model.newCatalog()
    return catalogo


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadMovies (catalogo,movies_details,movies_casting):
    loadDetails(catalogo,movies_details,sep=";")
    loadCasting (catalogo,movies_casting,sep=";")
    
def loadDetails (catalogo,movies_details,sep=";"):
    dialect= csv.excel()
    dialect.delimiter=sep
    with open(movies_details, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile,dialect=dialect)
        for row in spamreader:
            model.addMovie(catalogo,row)
            model.addCompanyMovie(catalogo,row["production_companies"].lower(),row)
    return catalogo

def loadCasting (catalogo,movies_casting,sep=";"):
    peliculas = catalogo["peliculas"]
    dialect= csv.excel()
    dialect.delimiter=sep
    with open(movies_casting, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile,dialect=dialect)
        for row in spamreader:
            for i in range(1,6):
                model.addActor(catalogo,row["actor"+str(i)+"_name"].lower(), me.getValue(mp.get(peliculas,row["id"])),row)
    return catalogo

def getMoviesbyCompany (catalogo,company_name):
    productorainfo=model.getMoviesbyCompany(catalogo,company_name)
    return productorainfo

def getActor_information(catalogo, actor_name):
    actor = model.getActor_information(catalogo, actor_name)
    return actor 

    
def moviesSize2 (catalogo,moviesfile2):
    return model.moviesSize(catalogo)