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

CIUDADES_ADYACENTES = {
    'sauce_viejo': [('santo_tome', 15)],
    'santo_tome': [('sauce_viejo', 15), ('santa_fe', 5), ('angelica', 85)],
    'santa_fe': [('santo_tome', 5), ('recreo', 10)],
    'recreo': [('santa_fe', 10), ('esperanza', 20)],
    'esperanza': [('recreo', 20), ('rafaela', 70)],
    'rafaela': [('lehmann', 8), ('susana', 10), ('esperanza', 70)],
    'lehmann': [('rafaela', 8), ('sunchales', 32)],
    'sunchales': [('lehmann', 8)],
    'susana': [('rafaela', 10), ('angelica', 25)],
    'angelica': [('susana', 25), ('sc_de_saguier', 60), ('santo_tome', 85), ('san_vicente', 18)],
    'sc_de_saguier': [('angelica', 60)],
    'san_vicente': [('angelica', 18)],
}

CIUDADES_CARGA = ['rafaela', 'santa_fe']

METODOS = {
    'breadth_first': breadth_first,
    'depth_first': depth_first,
    'iterative_limited_depth_first': iterative_limited_depth_first,
    'uniform_cost': uniform_cost,
    'astar': astar,
}

class MercadoArtificial(SearchProblem):

    def is_goal(self, state):
        camiones, paquetes = state
        lista = []
        if len(paquetes) != 0:
            return False

        for cam in camiones:
            if cam[1] not in CIUDADES_CARGA:
                return False
            if (len(cam[3]) > 0):
                paquetes_camion = cam[3]
                for paq in paquetes_camion:
                    if paq[2] != cam[1]:
                        return False

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
        #id_camion, origen_camion, capacidad_camion, paquetes_camion = camiones
        #id_paquete, origen_paquete, destino_paquete = paquetes

        acciones = []

        for camion in camiones: #por cada camion en el estado
            id_camion_actual = camion[0]
            origen_camion_actual = camion[1]
            capacidad_camion_actual = camion[2]
            paquetes_camion_actual = camion[3]
                #recorro sus ciudades adyacentes, a las que se puede mover
            for ciudad_ir in CIUDADES_ADYACENTES[origen_camion_actual]:
                    #a partir de los km, calculamos el consumo
                ciudad_adyacente = ciudad_ir[0]
                distancia = ciudad_ir[1]
                consumo_a_ciudad = round(((distancia) / 100),2) #distancia/100
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
            if (origen_paquete == origen_camion_estado):
                paquetes_camion_estado.append(paquete)

        for paq in paquetes_camion_estado:
            for paq2 in paquetes:
                if paq == paq2:
                    paquetes.remove(paq)

        #recorrer los paquetes del camion y ver si tiene como destino
        #la ciudad a la que me moví. Sacarlo.
        if len(paquetes_camion_estado) != 0:
            item_list = []
            for paquete_en_camion in paquetes_camion_estado:
                id_paquete_en_camion, origen_paquete_en_camion, destino_paquete_en_camion = paquete_en_camion
                if (destino_paquete_en_camion == origen_camion_estado):
                    #paquetes_camion_estado.remove(paquete_en_camion)
                    item_list.append(paquete_en_camion)
            if len(item_list) != 0:
                paquetes_camion_estado = [e for e in paquetes_camion_estado if e not in item_list]

        #ciudad_a_mover --nueva
        #nafta_necesaria
        nueva_ciudad = ciudad_a_mover
        consumo = consumo_a_ciudad
        #resto lo que me costó llegar

        #cargar si se encuentra en sta fe o rafaela
        if nueva_ciudad == 'santa_fe' or nueva_ciudad == 'rafaela':
            for indice2, camion_inicial in enumerate(CAMIONES_INICIAL):
                if camion_inicial[0] == nueva_ciudad:
                    indice_a_utilizar = indice2
                    capacidad_total_camion = CAMIONES_INICIAL[indice_a_utilizar][2]
                    capacidad_camion_estado = capacidad_total_camion
        else:
            capacidad_camion_estado -= consumo_a_ciudad

        #actualizar camion en estado.

        #ver de convertir antes a tupla
        camion_actual = (id_camion_estado,nueva_ciudad,capacidad_camion_estado,tuple(paquetes_camion_estado))

        for indice, camion_1 in enumerate(camiones):
            if camion_1[0] == id_camion_estado:
                indice_utilizar = indice
        camiones[indice_utilizar] = camion_actual

        nuevo_estado = (tuple(camiones),tuple(paquetes))

        return nuevo_estado

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
        lista_camiones.append((camion[0],camion[1], camion[2],())) #id, origen, capacidad, paquetes

    lista_paquetes = []
    for paquete in paquetes:
        lista_paquetes.append((paquete[0], paquete[1], paquete[2])) #le paso todos los valores, ver.
                            #id, origen, destino

    lista_camiones = tuple(lista_camiones)
    lista_paquetes = tuple(lista_paquetes)
    INITIAL_STATE = (lista_camiones, lista_paquetes)

    problema = MercadoArtificial(INITIAL_STATE)
    result = METODOS[metodo](problema)

    itinerario = []

    for action, state in result.path(): #por cada accion y estado del camino
        if action != None:
            camiones_estado, paquetes_estado = state
            id_camion, ciudad_camion, consumo_a_ciudad = action

            #destino del camion
            for indice_camion, camion_estado in enumerate(camiones_estado):
                if camion_estado[0] == id_camion:
                    indice = indice_camion
            ciudad = camiones_estado[indice][1]
            nafta = action[2]
            paquetes_camion = camiones_estado[indice][3]
            lista_paquetes = []
            for paq in paquetes_camion:
                lista_paquetes.append(paq[0])

            itinerario.append((id_camion,ciudad,nafta,tuple(lista_paquetes)))
        else:
            pass

    return itinerario
"""
itinerario = planear_camiones(
  # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
  metodo="astar",
  camiones=[
    # id, ciudad de origen, y capacidad de combustible máxima (litros)
    ('c1', 'rafaela', 1.5),
    ('c2', 'rafaela', 2),
    ('c3', 'santa_fe', 2),
  ],
  paquetes=[
    # id, ciudad de origen, y ciudad de destino
    ('p1', 'rafaela', 'angelica'),
    ('p2', 'rafaela', 'santa_fe'),
    ('p3', 'esperanza', 'susana'),
    ('p4', 'recreo', 'san_vicente'),
  ],
)

"""



if __name__ == '__main__':
    """camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
        ('c2', 'rafaela', 2),
        ('c3', 'santa_fe', 2),
    ]
    paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'angelica'),
        ('p2', 'rafaela', 'santa_fe'),
        ('p3', 'esperanza', 'susana'),
        ('p4', 'recreo', 'san_vicente'),
    ]
    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        "breadth_first",camiones,paquetes
    )"""