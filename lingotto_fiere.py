from csv import reader

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.__nome = nome
        self.__lista_stand = []
        self.__lista_espositori = []

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def lista_stand(self):
        return self.__lista_stand

    @property
    def lista_espositori(self):
        return self.__lista_espositori

    def aggiungi_stand(self, stand):
        self.__lista_stand.append(stand)

    def aggiungi_espositore(self, espositore):
        self.__lista_espositori.append(espositore)


    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as csvReader:
                infile = reader(csvReader)
                for row in infile:
                    codice=row[0]
                    if codice[:2]== "ST":   #controllo se la riga contiene uno stand
                        superficie = row[1]
                        padiglione = row[2]
                        prezzo_base = int(row[3])
                        tipologia = row[4] if len(row) > 4 else ""
                        if tipologia == "":
                            tipologia = "Standard"
                            prezzo_finale = prezzo_base
                        elif tipologia.isdigit():
                            prezzo_finale = int(prezzo_base) + (0.07 * int(tipologia))
                        elif tipologia.isalpha():
                            prezzo_finale = int(prezzo_base) * 1.30

                        stand = Stand(codice, superficie, padiglione, prezzo_base, tipologia, prezzo_finale)
                        self.aggiungi_stand(stand)

                    elif codice[:2]== "ES":     #controllo se la riga contiene un espositore
                        espositore = Espositore(row[0], row[1], row[2])
                        self.aggiungi_espositore(espositore)

        except FileNotFoundError:
            print("file not found")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand_trovato = None    # cerco lo stand
        for stand in self.__lista_stand:
            if stand.codice == codice_stand:
                stand_trovato = stand
                break

        if stand_trovato is None:
            raise ValueError(f"Errore: Lo stand con codice '{codice_stand}' non esiste.")

        espositore_trovato = None   # cerco l'espositore
        for espositore in self.__lista_espositori:
            if espositore.codice == codice_espositore:
                espositore_trovato = espositore
                break

        if espositore_trovato is None:
            raise ValueError(f"Errore: L'espositore con codice '{codice_espositore}' non esiste.")

        if not stand_trovato.disponibile:
            raise ValueError(f"Errore: Lo stand '{stand_trovato.codice}' non è disponibile.")

        for stand in self.__lista_stand:
            if stand.espositore == espositore_trovato:
                raise ValueError(f"Errore: L'espositore '{codice_espositore}' è già associato a un altro stand.")

        stand_trovato.disponibile = False
        stand_trovato.espositore = espositore_trovato
        print(f"Successo: Stand {codice_stand} assegnato all'espositore {codice_espositore}.")

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori specificando, quando applicabile, lo stand."""
        for espositore in self.__lista_espositori:
            # Cerco se esiste uno stand associato a questo espositore
            stand_trovato = None
            for stand in self.__lista_stand:
                if stand.espositore == espositore:
                    stand_trovato = stand
                    break
            # Se lo stand esiste, stampo il suo codice, altrimenti diciamo "Nessuno"
            if stand_trovato:
                print(f"{espositore} - Stand assegnato: {stand_trovato.codice}")
            else:
                print(f"{espositore} - Stand assegnato: Nessuno")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.__lista_stand)

class Stand:
    def __init__(self, codice_stand, superficie, padiglione, prezzo_base, tipologia, prezzo_finale):
        self.__codice_stand = codice_stand
        self.__superficie = superficie
        self.__padiglione = padiglione
        self.__prezzo_base = prezzo_base
        self.__tipologia = tipologia
        self.__prezzo_finale = prezzo_finale
        self.__disponibile = True
        self.__espositore = None

    def __lt__(self, other):
        return self.__prezzo_finale < other.__prezzo_finale

    def __str__(self):
        return f"Stand {self.__codice_stand}: {self.__tipologia} | {self.__superficie}mq - Pad. {self.__padiglione} - Prezzo: {self.__prezzo_finale}€"

    @property
    def codice(self): return self.__codice_stand

    @property
    def disponibile(self): return self.__disponibile

    @disponibile.setter
    def disponibile(self, val): self.__disponibile = val

    @property
    def espositore(self): return self.__espositore

    @espositore.setter
    def espositore(self, val): self.__espositore = val

    @property
    def prezzo_finale(self): return self.__prezzo_finale

class Espositore:
    def __init__(self, codice_espositore, nome, cognome):
        self.__codice_espositore = codice_espositore
        self.__nome = nome
        self.__cognome = cognome

    def __str__(self):
        return f"Espositore {self.codice}: {self.__nome} {self.__cognome}"

    @property
    def codice(self): return self.__codice_espositore