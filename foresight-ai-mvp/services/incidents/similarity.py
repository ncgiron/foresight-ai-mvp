def find_similar_incidents(
    incidents,
    query
):
    query_words = set(query.lower().split())

    results = []

    MIN_SCORE = 3

    for incident in incidents:

        score = 0

        for field in [
            getattr(incident, "nf_type", ""),
            getattr(incident, "scenario", ""),
            incident.root_cause or "",
            incident.diagnosis or "",
        ]:

            words = set(field.lower().split())

            score += len(
                query_words.intersection(words)
            )

        if score >= MIN_SCORE:
            results.append(
                {
                    "incident_id": str(incident.id),
                    "score": score,
                    "root_cause": incident.root_cause,
                    "diagnosis": incident.diagnosis
                }
            )

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )[:3]