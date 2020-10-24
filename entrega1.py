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



class MercadoArtificial(SearchProblem):

    def is_goal(self, state):
        pass

    def cost(self, state1, action, state2):
        pass

    def actions(self, state):
        pass

    def result(self, state, action):
        pass

    def heuristic(self, state):
        pass

if __name__ == '__main__':
    problema = MercadoArtificial(INITIAL_STATE)