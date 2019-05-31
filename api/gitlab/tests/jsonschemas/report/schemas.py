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

valid_branches_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Valid branches response schema",
    "type": "object",
    "properties": {
        "branches": {"type": "array"}
    },
    "required": ["branches"]
}

valid_commits_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Valid commits response schema",
    "type": "object",
    "properties": {
        "commits": {
            "last_commit": {
                "author_email": {"type": "string"},
                "author_name": {"type: string"},
                "authored_date": {"type": "string"},
                "title": {"type": "string"}
            },
            "number_of_commits": {"type": "integer"}
        }
    },
    "required": ["commits"]
}

valid_pipelines_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Valid pipelines response schema",
    "type": "object",
    "properties": {
        "pipeline": {
            "current_pipeline_id": {"type": "integer"},
            "current_pipeline_name": {"type": "string"},
            "failed_pipelines": {"type": "integer"},
            "number_of_pipelines": {"type": "integer"},
            "percent_succeded": {"type": "integer"},
            "recents_pipelines": {
                "last_30_days": {
                    "failed_pipelines": {"type": "integer"},
                    "number_of_pipelines": {"type": "integer"},
                    "percent_failed": {"type": "integer"},
                    "percent_succeded": {"type": "integer"},
                    "succeded_pipelines": {"type": "integer"}
                },
                "last_7_days": {
                    "failed_pipelines": {"type": "integer"},
                    "number_of_pipelines": {"type": "integer"},
                    "percent_failed": {"type": "integer"},
                    "percent_succeded": {"type": "integer"},
                    "succeded_pipelines": {"type": "integer"}
                }
            },
            "succeded_pipelines": {"type": "integer"}
        }
    },
    "required": ["pipeline"]
}

valid_project_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Valid cpmmits response schema",
    "type": "object",
    "properties": {
        "project": {
            "name": {"type": "string"},
            "web_url": {"type": "string"}
        }
    },
    "required": ["project"]
}
