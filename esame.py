# =========================================================
# ---------- Esame Laboratorio di Programmazione ----------
# Corso di Laurea: Intelligenza Artificiale e Data Analytic
# Autore: Andrea Nuzzo (MAT. SM3201217)
# Data consegna: 09/02/2021
# =========================================================

class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    def __init__(self, name=None):

        # Setto il nome del file
        self.name = name
        
        # Settando name su None cosi da poter sollevare l'eccezione se non viene inserito alcun dato come argomento
        if name == None:
            raise ExamException('Il nome del file deve essere una stringa non vuota')

        # Sollevo un eccezione se il nome non e' un stringa 
        if not isinstance(name, str):
            raise ExamException('Il nome del file deve essere una stringa non vuota')

         # Sollevo un eccezione se il nome e' un stringa vuota 
        if name == '':
            raise ExamException('Il nome del file deve essere una stringa non vuota')


    def get_data(self):

        # Inizzializzo una lista vuota per salvare i valori
        values = []

        # Provo ad aprire il file per estrarci i dati. Se non ci riesco sollevo un eccezione 
        try:
            data_file = open(self.name, 'r')

        except:
            raise ExamException ('Errore apertura file')
            
        # Inserisco un contatore di righe del file per stampare degli avvertimenti all'utente
        count = 1

        # Provo a leggere il file linea per linea 
        try:
            for line in data_file:
            
                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                # Le variabili elements[0] (epoch) e elements[1] (temperature) al momento sono ancora stringhe,
                # in quanto ho letto il file di testo, pertanto le convertiamo. La prima in intero e la seconda in
                # valore numerico. Se dovesse ritornare un errore non solleviamo un eccezioni ma ignoriamo la riga
                # contenente l'errore.
                try:
                    elements[0] = int(float(elements[0]))
                    elements[1] = float(elements[1])
                except:
                    continue
                
                # Se epoch è minore di zero salto la riga
                if elements[0]< 0:
                    continue

                count +=1
                # Se gli elementi per riga sono piu' di due avverto l'utente che i dati oltre la colonna due non verrano letti
                if len(elements) > 2:
                    print(f" ATTENZIONE: alla riga {count} ci sono più di due valori (epoch,temperature). I valori successivi al secondo verranno ignorati\n")
                
                # Considerando che le temperature massime e minime mai registrate sul nostro pianeta,
                # sono rispettivamente 57.8°C e − 98.7 °C se nelle temperatura ci sono dati che superano 
                # questo range avverto con un print per non inquinare la statistica ... Anche se dovremmo
                # abbassare il range (0°C - 45°C) visto che parliamo dell'interno di una abitazione.
                if elements [1] < -98.7 or elements [1] > 57.8:
                    print(f" ATTENZIONE: alla riga {count} la temperatura inserita e' pari a {elements[1]} °C\n")

                # Aggiungo alla lista dei valori le righe convertite in interi e float
                values.append(elements[0:2])
                    
        # Se il file può essere aperto ma i dati contenuti all'interno non possono essere processati sollevo un eccezione (Esempio: tabella estrapolata da excel)
        except UnicodeDecodeError:
            raise ExamException('Errore nella lettura dei dati nel file')
        
        # Chiudo il file
        data_file.close()

        # Se i valori di epoch non sono ordinato o sono duplicati sollevo un eccezione
        for i in range(1,len(values)):
            if values[i][0] <= values[i-1][0]:
                raise ExamException('I valori di epoch non sono in ordine o sono ducplicati')
            
        return values




# ===============================
# ----- CORPO DEL PROGRAMMA -----
# ===============================

time_series_file = CSVTimeSeriesFile('data.csv')

time_series = time_series_file.get_data()


# Funzione per il calcolo della statistica giornaliera delle temperature
def daily_stats(values_data_file = None):

    # Attuo i controlli minimi nel caso i valori in 'values_data_file' siano stati inseriti a mano 
    # (copia e incolla), quindi che values_data_file sia una matrice (lista contenente delle liste con il 
    # primo elemento un valore intero e come secondo elemento un float) se cosi non fosse ignoro l'elemento
    # contenente l'errore.

    # Inizzializzo una variabile per controllare i dati inseriti in values_data_file
    check_values_data_file = []

    # Controllo che sia stato inserito un valore su values_data_file per questo ho settato l'argomento su None
    # cosi da poter sollevare l'eccezione.
    if values_data_file == None:
        raise ExamException("Non e' stato inserito nessun argomento per la funzione daily_stats" )

    # Controllo che values_data_file sia una lista
    if not isinstance(values_data_file, list):
        raise ExamException('values_data_file deve essere una lista')

    # Controllo che all'interno di values_data_file ci siano delle liste contenenti due valori ...
    for item in values_data_file:
        if not isinstance(item, list):
            raise ExamException("I valori all'interno di values_data_file devono essere liste contenenti il timestamp e la temperatura")
        
        # e che questi valori siano il primo un interi ed il secondo un float se cosi non fosse salto l'elemento
        try:
            item[0] = int(float(item[0]))
            item[1] = float(item[1])
        except:
            continue
        
        # Adesso che ho controllato values_data_file appendo i valori validi e continuo con la statistica
        check_values_data_file.append(item)

    # Inizzializzo una lista vuota dove inserire tutti i giorni da analizzare
    list_of_days = []

    # Inizzializzo una lista vuota dove inserire la statistica delle temperature giornaliere [min, max, media]
    daily_temperature_statistics = []

    # Trovo l'inizio del giorno per ogni elemento e lo sostituisco
    for item in check_values_data_file:
        item[0] = item[0] - (item[0] % 86400)

        # Creo una lista dei giorni da confrontare con gli elementi nella variabile "check_values_data_file"
        list_of_days.append(item[0])
    
    # Elimino i duplicati dalla lista dei giorni e li metto in ordine cosi da ottenere il totale dei giorni contenuti nella lista
    days_in_the_file = list(set(list_of_days))
    days_in_the_file.sort()

    # Inizio il confronto per ogni giorno nella varaibile "days_in_the_file"
    for item in days_in_the_file:

        # Inizzializzo una lista vuota dove inserire le temperature di un singolo giorno
        temperatures_in_the_day = []

        for i in range(len(check_values_data_file)):
            # Se il valore epoch e' uguale al giorno in "days_in_the_file"...
            if check_values_data_file[i][0] == item:

                # Allora inserisco la temperatura nella lista del giorno che sto esaminando
                temperatures_in_the_day.append(check_values_data_file[i][1])
        
        # Adesso avendo tutte le temperature di un singolo giorno, trovo il minimo, il massimo e la media e
        # li inserisco come lista nella nella statistica delle temperature giornaliere
        daily_temperature_statistics.append([min(temperatures_in_the_day),max(temperatures_in_the_day),sum(temperatures_in_the_day)/len(temperatures_in_the_day)])

    # Se la statistica presenta meno di 28 o più di 31 dati sollevo un eccezione
    if len(daily_temperature_statistics) < 28 or len(daily_temperature_statistics) > 31:
        raise ExamException(f"Non e' presente almeno una misurazione di temperatura per ogni giorno nel mese o vi sono dati per piu' di un mese. I giorni contenuti sono {len(daily_temperature_statistics)}")
    
    # Ritorno una matrice con le statistiche delle temperature
    return daily_temperature_statistics

daily_stats(time_series)