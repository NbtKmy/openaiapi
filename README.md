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

__Code:__

- ./notes/ocr_1.ipynb
- ./notes/ocr_2.ipynb
- ./notes/ocr_3.ipynb



### Audio-Transkription

__Verwendete Modelle:__

- GPT-4o-transcribe

__Code:__

- ./notes/simple_transcription.ipynb
- ./notes/transcribe_ramrod.ipynb


### MCP (Model Context Protocol)

__Verwendete Modelle:__

- GPT-4o-mini
- text-embedding-ada-002

__Code:__

- ./src/kafka_brief_an_den_vater.py (MCP-Server)
- ./src/kafka_chatbot_proxy.py (Chatbot mit MCP-Server)
- ./src/create_vectorstore.py (Erstellung des Vector-Stores)

[MCP (Model Context Protocol)](https://docs.anthropic.com/en/docs/mcp) ist ein Protokoll, das die Kommunikation zwischen einem großen Sprachmodell (LLM) und externen Tools standardisiert. Es dient als Schnittstelle, über die ein LLM als Agent auf Werkzeuge, Funktionen oder Datenquellen zugreifen kann. MCP wurde von dem KI-Unternehmen Anthropic entwickelt und gewinnt zunehmend an Bedeutung als mögliche Standardlösung für die Orchestrierung von KI-Agenten.

In diesem Beispiel wird ein MCP-Server und Client (Chatbot) erstellt.
Das Beispiel ist im Prinzip ein einfache RAG-Anwendung, realisiert mit MCP-Server.

Der MCP-Server hier besteht aus einem Vector-Store. Als Datenquelle ist Kafkas ["Brief an den Vater" von Wikisource](https://de.wikisource.org/wiki/Brief_an_den_Vater) genommen. 

Die Quelle sind nach Seitentrennung in einen Vector-Store untergebracht. Der MCP-Server (/src/kafka_brief_an_den_vater.py) bietet den Zugriff auf den Vector-Store.

Der Client ("src/kafka_chatbot_proxy.py") ist ein Chatbot, der bei Fragen auf den Vector-Store zurückgreift.

Der Vorteil von einem MCP-Server ist, dass der Server auch von den anderen MCP-Client verwendet werden kann. In diesem Beispiel betrachten wir, wie der MCP-Server in die Coding-Software "Cursor" eingebunden werden kann.

In der RENKU-Umgebung kann man den Chatbot so starten:

```python

python /home/jovyan/lab/openaiapi/src/kafka_chatbot_proxy.py \
  --port 8502 \
  --root_path "${RENKU_BASE_URL_PATH%/}"

  ````

Um die Gradio-Applikation zu stoppen, kann man "Control + C" im Terminal drücken.



---

__Quelle:__
„Brief an den Vater – Wikisource“. Zugegriffen 24. Juli 2025. https://de.wikisource.org/wiki/Brief_an_den_Vater.

### Weitere Tools

Hier erwähne ich nebenbei, dass sonst noch zahlreiche KI-Tools (natürlich) vorhanden sind.
Weitere Beispiele: 

- [Aeneas](https://deepmind.google/discover/blog/aeneas-transforms-how-historians-connect-the-past/)
- [Historian's Friend](https://chatgpt.com/g/g-u5cMhl7RY-the-historian-s-friend)



## GenAI als (Forschnungs-)Methode

Man kann GenAI in eine Analyse integrieren. Hier ein Paar wichtige Aspekte dabei: 

- Datensicherheit
> By default, business data from ChatGPT Business, ChatGPT Enterprise, ChatGPT Edu, and the API Platform (after March 1, 2023) isn't used for training our models, unless you have explicitly opted in to share your data with us to improve the services. 

([link](https://openai.com/enterprise-privacy/), gesichtet am 30. Sept. 2025)

- Datenkontrolle durch OpenAI
> By default, abuse monitoring logs are generated for all API feature usage and retained for up to 30 days, unless we are legally required to retain the logs for longer.

 ([link](https://platform.openai.com/docs/guides/your-data), gesichtet am 30. Sept. 2025)

- Reproduzierbarkeit
> Chat Completions are non-deterministic by default (which means model outputs may differ from request to request). That being said, we offer some control towards deterministic outputs by giving you access to the seed parameter and the system_fingerprint response field.

([link](https://platform.openai.com/docs/advanced-usage#reproducible-outputs), gesichtet am 30. Sept. 2025)

## YouTube-Kommentare analysieren

__Verwendete Modelle__
- text-embedding-3-small
- gpt-4o-mini


__Code:__

- ./notes/analysing_youtube_comments_1.ipynb
- ./notes/analysing_youtube_comments_3.ipynb

__Beschreibung:__

In diesem Beispiel nehmen wir die Kommentare von [diesem YouTube-Video](https://youtu.be/6dWYxKW5rY4?feature=shared) durch die API-Schnittstelle und analysieren mit text-embedding und gpt-4o-mini-Modelle. Die Analyse wird maschinell durchgefürht. In der Analyse sind die beiden Modelle integriert und unentbehrlich in diesem Prozess.


