from memory import classifier, short_term, sqlite, summarizer

def update_memory(inputs):

    output = ""

    for input in inputs:
        if input["input_type"].startswith("mic_input"):
            validated = classifier.classify_transcription_relevance(input["content"])
            if validated["priority"] < 0.5 or validated["confidence"] < 0.5:
                print("im herhe")
                continue
            summarized = summarizer.long_term_summarizer(input["content"]) 
            output = summarized["summary"]
            sqlite.add_to_db(summarized["category"], summarized["summary"], summarized["importance"])
            if len(short_term.working_memory["recent_events"]) >= 20:
                short_term.working_memory["recent_events"].pop(0)
            short_term.working_memory["recent_events"].append(summarized["summary"])


    return output 
