from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceDDAeroportoP = None
        self._choiceDDAeroportoD = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()


    def handleAnalizza(self,e):
        nMinTxt=self._view._txtInCMin.value
        if nMinTxt== "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico"))
            self._view.update_page()
            return
        try:
            cMin=int(nMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico intero"))
            self._view.update_page()
            return
        if cMin < 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico intero positivo"))
            self._view.update_page()
            return

        self._model.buildGraph(cMin)

        allNodes=self._model.getAllNodes()
        self._fillDD(allNodes)


        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato"))
        self._view.txt_result.controls.append(ft.Text(nNodes))
        self._view.txt_result.controls.append(ft.Text(nEdges))
        self._view.update_page()





    def handleCerca(self,e):
        v0=self._choiceDDAeroportoP
        v1=self._choiceDDAeroportoD
        t=self._view._txtInTratteMax.value
        tint=int(t)
        #dovresti fare un try except e controllare sia inserito
        tic=datetime.now()
        path,score=self._model.getCamminoOttimo(v0,v1,tint)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Percorso ottimo"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score totale: {score}"))
        self._view.txt_result.controls.append(ft.Text(f"Percorso trovato in: {datetime.now() - tic}"))
        self._view.update_page()



    def handleConnessi(self,e):
        node=self._choiceDDAeroportoP
        if node is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non hai selezionato un areoporto di partenza"))
            self._view.update_page()
            return
        viciniTuple=self._model.getSortedNeighbors(node)
        self._view.txt_result.controls.append(ft.Text("i vicini dell'areoporto selezionato sono:"))
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[0]}-peso {v[1]}"))
            self._view.update_page()


    def _fillDD(self,allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n,
                                                                       key=n.IATA_CODE,
                                                                       on_click=self.pickDDPartenza))
            self._view._ddAeroportoD.options.append(ft.dropdown.Option(data=n,
                                                                       key=n.IATA_CODE,
                                                                       on_click=self.pickDDArrivo))
        self._view.update_page()

    def pickDDPartenza(self,e):
        self._choiceDDAeroportoP=e.control.data

    def pickDDArrivo(self,e):
        self._choiceDDAeroportoD=e.control.data


    def handlePercorso(self,e):
        v0=self._choiceDDAeroportoP
        if v0 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non hai selezionato un areoporto di partenza"))
            self._view.update_page()
            return
        v1=self._choiceDDAeroportoD
        if v1 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non hai selezionato un areoporto di destinazione"))
            self._view.update_page()
            return
        path=self._model.getPath(v0,v1)
        if len(path)==0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non c'è nessun volo fra i 2 aeroporti"))
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("percorso trovato, di seguito i nodi del cammino"))
            for v in path:
                self._view.txt_result.controls.append(ft.Text(v))
        self._view.update_page()


