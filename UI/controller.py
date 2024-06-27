import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.squadra_scelta = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_dd_year(self):
        for y in range(2019, 1979, -1):
            self.view.ddAnno.options.append(ft.dropdown.Option(f"{y}"))

    def handle_dd_selection(self, e):
        anno = int(self.view.ddAnno.value)
        teams = self.model.get_teams(anno)
        self.view.txtOutSquadre.controls.clear()
        self.view.txtOutSquadre.controls.append(ft.Text(f"Nel {anno} hanno giocato {len(teams)} squadre"))
        for t in teams:
            self.view.txtOutSquadre.controls.append(ft.Text(t))
        self.view.btnCreaGrafo.disabled = False
        self.fill_dd_squadre(teams)
        self.view.update_page()

    def fill_dd_squadre(self, teams):
        self.view.ddSquadra.options.clear()
        for t in teams:
            self.view.ddSquadra.options.append(ft.dropdown.Option(data=t,
                                                                  text=t,
                                                                  on_click=self.scegli_squadra))
    def scegli_squadra(self, e):
        if e.control.data is None:
            self.squadra_scelta = None
        self.squadra_scelta = e.control.data

    def handleCreaGrafo(self, e):
        graph = self.model.build_graph()
        self.view.btnDettagli.disabled = False
        self.view.btnPercorso.disabled = False
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {len(graph.nodes)} Numero di archi: {len(graph.edges)}"))
        self.view.update_page()

    def handleDettagli(self, e):
        if self.squadra_scelta is None:
            self.view.txt_result.controls.clear()
            self.view.txt_result.controls.append(ft.Text(f"SCEGLIERE UNA SQUADRA"))
            self.view.update_page()
            return
        sorted_neighbors = self.model.get_sorted_neighbors(self.squadra_scelta)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Dettagli per {self.squadra_scelta}:"))
        for n in sorted_neighbors:
            self.view.txt_result.controls.append(ft.Text(f"{n[0]}, peso = {n[1]}"))
        self.view.update_page()

    def handlePercorso(self, e):
        if self.squadra_scelta is None:
            self.view.txt_result.controls.clear()
            self.view.txt_result.controls.append(ft.Text(f"SCEGLIERE UNA SQUADRA"))
            self.view.update_page()
            return
        path, peso = self.model.get_percorso(self.squadra_scelta)
        self.view.txt_result.controls.clear()
        self.view.txt_result.controls.append(ft.Text(f"Il percorso trovato ha peso {peso}:"))
        for i in range(len(path)-1):
            self.view.txt_result.controls.append(
                ft.Text(f"{path[i]} --> {path[i+1]}, {self.model.get_peso_arco((path[i], path[i+1]))}"))
        self.view.update_page()

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model
