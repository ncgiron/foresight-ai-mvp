def find_similar_incidents(
    incidents,
    query
):
    query = query.lower()

    results = []

    for incident in incidents:

        score = 0

        if incident.root_cause and query in incident.root_cause.lower():
            score += 5

        if incident.diagnosis and query in incident.diagnosis.lower():
            score += 3

        if score > 0:
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
    )