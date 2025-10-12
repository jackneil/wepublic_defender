import json, importlib.util
path = r"c:\Github\wepublic_defender\wepublic_defender\models\legal_responses.py"
spec = importlib.util.spec_from_file_location('legal_responses', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore
OpposingCounselReview = getattr(mod, 'OpposingCounselReview')
schema = OpposingCounselReview.model_json_schema()
print(json.dumps(schema, indent=2))
