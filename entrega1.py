from itertools import count

from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    greedy,
    astar,
    iterative_limited_depth_first)

from simpleai.search.viewers import WebViewer, BaseViewer

INITIAL_STATE=()

CIUDADES_ADYACENTES = {
    'sauce_viejo': [('santo_tome', 15)],
    'santo_tome': [('sauce_viejo',15),('santa_fe', 5), ('angelica', 85)],
    'santa_fe': [('santo_tome',5), ('recreo',10)],
    'recreo': [('santa_fe',10),('esperanza',20)],
    'esperanza': [('recreo',20),('rafaela',70)],
    'rafaela':[('lehmann',8),('susana',10),('esperanza',70)],
    'lehmann': [('rafaela',8),('sunchales',32)],
    'sunchales': [('lehmann',8)],
    'susana': [('rafaela',10),('angelica',25)],
    'angelica':[('susana',25),('sc_de_saguier',60),('santo_tome',85),('san_vicente',18)],
    'sc_de_saguier': [('angelica'),60],
    'san_vicente':[('angelica',18)],
}

PUNTOSDECARGA= {'rafaela', 'santa_fe'}

listado_global_paquetes = []

class MercadoArtificial(SearchProblem):

    def is_goal(self, state):
        camiones, paquetes = state
        id_camion, origen_camion, capacidad = camiones
        camiones=list(camiones)
        id_paquete, origen_paquete, destino_paquete = paquetes
        paquetes=list(paquetes)
        #si los camiones se encuentran en las ciudades de puntosdecarga quiere decir que llegaron al destino final
        return (set(camiones[1]) in PUNTOSDECARGA) and len(paquetes)==0

    def cost(self, state1, action, state2):
        camiones1, paquetes1 = state1
        camiones2, paquetes2 = state2
        consumo_combustible_origen=0
        consumo_combustible_destino=0
        for x,camion in enumerate(camiones2):
            if camion[x]==action[0]:
                consumo_combustible_destino=camion[2]
                for y, camion_origen in enumerate(camiones1):
                    if y==x:
                        consumo_combustible_origen=camion_origen[2]
        return (consumo_combustible_destino - consumo_combustible_origen)

    def actions(self, state):
        camiones, paquetes = state
        id_camion, origen_camion, capacidad = camiones
        id_paquete, origen_paquete, destino_paquete = paquetes

        acciones = []

        for camion in camiones:
            id_camion_actual, origen_camion_actual, capacidad_camion_actual = camion
            for ciudad in CIUDADES_ADYACENTES[origen_camion]:
                consumo_a_ciudad = (ciudad[1] / 100)
                if capacidad_camion_actual >= consumo_a_ciudad:
                    acciones.append(((id_camion_actual,ciudad[1],consumo_a_ciudad),(paquetes)))

        return acciones

    def result(self, state, action):
        camiones, paquetes = state
        camiones_accion, paquetes_accion = action
        id_camion, ciudad_a_mover, consumo_a_ciudad = camiones_accion

        lista_paquetes = list(paquetes)
        lista_camiones = list(camiones)
        nueva_ciudad = ciudad_a_mover
        #solo va a cambiar esta ciudad, en el camion de id_camion
        lista_global = list(listado_global_paquetes)
        #los paquetes que tienen como destino la ciudad a la que me movi
        #agregar los paquetes que tienen como origen la ciudad a la que me moví
        for paquete in paquetes:
            id_paquete, origen_paquete, destino_paquete = paquete
            if (destino_paquete == nueva_ciudad):
                lista_global.remove(paquete)
                lista_paquetes.remove(paquete)
            if (origen_paquete == nueva_ciudad):
                lista_global.append((id_camion,paquete))

        for camion in camiones:
            if camion[0] == id_camion:
                camion[1] = nueva_ciudad
                camion[2] -= consumo_a_ciudad

        camiones_nuevo = tuple(camiones)
        paquetes_nuevo = tuple(lista_paquetes)
        return (camiones_nuevo,paquetes_nuevo)

    def heuristic(self, state):
        camiones, paquetes=state
        paquetes=list(paquetes)
        cant_paquetes=count(paquetes[0])
        # me faltan tantas acciones como paquetes me falten entregar para llegar a la cantidad total de paquetes en el camion
        return cant_paquetes - len(state)


def planear_camiones(metodo, camiones, paquetes):
    #Habria que ver si se le pasa tal cual vienen los paquetes y camiones o habria que agregarlos a una lista
    INITIAL_STATE=(camiones, paquetes)

    problem = MercadoArtificial(INITIAL_STATE)

    METODOS = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'iterative_limited_depth_first': iterative_limited_depth_first,
        'uniform_cost': uniform_cost,
        'astar': astar,
    }

    result = METODOS[metodo](problem)
    itinerario=[]

    for action, state in result.path():
        camiones, paquetes = state
        camiones_accion, paquetes_accion = action
        id_camion, ciudad_a_mover, consumo_a_ciudad = camiones_accion

        lista_paquetes = list(paquetes)
        lista_camiones = list(camiones)
        nueva_ciudad = ciudad_a_mover
        # solo va a cambiar esta ciudad, en el camion de id_camion
        lista_global = list(listado_global_paquetes)
        # los paquetes que tienen como destino la ciudad a la que me movi
        # agregar los paquetes que tienen como origen la ciudad a la que me moví
        for paquete in paquetes:
            id_paquete, origen_paquete, destino_paquete = paquete
            if (destino_paquete == nueva_ciudad):
                lista_global.remove(paquete)
                lista_paquetes.remove(paquete)
            if (origen_paquete == nueva_ciudad):
                lista_global.append((id_camion, paquete))

        for camion in camiones:
            if camion[0] == id_camion:
                camion[1] = nueva_ciudad
                camion[2] -= consumo_a_ciudad

        camiones_nuevo = tuple(camiones)
        paquetes_nuevo = tuple(lista_paquetes)
        itinerario=(camiones_nuevo, paquetes_nuevo)
    return itinerario




if __name__ == '__main__':
    #problema = MercadoArtificial(INITIAL_STATE)
    camiones = [
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
        ('c2', 'rafaela', 2),
        ('c3', 'santa_fe', 2),
    ]

    paquetes = [
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'angelica'),
        ('p2', 'rafaela', 'santa_fe'),
        ('p3', 'esperanza', 'susana'),
        ('p4', 'recreo', 'san_vicente'),
    ]

    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        breadth_first, camiones, paquetes
    )

    print(itinerario)