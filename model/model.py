import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.best_peso = None
        self.best_sol = None
        self.teams = None
        self.graph = nx.Graph()

    def get_teams(self, anno):
        self.teams = DAO.get_teams(anno)
        return self.teams

    def build_graph(self):
        self.graph.clear()
        self.graph.add_nodes_from(self.teams)
        for t1 in self.graph.nodes:
            for t2 in self.graph.nodes:
                if t1 != t2:
                    self.graph.add_edge(t1, t2, weight=t1.somma_salari + t2.somma_salari)
        return self.graph

    def get_sorted_neighbors(self, squadra):
        result = [(n, self.graph[squadra][n]['weight']) for n in self.graph.neighbors(squadra)]
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def get_percorso(self, squadra):
        self.best_sol = []
        self.best_peso = 0
        sorted_neighbors = self.get_sorted_neighbors(squadra)
        for n in sorted_neighbors:
            parziale = [squadra, n[0]]
            somma_pesi = [squadra.somma_salari + n[0].somma_salari]
            self.ricorsione(parziale, somma_pesi)
            parziale.pop()
        return self.best_sol, self.best_peso

    def ricorsione(self, parziale, somma_pesi):
        ultimo = parziale[-1]
        sorted_neighbors = self.get_sorted_neighbors(ultimo)
        if self.graph[ultimo][sorted_neighbors[-1][0]]['weight'] > self.graph[parziale[-2]][ultimo]['weight']:
            return
        peso_sol = somma_pesi[-1]
        if peso_sol > self.best_peso:
            self.best_sol = copy.deepcopy(parziale)
            self.best_peso = peso_sol
            print(parziale)
        for neighbor in sorted_neighbors:
            if self.check(parziale, neighbor):
                parziale.append(neighbor[0])
                somma_pesi.append(peso_sol + neighbor[0].somma_salari)
                self.ricorsione(parziale, somma_pesi)
                parziale.pop()
                somma_pesi.pop()

    def check(self, parziale, neighbor):
        ultimo = parziale[-1]
        ultimo_peso = self.graph[parziale[-2]][ultimo]['weight']
        da_aggiungere = self.graph[ultimo][neighbor[0]]['weight']
        if neighbor not in parziale and da_aggiungere < ultimo_peso:
            return True
        return False

    def get_peso_arco(self, edge):
        return self.graph[edge[0]][edge[1]]['weight']
