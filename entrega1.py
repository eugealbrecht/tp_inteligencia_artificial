from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    astar,
    iterative_limited_depth_first
)
from simpleai.search.viewers import WebViewer, BaseViewer
from simpleai.search.traditional import astar

INITIAL_STATE = ((('sunchales',1.5,()), ('sunchales',2,()), ('rafaela',2, ())), ('p1', 'p2', 'p3', 'p4'))


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

CIUDADES_CARGA = {'rafaela', 'santa_fe'}

METODOS = {
    'breadth_first': breadth_first,
    'depth_first': depth_first,
    'iterative_limited_depth_first': iterative_limited_depth_first,
    'uniform_cost': uniform_cost,
    'astar': astar,
}

listado_global_paquetes = []

class MercadoArtificial(SearchProblem):

    def is_goal(self, state):
        camiones, paquetes = state
        #set_ciudades = set(camiones[1])
        camiones = list(camiones)
        paquetes = list(paquetes)
        # si los camiones se encuentran en las ciudades de puntosdecarga quiere decir que llegaron al destino final


        for camion in camiones:
            if camion[1] not in CIUDADES_CARGA:
                return False
            else:
                return True
        if len(paquetes) > 0:
            return False
        else:
            return True


    def cost(self, state1, action, state2):
        id_camion, ciudad_a_mover, consumo_a_ciudad = action
        return consumo_a_ciudad
        #camiones1, paquetes1 = state1
        #camiones2, paquetes2 = state2
        #consumo_combustible_origen=0
        #consumo_combustible_destino=0
        #for x,camion_destino in enumerate(camiones2):
        #   if camion_destino[x]==action[0]:
        #      consumo_combustible_destino=camion_destino[2]
        #     for y, camion_origen in enumerate(camiones1):
        #        if y==x:
        #           consumo_combustible_origen=camion_origen[2]
        #return (consumo_combustible_destino - consumo_combustible_origen)


    def actions(self, state):
        camiones, paquetes = state
        id_camion, origen_camion, capacidad_camion, paquetes_camion = camiones
        #id_paquete, origen_paquete, destino_paquete = paquetes

        acciones = []

        for camion in camiones: #por cada camion en el estado
            id_camion_actual, origen_camion_actual, capacidad_camion_actual, paquetes_camion_actual = camion
                #recorro sus ciudades adyacentes, a las que se puede mover
            for ciudad in CIUDADES_ADYACENTES[origen_camion_actual]:
                    #a partir de los km, calculamos el consumo
                ciudad_adyacente, distancia = ciudad
                consumo_a_ciudad = (distancia / 100) #distancia/100
                    #si le alcanza, generamos la acción
                if capacidad_camion_actual >= consumo_a_ciudad:
                    acciones.append((id_camion_actual,ciudad_adyacente,consumo_a_ciudad))

        return acciones

    def result(self, state, action):
        #lo que viene en state
        camiones, paquetes = state

        #lo que viene en actions
        id_camion, ciudad_a_mover, consumo_a_ciudad = action

        #genero listas para hacer operaciones con los camiones y paq. del estado
        paquetes = list(paquetes)
        camiones = list(camiones)

        #buscar en el estado, el camion que llega en actions
        for camion in camiones:
            if (camion[0] == id_camion):
                camion_actual = camion
        id_camion_estado, origen_camion_estado, capacidad_camion_estado, paquetes_camion_estado = camion_actual
        paquetes_camion_estado = list(paquetes_camion_estado)

        #identifico en el estado, paquetes que tengan como origen
        #la ciudad a la que me estoy moviendo.
        # Los agrego a los paquetes del camión. Y lo saco del estado.
        for paquete in paquetes:
            id_paquete, origen_paquete, destino_paquete = paquete
            if (origen_paquete == ciudad_a_mover):
                paquetes_camion_estado.append(paquete)
                paquetes.remove(paquete)

        #recorrer los paquetes del camion y ver si tiene como destino
        #la ciudad a la que me moví. Sacarlo.
        for paquete_en_camion in paquetes_camion_estado:
            id_paquete_en_camion, origen_paquete_en_camion, destino_paquete_en_camion = paquete_en_camion
            if (destino_paquete_en_camion == ciudad_a_mover):
                paquetes_camion_estado.remove(paquete_en_camion)

        #ciudad_a_mover --nueva
        #nafta_necesaria

        #resto lo que me costó llegar
        capacidad_camion_estado -= consumo_a_ciudad

        #cargar si se encuentra en sta fe o rafaela
        if ciudad_a_mover == 'santa_fe' or ciudad_a_mover == 'rafaela':
            capacidad_total_camion = CAMIONES_INICIAL[ciudad_a_mover][2]
            capacidad_camion_estado = capacidad_total_camion

        #actualizar camion en estado.

        #ver de convertir antes a tupla
        camion_actual = tuple((id_camion_estado,ciudad_a_mover,capacidad_camion_estado,paquetes_camion_estado))

        return (tuple(camiones), tuple(paquetes))

    def heuristic(self, state):
        camiones, paquetes=state
        paquetes=list(paquetes)
        cant_paquetes=len(paquetes)
        # me faltan tantas acciones como paquetes me falten entregar para llegar a la cantidad total de paquetes en el camion
        return cant_paquetes - len(state)


def planear_camiones(metodo, camiones, paquetes):
    #se crea global de camiones para poder acceder a la capacidad
    #inicial de cada uno desde result
    global CAMIONES_INICIAL
    CAMIONES_INICIAL = list(camiones)

    lista_camiones = []
    for camion in camiones:
        lista_camiones.append(((camion[0],camion[1], camion[2],()))) #origen, capacidad, paquetes

    lista_paquetes = []
    for paquete in paquetes:
        lista_paquetes.append(paquete) #le paso todos los valores, ver.

    estado_inicial = (tuple(lista_camiones), tuple(lista_paquetes))

    problema = MercadoArtificial(estado_inicial)
    result = METODOS[metodo](problema)

    itinerario = []

    for action, state in result.path(): #por cada accion y estado del camino
        if action != None:
            camiones_estado, paquetes_estado = state
            camiones_accion, paquetes_accion = action

            camion = camiones_accion

            #destino del camion
            for camion_estado in camiones_estado:
                if camion_estado[0] == camion:
                    camion_actual = camion_estado[0]
                    ciudad_destino = camion_estado[1]

            consumo_a_ciudad = action[2]

            paquetes_camion = camion_actual[2]

            itinerario.append((camion,ciudad_destino,consumo_a_ciudad,paquetes_camion))

    return itinerario