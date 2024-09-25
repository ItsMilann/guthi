app_config = {
    "app_name": "template",
    "content_type": False,
    "models": {
        "TemplateCategory": {
            "title": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 255
            },
            "icon": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 255
            }
        },
        "TemplateDocument": {
            "type": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 255,
                "choices": "(('personal', 'personal'), ('sifarish', 'sifarish'))"
            },
            "title": {
                "datatype": "CharField",
                "blank": True,
                "null": True,
                "max_length": 255,
            }
        }
    }
}
