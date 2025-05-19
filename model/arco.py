from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Arco():
    aeroportoP: Airport
    aeroportoD: Airport
    peso: int
    #meglio della tupla perchè non vai per posizione ma per nomi con i punti
