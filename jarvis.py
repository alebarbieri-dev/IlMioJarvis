import json
import pyttsx3
from groq import Groq

# --- CONFIGURAZIONE CERVELLO AI ---
client = Groq(api_key="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")

# --- LA VOCE ---
motore = pyttsx3.init()
motore.setProperty('rate', 170)

def parla(testo):
    print("JARVIS:", testo)
    motore.say(testo)
    motore.runAndWait()

# --- LE ORECCHIE (modalità tastiera) ---
def ascolta():
    print("🎙️ Scrivi cosa vuoi dirgli:")
    testo = input(" Tu: ")
    return testo.lower().strip()

# --- LA MEMORIA ---
def carica_agenda():
    try:
        with open('agenda.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def salva_agenda(dati):
    with open('agenda.json', 'w', encoding='utf-8') as file:
        json.dump(dati, file, ensure_ascii=False, indent=4)

# --- FUNZIONE PER CHIEDERE AL CERVELLO AI ---
def chiedi_al_cervello(domanda):
    try:
        print("🧠 JARVIS sta pensando...")
        completion = client.chat.completions.create(
                                                   model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": "Sei JARVIS, l'assistente vocale personale di uno studente italiano. Rispondi in modo breve, conciso e diretto (massimo 2 frasi). Non usare elenchi puntati o asterischi."},
                {"role": "user", "content": domanda}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"ERRORE: {e}")
        return "Scusa, ho un problema di connessione con il mio cervello centrale."

# --- IL CERVELLO LOCALE ---
parla("Ciao! Sono JARVIS. Nuovo cervello installato. Sono pronto a tutto.")

while True:
    comando = ascolta()
    agenda = carica_agenda()

    if "esci" in comando:
        parla("A presto! Spengo i sistemi.")
        break
        
    elif "aggiungi" in comando or "segna" in comando:
        parla("Cosa vuoi aggiungere? Dimmi: materie, compiti, sport, uscite o promemoria.")
        categoria = ascolta()
        chiave = "materie_domani" if categoria == "materie" else categoria
        
        if chiave in ["materie_domani", "compiti", "sport", "uscite", "promemoria"]:
            parla(f"Ok, dimmi cosa devo scrivere per {categoria}.")
            nuovo_valore = ascolta()
            if chiave == "materie_domani":
                if not isinstance(agenda.get(chiave), list): agenda[chiave] = []
                agenda[chiave].append(nuovo_valore)
            else:
                attuale = agenda.get(chiave, "")
                agenda[chiave] = attuale + ", " + nuovo_valore if attuale else nuovo_valore
            salva_agenda(agenda)
            parla("Perfetto, ho aggiornato la tua agenda.")

    elif "domani" in comando or "materie" in comando:
        materie = agenda.get("materie_domani", [])
        parla(f"Domani hai: {', '.join(materie)}." if materie else "Nessuna materia registrata.")
    elif "compiti" in comando:
        parla(f"I tuoi compiti sono: {agenda.get('compiti', 'nessuno')}")
    elif "sport" in comando or "cyclette" in comando:
        parla(f"Il tuo sport: {agenda.get('sport', 'nessuno')}")
    elif "uscite" in comando or "appuntamento" in comando or "piano" in comando:
        parla(f"Le tue uscite: {agenda.get('uscite', 'nessuna')}")
    elif "promemoria" in comando or "sciopero" in comando:
        parla(f"Promemoria: {agenda.get('promemoria', 'nessuno')}")

    elif comando != "":
        risposta_ai = chiedi_al_cervello(comando)
        risposta_pulita = risposta_ai.replace("*", "").replace("\n", " ")
        parla(risposta_pulita)