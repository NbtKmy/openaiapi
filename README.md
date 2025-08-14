# ChatGPT-API für die Wissenschaft nutzen

## Intro

In diesem Workshop probieren wir verschiedene API-Schnittstellen von OpenAI für wissenschaftliche Zwecke aus.
Was Oberbichler und Petz (2025) in ihrem Working Paper für Geschichtsforschung schreibt, entspricht auch den Geisteswissenschaften allgemein. Die Anwendungen der GenAI für Geisteswissenschaften können grob gesagt in zwei Umsetzungsebenen, AI als ein Tool oder AI als Methode, unterteilt werden. 
Hier werden die Anwendungsbeispiele nach diesem Schema gezeigt.

Oberbichler, Sarah, and Cindarella Petz. “Working Paper: Implementing Generative AI in the Historical Studies”. Zenodo, February 25, 2025. https://doi.org/10.5281/zenodo.14924737.



## Verschiedene APIs bei OpenAI

Wie oben erwähnt, bietet OpenAI Zugriffe auf verschiedene KI-Modelle:

- LLMs wie GPT-4.1, 4o-mini, o3 usw.
- Image Generation Modells wie DALL.E 2, DALL.E 3 usw.
- TTS (Text-to-Speach) wie TTS-1, GPT-4o mini TTS usw.
- Transkription wie GPT-4o Transcribe, GPT-4o mini Transcribe, Whisper
- Embeddings wie text-embedding-3 small, text-embedding-3 large,  text-embedding-ada-002

Weitere Modelle sind [hier](https://platform.openai.com/docs/models) zu sehen.


## GenAI als Tool

Wir testen hier 3 Anwendungsbeispiele, bei denen GenAI als Hilfstools eingesetzt werden:

1. OCR (von digitalen Bildern zu Text, auch strukturierte Ausgabe)
1. Transkription (von Audio-Daten zu digitalem Text)
1. KI-Agent mit MCP

### OCR

__Verwendete Modelle:__
- GPT-4.1





### Audio-Transkription


### MCP (Model Context Protocol)

__Verwendete Modelle:__
- GPT-4o-mini
- text-embedding-ada-002

__Code:__
- ./src/kafka_brief_an_den_vater.py (MCP-Server)
- ./src/ask_kafka_client.py (MCP-Client)
- ./src/create_vectorstore.py (Erstellung des Vector-Stores)

[MCP (Model Context Protocol)](https://docs.anthropic.com/en/docs/mcp) ist ein Protokoll, das die Kommunikation zwischen einem großen Sprachmodell (LLM) und externen Tools standardisiert. Es dient als Schnittstelle, über die ein LLM als Agent auf Werkzeuge, Funktionen oder Datenquellen zugreifen kann. MCP wurde von dem KI-Unternehmen Anthropic entwickelt und gewinnt zunehmend an Bedeutung als mögliche Standardlösung für die Orchestrierung von KI-Agenten.

In diesem Beispiel wird ein MCP-Server und Client (Chatbot) erstellt.
Das Beispiel ist im Prinzip ein einfache RAG-Anwendung, realisiert mit MCP-Server.

Der MCP-Server hier besteht aus einem Vector-Store. Als Datenquelle ist Kafkas ["Brief an den Vater" von Wikisource](https://de.wikisource.org/wiki/Brief_an_den_Vater) genommen. 

Die Quelle sind nach Seitentrennung in einen Vector-Store untergebracht. Der MCP-Server (/src/kafka_brief_an_den_vater.py) bietet den Zugriff auf den Vector-Store.

Der Client ("src/ask_kafka_client.py") ist ein Chatbot, der bei Fragen auf den Vector-Store zurückgreift.

Der Vorteil von einem MCP-Server ist, dass der Server auch von den anderen MCP-Client verwendet werden kann. In diesem Beispiel betrachten wir, wie der MCP-Server in die Coding-Software "Cursor" eingebunden werden kann.



---

__Quelle:__
„Brief an den Vater – Wikisource“. Zugegriffen 24. Juli 2025. https://de.wikisource.org/wiki/Brief_an_den_Vater.

### Weitere Tools

Hier erwähne ich nebenbei, dass sonst noch zahlreiche KI-Tools (natürlich) vorhanden sind.
Weitere Beispiele: 

- [Aeneas](https://deepmind.google/discover/blog/aeneas-transforms-how-historians-connect-the-past/)
- [Historian's Friend](https://chatgpt.com/g/g-u5cMhl7RY-the-historian-s-friend)



## GenAI als (Forschnungs-)Methode

