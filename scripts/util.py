import re 
import json

valid_errors = {
    "tags_not_found": "The tag attribute was not present",
    "tags_set_none": "The tag attribute was found, but set to None",
    "tags_missing": "A required tag is missing. Please see error.info",
    "invalid_name_logical": "The logical name is invalid",
    "name_resource_invalid": "The resource name is invalid",
    "name_resource_set_none": "The name attribute was found, but set to None",
    "name_resource_not_found": "The name attribute was not present",
}

def load_json_from_file(fname):
    data = None
    with open(fname, "r") as f:
        data = json.load(f)
    return data

valid_errors = load_json_from_file("./errors.json")
attribute_names = load_json_from_file("attribute_names.json")

settings = load_json_from_file("config.json")
conf = settings["rules"]


class TerraformError:
    """
        Represents an error found while validating a Terraform plan.
    """
    def __init__(self, logical_name, error, info=None):
        # if error not in valid_errors:
        #     exit(f"INVALID ERROR {error} MUST BE IN {valid_errors.keys()}")

        self.logical_name = logical_name 
        self.error = error
        self.info = info

    def __str__(self):
        return f"{self.logical_name}: {self.error} - {self.info}"

def validate_resource(resource): 
    # Return True if no errors
    #       else return a list of TerraformErrors

    errors = []
    logical_name = resource['name']
    resource_type = resource['type']

    for rule_ in conf:
        ns = None

        rule = conf[rule_]

        if rule['namespace'] == 'root':
            ns = resource

            name = rule['name']

            if rule['type'] == 'regex':

                p = re.compile(rule['rule'])
                result = p.match(ns[name])

                if not result:
                    errors.append(TerraformError(logical_name, f"{rule['type']}_{rule['namespace']}_{rule['name']}"))



        elif rule['namespace'] == 'values':
            ns = resource['values']

            name = rule['name']



            if rule['type'] == 'regex':

                p = re.compile(rule['rule'])
    

                if resource_type in settings['alt_names']:
                    name = settings['alt_names'][resource_type][name]

                result = p.match(ns[name])

                if not result:
                    errors.append(TerraformError(logical_name, f"{rule['type']}_{rule['namespace']}_{rule['name']}"))

            elif rule['type'] == "keys_present":
                keys = ns[rule['name']]

                key_set = set(keys)

                key_set_required = set(rule['rule'])

                dff = key_set_required - key_set

                if len(dff) > 0:
                    errors.append(TerraformError(logical_name, f"{rule['type']}_{rule['namespace']}_{rule['name']}", dff))

    return errors



def validate_logical_name(logical_name):
    """
        Ensure the logical name of a Terraform resource is valid
    """ 

    p = re.compile(configuration['regex']['logical'])
    result = p.match(logical_name)
    
    if result is None:
        return TerraformError(logical_name, "invalid_name_logical", "invalid character found. logical name must match '^[a-zA-Z0-9_]+$'")

    return 1


def validate_resource_name(resource):
    """
        Ensure the logical name of a Terraform resource is valid

        :param resource_name: The name that has been given to a Terraform resource 
    """ 

    logical_name = resource['name']

    resource_type = resource['type']

    name_attribute = 'name'

    if resource_type in attribute_names:
        name_attribute = attribute_names[resource_type]['name']

    if name_attribute not in resource['values']:
        return TerraformError(logical_name, "name_resource_not_found")

    resource_name = resource['values'][name_attribute]

    if resource_name is None:
        return TerraformError(logical_name, "name_resource_set_none")

    p = re.compile(configuration['regex']['resource'])
    result = p.match(resource_name)
    
    if result is None:
        return TerraformError(logical_name, "name_resource_set_none", resource_name)
    return 1

def validate_tag_set(resource):
    """
        Validate a set of Terraform tags

        :param tags: dict of tag values
    """

    logical_name = resource['name']

    if 'tags' not in resource['values']:
        return TerraformError(logical_name, "tags_not_found")

    tags = resource['values']['tags']
    if tags is None:
        return TerraformError(logical_name, "tags_set_none")

    tags_required = ["Name", "Environment", "Project"]

    tags_found = []
    tags_missing = []

    valid = True 

    for tag_key in tags:
        tags_found.append(tag_key)

    tags_missing = set(tags_required) - set(tags_found)
    
    if len(tags_missing) > 0:
        return TerraformError(logical_name, "tags_missing", tags_missing)


    return valid 
