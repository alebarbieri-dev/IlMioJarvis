import json
import pyttsx3

# --- LA VOCE ---
motore = pyttsx3.init()
motore.setProperty('rate', 170)

def parla(testo):
    print("JARVIS:", testo)
    motore.say(testo)
    motore.runAndWait()

# --- LE ORECCHIE (modalità tastiera) ---
def ascolta(messaggio="Scrivi cosa vuoi dirgli:"):
    print(f"🎙️ {messaggio}")
    testo = input("👤 Tu: ")
    return testo.lower().strip()

# --- LA MEMORIA ---
def carica_agenda():
    try:
        with open('agenda.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salva_agenda(dati):
    """Questa funzione scrive fisicamente nel file JSON"""
    with open('agenda.json', 'w', encoding='utf-8') as file:
        json.dump(dati, file, ensure_ascii=False, indent=4)

# --- IL CERVELLO ---
parla("Ciao! Sono JARVIS. Sistemi avviati e memoria dinamica attiva.")

while True:
    comando = ascolta()
    agenda = carica_agenda()

    if "esci" in comando:
        parla("A presto! Spengo i sistemi.")
        break
        
    # --- NUOVA FUNZIONE: AGGIUNGERE COSE ---
    elif "aggiungi" in comando or "segna" in comando or "salva" in comando:
        parla("Cosa vuoi aggiungere? Dimmi: materie, compiti, sport, uscite o promemoria.")
        categoria = ascolta("Scegli la categoria:")
        
        chiave = categoria
        if categoria == "materie":
            chiave = "materie_domani"
            
        if chiave in ["materie_domani", "compiti", "sport", "uscite", "promemoria"]:
            parla(f"Ok, dimmi cosa devo scrivere per {categoria}.")
            nuovo_valore = ascolta("Cosa devo scrivere?")
            
            if chiave == "materie_domani":
                if not isinstance(agenda.get(chiave), list):
                    agenda[chiave] = []
                agenda[chiave].append(nuovo_valore)
            else:
                attuale = agenda.get(chiave, "")
                agenda[chiave] = attuale + ", " + nuovo_valore if attuale else nuovo_valore
                
            salva_agenda(agenda)
            parla("Perfetto, ho aggiornato la tua agenda.")
        else:
            parla("Non ho capito la categoria. Riprova.")

    # --- RISPOSTE STANDARD ---
    elif "domani" in comando or "materie" in comando:
        materie = agenda.get("materie_domani", [])
        if materie:
            parla(f"Domani hai: {', '.join(materie)}.")
        else:
            parla("Non ho registrato materie per domani.")
            
    elif "compiti" in comando:
        parla(f"I tuoi compiti sono: {agenda.get('compiti', 'nessun compito registrato')}")
        
    elif "sport" in comando or "allenamento" in comando or "cyclette" in comando:
        parla(f"Il tuo sport: {agenda.get('sport', 'nessuno sport registrato')}")
        
    elif "amici" in comando or "uscite" in comando or "crush" in comando:
        parla(f"Le tue uscite: {agenda.get('uscite', 'nessuna uscita registrata')}")
        
    elif "ricorda" in comando or "promemoria" in comando or "sciopero" in comando:
        parla(f"Promemoria: {agenda.get('promemoria', 'nessun promemoria attivo')}")
        
    elif "ciao" in comando:
        parla("Ciao! È un piacere sentirti.")
        
    elif "come stai" in comando:
        parla("Tutti i sistemi sono operativi al cento per cento. Grazie!")
        
    elif comando != "":
        parla("Ho sentito: " + comando + ". Non so ancora cosa significa, ma imparerò.")