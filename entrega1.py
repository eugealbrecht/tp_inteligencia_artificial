from itertools import count

from simpleai.search import(
SearchProblem,
breadth_first,
depth_first,
uniform_cost,
greedy,
astar,
)

from simpleai.search.viewers import WebViewer, BaseViewer
INITIAL_STATE=()

def planear_camiones(metodo, camiones, paquetes):
    INITIAL_STATE = (camiones, paquetes)
    #camiones = (id, ciudad origen, capacidad maxima de comb.)
    #paquetes = (id, ciudad origen, ciudad destino)

    print(INITIAL_STATE)
    return INITIAL_STATE

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

class MercadoArtificial(SearchProblem):

    def is_goal(self, state):
        camiones, paquetes = state
        id_camion, origen_camion, capacidad = camiones
        id_paquete, origen_paquete, destino_paquete = paquetes

        pass

    def cost(self, state1, action, state2):
        return 1 

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def heuristic(self, state):
        camiones, paquetes=state
        paquetes=list(paquetes)
        cant_paquetes=count(paquetes[0])
        # me faltan tantas acciones como paquetes me falten entregar para llegar a la cantidad total de paquetes en el camion
        return cant_paquetes - len(state)

if __name__ == '__main__':
    problema = MercadoArtificial(INITIAL_STATE)