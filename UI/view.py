import flet as ft
from flet_core import MainAxisAlignment

from model.airport import Airport


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._btnPercorso = None
        self.txt_result = None
        self._btnCerca = None
        self._txtInTratteMax = None
        self._ddAeroportoD = None
        self._btnConnessi = None
        self._ddAeroportoP = None
        self._btnAnalizza = None
        self._txtInCMin = None
        self._page = page
        self._page.title = "Flights Manager"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None


    def load_interface(self):
        # title
        self._title = ft.Text("Flights Manager", color="blue", size=24)
        self._page.controls.append(self._title)

        self._txtInCMin=ft.TextField(label="N Compagnie min")
        self._btnAnalizza= ft.ElevatedButton(text="Analizza Aeroporti", on_click=self._controller.handleAnalizza)

        row1=ft.Row([ft.Container(None, width=250),ft.Container(self._txtInCMin, width=250),ft.Container(self._btnAnalizza, width=250) ], alignment=MainAxisAlignment.CENTER)

        self._ddAeroportoP=ft.Dropdown(label="Aeroporto partenza")
        self._btnConnessi=ft.ElevatedButton(text="Aeroporti connessi", on_click=self._controller.handleConnessi)

        row2=ft.Row([ft.Container(None, width=250),ft.Container(self._ddAeroportoP, width=250),ft.Container(self._btnConnessi, width=250) ], alignment=MainAxisAlignment.CENTER)
        self._ddAeroportoD=ft.Dropdown(label="Aeroporto destinazione")
        self._txtInTratteMax=ft.TextField(label="Numero di Tratte maxi")
        self._btnCerca=ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handleCerca)
        self._btnPercorso= ft.ElevatedButton(text="Cerca percorso", on_click=self._controller.handlePercorso)

        row3 = ft.Row([ft.Container(self._ddAeroportoD, width=250), ft.Container(self._txtInTratteMax, width=250),
                       ft.Container(self._btnCerca, width=250),  ft.Container(self._btnPercorso, width=250)], alignment=MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)
        self._page.update()

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
