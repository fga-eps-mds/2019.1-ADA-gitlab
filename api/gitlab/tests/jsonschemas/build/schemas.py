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
    "type": "array",
    "properties": {
        "job_id": {"type": "integer"},
        "branch": {"type": "string"},
        "commit": {"type": "string"},
        "stage": {"type": "string"},
        "job_name": {"type": "string"},
        "status": {"type": "string"},
        "web_url": {"type": "string"},
        "pipeline_url": {"type": "string"}
    },
    "required": ["job_id", "branch", "commit", "stage", "job_name",
                 "status", "web_url", "pipeline_url"]
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

build_valid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "array",
    "properties": {
        "job_id": {"type": "integer"},
        "branch": {"type": "string"},
        "commit": {"type": "string"},
        "stage": {"type": "string"},
        "job_name": {"type": "string"},
        "status": {"type": "string"},
        "web_url": {"type": "string"},
        "pipeline_url": {"type": "string"}
    },
    "required": ["job_id", "branch", "commit", "stage", "job_name",
                 "status", "web_url", "pipeline_url"]
}

build_invalid_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status_code": {"type": "integer"}
    },
    "required": ["message", "status_code"]
}
