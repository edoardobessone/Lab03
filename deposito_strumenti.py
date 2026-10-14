class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.codice} - {self.tipo} ({self.marca}) | Anno: {self.anno_acquisto} | Valore: €{self.valore}"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito} | Strumento: {self.id_strumento} | Allievo: {self.cognome_allievo} | Data: {self.data}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            file = open(file_path, "r", encoding="utf-8")
            for linea in file:
                linea = linea.rstrip()
                if linea != "":
                    parti = linea.split(",")
                    if len(parti) == 5:
                        codice = parti[0].rstrip()
                        tipo = parti[1].rstrip()
                        marca = parti[2].rstrip()
                        try:
                            anno = int(parti[3].rstrip())
                            valore = float(parti[4].rstrip())

                            nuovo_strumento = Strumento(codice, tipo, marca, anno, valore)
                            self.strumenti.append(nuovo_strumento)
                        except ValueError:
                            errore = True
            file.close()
            print("Strumenti caricati con successo.")
        except FileNotFoundError:
            raise FileNotFoundError("Errore: il file non esiste.")
        except Exception as e:
            print(f"Errore generico: {e}")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        numero_max = 0
        for strumento in self.strumenti:
            codice_attuale = strumento.codice
            if codice_attuale[0] == 'S':
                try:
                    numero = int(codice_attuale[1:])
                    if numero > numero_max:
                        numero_max = numero
                except ValueError:
                    errore = True

        nuovo_codice = f"S{numero_max + 1}"
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        strumenti_ordinati = list(self.strumenti)

        for i in range(len(strumenti_ordinati)):
            for j in range(0, len(strumenti_ordinati) - i - 1):
                if strumenti_ordinati[j].marca > strumenti_ordinati[j + 1].marca:
                    temp = strumenti_ordinati[j]
                    strumenti_ordinati[j] = strumenti_ordinati[j + 1]
                    strumenti_ordinati[j + 1] = temp

        return strumenti_ordinati

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        strumento_trovato = False
        for strumento in self.strumenti:
            if strumento.codice == id_strumento:
                strumento_trovato = True

        if strumento_trovato == False:
            raise Exception("Lo strumento richiesto non esiste nel sistema.")

        for prestito in self.prestiti:
            if prestito.id_strumento == id_strumento:
                raise Exception("Lo strumento è già in prestito.")

        numero_max_prestito = 0
        for prestito in self.prestiti:
            id_attuale = prestito.id_prestito
            if id_attuale[0] == 'P':
                try:
                    numero = int(id_attuale[1:])
                    if numero > numero_max_prestito:
                        numero_max_prestito = numero
                except ValueError:
                    errore = True

        nuovo_codice_prestito = f"P{numero_max_prestito + 1}"
        nuovo_prestito = Prestito(nuovo_codice_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(nuovo_prestito)
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        prestito_trovato = False
        indice_da_rimuovere = -1

        for i in range(len(self.prestiti)):
            if self.prestiti[i].id_prestito == id_prestito:
                prestito_trovato = True
                indice_da_rimuovere = i

        if prestito_trovato == False:
            raise Exception("Nessun prestito trovato con questo codice.")

        self.prestiti.pop(indice_da_rimuovere)
