def retrieve_documents(query, search_engine):
    """
    Nutzt ein Suchsystem, um Dokumente zu finden, die auf die Suchanfrage passen.
    :param query: Die Suchanfrage (Frage des Benutzers)
    :param search_engine: Das Suchsystem (z.B. Elasticsearch)
    :return: Liste von Dokumenten
    """
    # Transformiere die Abfrage mit BioLinkBERT in einen semantischen Vektor
    query_vector = biolinkbert_transform(query)

    # Führe die Vektorsuche durch und erhalte Dokumente
    documents = search_engine.vector_search(query_vector)
    return documents


def answer_question(question, documents, biolinkbert_model):
    """
    Verwendet BioLinkBERT, um die spezifischste Antwort aus den abgerufenen Dokumenten zu extrahieren.
    :param question: Die gestellte Frage
    :param documents: Liste von Dokumenten, die als relevant abgerufen wurden
    :param biolinkbert_model: Das geladene BioLinkBERT-Modell für QA
    :return: Die extrahierte Antwort
    """
    best_score = float('-inf')
    best_answer = None

    # Durchsuche jedes Dokument, um die beste Antwort zu finden
    for doc in documents:
        # Verwende BioLinkBERT, um eine Antwort aus dem Dokument zu extrahieren
        answer, score = biolinkbert_model.extract_answer(question, doc)

        # Aktualisiere die beste Antwort, wenn diese ein höheres Score hat
        if score > best_score:
            best_score = score
            best_answer = answer

    return best_answer


# Hauptfunktion, die alles zusammenführt
def main(question, search_engine, biolinkbert_model):
    """
    Hauptfunktion zur Abfrageverarbeitung und Antwortfindung.
    :param question: Die vom Benutzer gestellte Frage
    :param search_engine: Das Suchsystem
    :param biolinkbert_model: Das BioLinkBERT-Modell
    """
    # Schritt 1: Abrufen relevanter Dokumente
    documents = retrieve_documents(question, search_engine)

    # Schritt 2: Extrahiere die Antwort aus den Dokumenten
    answer = answer_question(question, documents, biolinkbert_model)

    return answer


# Beispieldaten und -modelle
search_engine = initialize_search_engine()
biolinkbert_model = load_biolinkbert_model()

# Beispielabfrage
question = "Was sind die Ursachen von Diabetes?"
answer = main(question, search_engine, biolinkbert_model)
print("Antwort:", answer)
