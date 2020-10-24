from simpleai.search import(
SearchProblem,
breadth_first,
depth_first,
uniform_cost,
greedy,
astar,
)

from simpleai.search.viewers import WebViewer, BaseViewer

INITIAL_STATE = ()

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