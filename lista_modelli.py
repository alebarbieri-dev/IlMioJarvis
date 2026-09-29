from groq import Groq

client = Groq(api_key="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")

modelli = client.models.list()
print("📋 MODELLI DISPONIBILI SU GROQ:\n")
for m in modelli.data:
    print(f"  → {m.id}")