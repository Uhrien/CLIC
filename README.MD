# CLIC - Customizable Looped Input Clicker

CLIC è un programma sviluppato in Python con interfaccia grafica basata su `CustomTkinter`. Consente di generare automaticamente click del mouse a una frequenza regolabile, fornendo un'interfaccia intuitiva con due modalità operative principali.

## Funzionalità

- **Automazione dei Click**: Il programma permette di attivare uno spam di click automatici con il tasto sinistro del mouse a una frequenza personalizzabile.
- **Modalità Operative**: Sono disponibili due modalità:
  - **Toggle**: Attiva o disattiva lo spam dei click con un singolo tocco del tasto `CTRL`.
  - **Push to Activate**: Lo spam dei click è attivo solo mentre `CTRL` è premuto e si ferma al rilascio.
- **Feedback Visivo**: Il programma mostra lo stato attuale in modo prominente con una label che indica "ARMED" (in rosso) durante lo spam dei click e "DISARMED" (in verde) quando il programma è inattivo.
- **Controllo della Frequenza dei Click**: La frequenza dei click può essere incrementata o decrementata tramite la rotellina del mouse.

## Prerequisiti

Per eseguire questo programma, sono necessari i seguenti moduli Python:

*************************
pip install customtkinter pynput
*************************

## Come Utilizzare CLIC

1. **Avvio del Programma**: Avvia il programma eseguendo lo script Python. Apparirà una finestra con le seguenti sezioni:
   - **Selettore di Modalità**: Consente di scegliere tra le modalità `Toggle` e `Push to Activate`.
   - **Frequenza dei Click**: Permette di impostare il numero di click al secondo. È possibile modificare la frequenza sia manualmente, inserendo un valore nel campo, sia dinamicamente, utilizzando la rotellina del mouse durante l'esecuzione dello spam dei click.
   - **Label di Stato**: Mostra il feedback visivo "DISARMED" in verde quando il programma è inattivo e "ARMED" in rosso durante lo spam dei click.
   - **Istruzioni**: Elenca i comandi per utilizzare il programma in ciascuna modalità.

2. **Selezione della Modalità**:
   - **Toggle**:
     - Premere `CTRL` una volta per attivare lo spam dei click (lo stato diventa "ARMED").
     - Premere nuovamente `CTRL` per fermare lo spam dei click (lo stato torna a "DISARMED").
   - **Push to Activate**:
     - Tieni premuto `CTRL` per mantenere attivo lo spam dei click (lo stato è "ARMED").
     - Rilascia `CTRL` per fermare lo spam dei click (lo stato torna a "DISARMED").

3. **Regolazione della Frequenza dei Click**:
   - **Campo di Input**: Inserisci un numero nel campo di frequenza e premi `Invio` per aggiornare la frequenza.
   - **Rotellina del Mouse**: Durante lo spam dei click, scorri verso l'alto per aumentare la frequenza di 10 click per secondo o verso il basso per diminuirla di 10 click per secondo.

4. **Feedback Visivo**:
   - Durante lo spam dei click, la label di stato mostrerà "ARMED" in rosso.
   - Quando il programma è inattivo, la label di stato mostrerà "DISARMED" in verde.
   - Un'animazione sulla label di stato segnala visivamente l’attività del programma.

## Comandi Principali

- **CTRL Toggle**: Attiva/disattiva lo spam dei click in modalità `Toggle`.
- **CTRL Push**: Attiva lo spam dei click in modalità `Push to Activate`.
- **Mouse Wheel Up**: Aumenta la frequenza di click.
- **Mouse Wheel Down**: Diminuisce la frequenza di click.

## Suggerimenti e Note

- **Uso Responsabile**: Questo programma è un clicker automatico, e l'automazione dei click può interferire con altre applicazioni. Usalo con responsabilità.
- **Permessi**: Su alcuni sistemi, potrebbe essere necessario eseguire lo script con privilegi elevati per catturare gli eventi globali della tastiera e del mouse.

## Schermate dell'Interfaccia

**Stato DISARMED**:
*************************
[DISARMED] (in verde)
*************************

**Stato ARMED**:
*************************
[ARMED] (in rosso con animazione)
*************************

## Crediti

Progetto realizzato da Salvatore Gambino
