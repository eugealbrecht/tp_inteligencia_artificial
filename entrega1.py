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
    'sunchales': [('lehmann', 32)],
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

        for camion in camiones:
            id_camion, ciudad_camion, capacidad, paquetes_camion = camion

            for paquete in paquetes_camion: #Si hay paquetes en el camión los cuales la ciudad actual NO es su destino, no se llegó al estado final.
                id_paquete, origen_paquete, destino_paquete = paquete
                if destino_paquete is not ciudad_camion:
                    return False

            if ciudad_camion not in CIUDADES_CARGA: #Si el camión NO está en rafaela o santa fe, no se llegó al estado final.
                return False

        # Si hay paquetes en el estado, que no están asociados a ningún camión, no se llegó al estado final (pendientes entregar)
        if len(paquetes) > 0:
            return False

        return True

    def cost(self, state1, action, state2):
        id_camion, ciudad_a_mover, consumo_a_ciudad = action
        return consumo_a_ciudad

    def actions(self, state):
        camiones, paquetes = state
        acciones = []

        for camion in camiones: #por cada camion en el estado
            id_camion_actual, origen_camion_actual, capacidad_camion_actual, paquetes_camion_actual = camion
            #recorremos las ciudades adyacentes a las que se encuentra.
            for ciudad in CIUDADES_ADYACENTES[origen_camion_actual]:
                ciudad_adyacente, distancia = ciudad
                #a partir de los km de distancia, calculamos el consumo en nafta - 1l / 100km
                consumo_a_ciudad = (distancia / 100)
                if capacidad_camion_actual >= consumo_a_ciudad: #si el camión tiene combustible suficiente, generamos la acción
                    acciones.append((id_camion_actual,ciudad_adyacente,consumo_a_ciudad))

        return acciones

    def result(self, state, action):
        camiones, paquetes = state
        id_camion, ciudad_a_mover, consumo_a_ciudad = action

        #generamos las listas de camiones y paquetes para poder modificarlas
        paquetes = list(paquetes)
        camiones = list(camiones)

        #identificamos en camiones, el que llega en actions
        for camion in camiones:
            if (camion[0] == id_camion):
                camion_actual = camion
        id_camion_estado, origen_camion_estado, capacidad_camion_estado, paquetes_camion_estado = camion_actual

        #generamos lista de paquetes del camión para poder modificarla
        paquetes_camion_estado = list(paquetes_camion_estado)

        #por cada paquete en el camión, chequeamos si tiene como destino la ciudad en la que se encuentra el camión.
        #Si es así, se agregan a una lista para desp eliminarlos.
        paquetes_a_eliminar = []
        for paquete_en_camion in paquetes_camion_estado:
            id_paquete_en_camion, origen_paquete_en_camion, destino_paquete_en_camion = paquete_en_camion
            if (destino_paquete_en_camion == origen_camion_estado):
                paquetes_a_eliminar.append(paquete_en_camion)

        if len(paquetes_a_eliminar) != 0: #si hay elementos a eliminar
            nueva_lista = []
            for paquete_que_sigue in paquetes_camion_estado:
                if paquete_que_sigue not in paquetes_a_eliminar:
                    nueva_lista.append(paquete_que_sigue) #agrego en una nueva lista todos los paquetes, menos los que se tienen que eliminar
            paquetes_camion_estado = nueva_lista #ahora los paquetes del camión, son la nueva lista que generamos.

        #Por cada paquete, chequeamos si tiene como origen la ciudad en la que se encuentra el camión.
        #Si es así, lo agregamos a los paquetes del camión y lo sacamos de la lista de paquetes.
        for paquete in paquetes:
            id_paquete, origen_paquete, destino_paquete = paquete
            if (origen_paquete == origen_camion_estado):
                paquetes_camion_estado.append(paquete) #Se agrega a los paquetes del estado

        for paquete_en_camion in paquetes_camion_estado:
            for paquete_general in paquetes:
                if paquete_en_camion == paquete_general:
                    paquetes.remove(paquete_en_camion) #Se elimina de la lista de paquetes pendiente de carga

        nueva_ciudad = ciudad_a_mover               # ciudad a la que el camión se va a mover (viene en actions)
        capacidad_camion_estado -= consumo_a_ciudad # restamos el consumo de nafta a esa ciudad (viene en actions)

        #Si la ciudad a la que el camión se va a mover, es santa fe o rafaela, se llena el tanque de nafta.
        if ciudad_a_mover in CIUDADES_CARGA:
            for camion_inicial in CAMIONES_INICIAL: #buscamos en la variable global, el tamaño del tanque.
                if camion_inicial[0] == id_camion:
                    tope_nafta = camion_inicial[2]
            capacidad_camion_estado = tope_nafta

        # armamos el nuevo camión
        camion_actual = (id_camion_estado,ciudad_a_mover,capacidad_camion_estado,tuple(paquetes_camion_estado))

        #actualizamos con el nuevo camión en el estado
        for indice, camion_1 in enumerate(camiones):
            if camion_1[0] == id_camion_estado:
                indice_utilizar = indice
        camiones[indice_utilizar] = camion_actual

        #armamos el nuevo estado
        nuevo_estado = (tuple(camiones),tuple(paquetes))

        return nuevo_estado

    def heuristic(self, state):
        camiones, paquetes=state
        consumo_a_ciudad = 0
        lista=[]
        consumo=0
        #calculo el combustible que me falta para llegar a destino
        for camion in camiones:
            id_camion, ciudad_camion, combustible, paquetes_del_camion = camion
            for ciudad in CIUDADES_ADYACENTES[ciudad_camion]:
                if ciudad in CIUDADES_CARGA: #si dentro de las ciudades adyacentes esta dentro de las de carga, se calcula el consumo hasta esa ciudad
                    ciudad_adyacente, distancia=ciudad
                    consumo_a_ciudad = (distancia/100)
                if ciudad not in CIUDADES_CARGA: #si la ciudad no esta dentro de las ciudades de carga, se calcula el menor costo
                    ciudad_adyacente, distancia = ciudad
                    consumo = (distancia / 100)
                    lista.append(consumo)
                    consumo_a_ciudad=min(lista)
                if ciudad_camion in CIUDADES_CARGA: #si la ciudad esta en rafaela o santa fe, el costo es=0
                    consumo_a_ciudad=0

        return consumo_a_ciudad


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
        if action is not None and state is not None: #dejamos de lado la primer acción
            camiones_estado, paquetes_estado = state
            id_camion, ciudad_camion, consumo_a_ciudad = action

            #identificamos el destino del camión
            for indice_camion, camion_estado in enumerate(camiones_estado):
                if camion_estado[0] == id_camion:
                    indice = indice_camion
            id_camion_estado, ciudad_camion_estado, nafta_camion_estado, paquetes_camion = camiones_estado[indice]

            lista_paquetes = []
            for paquete_en_camion in paquetes_camion: #agregar unicamente el id de paquete para devolver en el itinerario
                lista_paquetes.append(paquete_en_camion[0])
            lista_paquetes = tuple(lista_paquetes)

            itinerario.append((id_camion,ciudad_camion_estado,consumo_a_ciudad,lista_paquetes)) #armado de itinerario
        else:
            pass

    return itinerario

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