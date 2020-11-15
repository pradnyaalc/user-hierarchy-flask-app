import json
import jsonschema
from jsonschema import validate

class Collection:
    def validate_collection(self, collection, schema_path):
        with open(schema_path, 'r') as file:
            schema = json.load(file)
        try:
            for each in collection:
                validate(instance=each, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            err = "Given JSON data is InValid"
            print(err)
            return False
        return True

    def read_data_and_build_hierarchy(self, collection, schema_path):
       pass

    def get_subordinates(self):
        pass