  
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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------

def newCatalog():
    catalogo = {'peliculas': None, 'productoras': None, "actores": None}  
    catalogo['peliculas'] = mp.newMap(numelements=349100,maptype='CHAINING', loadfactor=2, comparefunction=compareMovieId)
    catalogo['productoras'] = mp.newMap(numelements=36000,maptype='CHAINING', loadfactor=2, comparefunction=compareProductionCompanybyName)
    catalogo['actores'] = mp.newMap(numelements=261000,maptype='CHAINING', loadfactor=2, comparefunction=compareActorbyName)
    return catalogo

def newProductionCompany(nombre):
    company = {'name': '', 'movies': None, 'average_rating': 0.0}
    company['name'] = nombre
    company['movies'] = lt.newList('SINGLE_LINKED', compareProductionCompanybyName)
    return company

def newActor(nombre):
    actor = {"name": "", "movies": None, 'average_rating': 0.0, 'directores': None}
    actor["name"] = nombre
    actor["movies"] = lt.newList('SINGLE_LINKED', compareMovieId)
    actor['directores'] = mp.newMap(numelements=1000,maptype='CHAINING', loadfactor=2, comparefunction=compareDirectorByname)
    return actor

# Funciones para agregar informacion al catalogo

def addMovie(catalogo, pelicula):
    mp.put(catalogo["peliculas"], pelicula["id"], pelicula)

def addCompanyMovie(catalogo, companyname, movie):
    companies = catalogo['productoras']
    esta = mp.contains(companies, companyname)
    if esta:
        entry = mp.get(companies, companyname)
        comp = me.getValue(entry)
    else:
        comp = newProductionCompany(companyname)
        mp.put(companies, companyname, comp)
    lt.addLast(comp['movies'], movie)
    rat_comp = comp['average_rating']
    num_mov = lt.size(comp['movies'])
    rat_peli = movie['vote_average']
    new_ave = round(((num_mov-1)*rat_comp+float(rat_peli))/(num_mov), 2)
    comp['average_rating'] = new_ave

def addActor(catalogo, actor, movie, casting):
    actores = catalogo["actores"]
    esta = mp.contains(actores, actor)
    if esta:
        entry = mp.get(actores, actor)
        act = me.getValue(entry)
    else:
        act = newActor(actor)
        mp.put(actores, actor, act)
    lt.addLast(act["movies"],movie)
    prom_act = act['average_rating']
    num_mov = lt.size(act['movies'])
    rat_peli = movie['vote_average']
    new_prom = round(((num_mov-1)*prom_act+float(rat_peli))/(num_mov), 2)
    act['average_rating'] = new_prom
    director = casting["director_name"]
    if mp.contains(act['directores'], director):
        direct = mp.get(act["directores"], director)
        valor = me.getValue(direct)
        valor+=1
        mp.put(act["directores"], director, valor)
    else:
        valor = 0
        mp.put(act["directores"], director, valor)
        direct = mp.get(act["directores"], director)
        valor = me.getValue(direct)
        valor+=1
        mp.put(act["directores"], director, valor)
    return catalogo


# ==============================
# Funciones de consulta
# ==============================

def moviesSize(catalogo):
    return lt.size(catalogo["peliculas"])

def companiesSize(catalogo):
    return mp.size(catalogo['productoras'])

def getMoviesbyCompany(catalogo, company_name):
    comp = mp.get(catalogo["productoras"], company_name)
    if comp is not None:
        return me.getValue(comp)
    return None

def getActor_information(catalogo, actor_name):
    actor_entry = mp.get(catalogo["actores"], actor_name)
    if actor_entry is not None:
        return me.getValue(actor_entry)
    return None

# ==============================
# Funciones de Comparacion
# ==============================    

    

def compareMovieId(id_1, id_2):
    entryname = me.getKey(id_2)
    if id_1 == entryname:
        return 0
    elif id_1 > entryname:
        return 1
    else:
        return -1
def compareProductionCompanybyName(name, company):
    entryname = me.getKey(company)
    if name == entryname:
        return 0
    elif name > entryname:
        return 1
    else:
        return -1

def compareDirectorByname(name, director):
    entryname = me.getKey(director)
    if name == entryname:
        return 0
    elif name > entryname:
        return 1
    else:
        return -1

def compareActorbyName(name, actor):
    entryname = me.getKey(actor)
    if name == entryname:
        return 0
    elif name > entryname:
        return 1
    else:
        return -1