ping_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["message", "status"]
}

valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "sha": {"type": "string"},
        "ref": {"type": "string"},
        "status": {"type": "string"},
        "web_url": {"type": "string"}
    },
    "required": ["id", "sha", "ref", "status", "web_url"]
}

unauthorized_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status_code": {"type": "integer"}
    },
    "required": ["status_code"]
}

invalid_project_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status_code": {"type": "integer"}
    },
    "required": ["status_code"]
}

report_valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "branches": {"name": {
                        "type": "array"}},
        "commits":  {"last_commit": {
                        "type": "array"},
                     "number_of_commits": {
                         "type": "integer"}
                     }
    },
    "required": ["branches", "commits"]
}

report_invalid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    },
    "required": ["message", "status_code"]
}

report_invalid_project_id_schema = {
       "$schema": "http://json-schema.org/draft-04/schema#",
       "title": "User response schema",
       "type": "object",
       "properties": {
            "status_code": {"type": "integer"}
        },
       "required": ["status_code"]
}
