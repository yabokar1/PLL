student_id_recognizer = {
        "name": "student_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "student_id_pattern", "regex": r"\b\d{9}\b", "score": 0.9}
        ],
        "context": ["student", "id", "number"],
        "supported_entity": "STUDENT_ID"
    }


faculty_id_recognizer = {
        "name": "faculty_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "faculty_id_pattern", "regex": r"\b1\d{8}\b", "score": 0.85}
        ],
        "context": ["faculty", "id", "number"],
        "supported_entity": "FACULTY_ID"
    }


sin_recognizer = {
        "name": "sin_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "sin_pattern", "regex":r"\b\d{3}-\d{3}-\d{3}\b", "score": 0.8}
        ],
        "context": ["social", "insurance", "number", "SIN"],
        "supported_entity": "SIN"
    }


medical_records_recognizer = {
        "name": "medical_records_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "medical_records_pattern", "regex": r"\b\d{6,10}\b", "score": 0.7}
        ],
        "context": ["medical", "record", "number"],
        "supported_entity": "MEDICAL_RECORD"
    }

passport_id_recognizer = {
        "name": "passport_id_pattern",
        "supported_language": "en",
        "patterns": [
            {"name": "passport_id_pattern", "regex": r"\b[A-Z]{1,2}\d{5,9}\b", "score": 0.8}
        ],
        "context": ["passport", "id", "number"],
        "supported_entity": "PASSPORT_ID"
}

