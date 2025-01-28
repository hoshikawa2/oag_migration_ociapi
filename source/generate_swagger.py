import json
import xml.etree.ElementTree as ET
from lxml import etree

def find_pk(element):
    json_list = []
    json_list_items = []
    element_type = element.get("type")
    json_list_items = []
    json_list_process = []
    if element != None:
        for value in element:
            type_value = value.get("type")
            name_value = value.get("name")
            if type_value == "CircuitContainer":
                value_reference = value
                while value_reference != None:
                    if value_reference.__len__() > 0:
                        if value.get("type") == "CircuitContainer":
                            process = None
                            key_value = value_reference[0].get("value")
                            if value_reference.get("type") == "FilterCircuit":
                                process = key_value
                                key_value = None
                            if key_value != None:
                                json_list_items.append(key_value)
                            if process != None:
                                json_list_process.append(process)
                        for value_item in value_reference:
                            value_reference = value_item
                    else:
                        value_reference = None
            if name_value == "filterCircuit":
                value = value[0]
                value = value[0]
                value_reference = value
                while value_reference != None:
                    if value_reference.__len__() > 0:
                        if value.get("type") == "CircuitContainer":
                            process = None
                            key_value = value_reference[0].get("value")
                            if value_reference.get("type") == "FilterCircuit":
                                process = key_value
                                key_value = None
                            if key_value != None:
                                json_list_items.append(key_value)
                            if process != None:
                                json_list_process.append(process)
                        for value_item in value_reference:
                            value_reference = value_item
                    else:
                        value_reference = None

        if json_list_items != None:
            json_list.append({"keys": json_list_items, "process": json_list_process})
    return json_list

def get_circuitContainer(value, filter):
    json_list_items = []
    json_list_process = []
    if value.__len__() > 0:
        if value[0].__len__() > 0:
            value_reference = value[0][0]
            while value_reference != None:
                if value_reference.__len__() > 0:
                    if value_reference.get("type") == filter:
                        key_value = value_reference[0].get("value")
                        process = None
                        if value_reference.get("type") == filter:
                            process = key_value
                            key_value = None
                        if key_value != None:
                            json_list_items.append(key_value)
                        if process != None:
                            json_list_process.append(process)
                    for value_item in value_reference:
                        value_reference = value_item
                else:
                    value_reference = None
    return json_list_process

def find_keys(find_element, filename):
    json_list = []
    json_list_items = []
    tree = etree.parse(filename)
    root = tree.getroot()
    namespaces = {    'xmlns': 'http://www.vordel.com/2005/06/24/entityStore',}
    found_elements = root.xpath(".//xmlns:entity", namespaces=namespaces)
    if found_elements:
        for element in found_elements:
            element_type = element.get("type")
            json_list_items = []
            json_list_process = []
            if element != None:
                for value in element:
                    type_value = value.get("type")
                    if type_value == "CircuitContainer":
                        value_reference = value
                        while value_reference != None:
                            if value_reference.__len__() > 0:
                                if value.get("type") == "CircuitContainer":
                                    key_value = value_reference[0].get("value")
                                    process = None
                                    if value_reference.get("type") == "FilterCircuit":
                                        process = key_value
                                        key_value = None
                                    if key_value != None:
                                        json_list_items.append(key_value)
                                    if process != None:
                                        json_list_process.append(process)
                                for value_item in value_reference:
                                    value_reference = value_item
                            else:
                                value_reference = None

                json_list_items2 = []
                for value in element:
                    type_value = value.get("name")
                    next_process = []
                    if value.__len__() > 0:
                        if type_value == "successNode":
                            next_process = get_circuitContainer(value, "CircuitDelegateFilter")
                        if next_process.__len__() > 0:
                            text_value = next_process[0]
                        else:
                            text_value = value[0].text
                        if text_value != None:
                            text_value = text_value.replace("'", "").replace('\"', "")
                        if text_value == "\n\t\t" or text_value == "\n":
                            text_value = None
                        if type_value != None and text_value != None:
                            json_list_items2.append({"fval": type_value, "value": text_value, })

                found = False
                index_list = 0
                match_list = 0
                while index_list < json_list_items.__len__():
                    if index_list < find_element.__len__():
                        if json_list_items[index_list] == find_element[index_list]:
                            match_list = match_list + 1
                    index_list = index_list + 1

            if json_list_items != None and json_list_items2 != None and match_list == find_element.__len__():
                json_list.append({"type": element_type, "keys": json_list_items, "properties": json_list_items2, "process": json_list_process})
    return json_list

def find_EnvironmentalizedFieldString(find_element, filename):
    json_list = []
    json_list_items = []
    tree = etree.parse(filename)
    root = tree.getroot()
    namespaces = {    'xmlns': 'http://www.vordel.com/2005/06/24/entityStore',}
    found_elements = root.xpath(".//xmlns:entity[@type='EnvironmentalizedFieldString']", namespaces=namespaces)
    if found_elements:
        for element in found_elements:
            element_type = element.get("type")
            if element != None:
                for value in element:
                    type_value = value.get("type")
                    if type_value == "EnvironmentalizedEntities":
                        value_reference = value
                        for key in value_reference:
                            if key.__len__() > 0:
                                if key.get("type") == "EnvironmentalizedEntity":
                                    if key.__len__() > 0:
                                        if key[0].get("field") == "entityPk":
                                            key_value = key[0].get("value")

                                            found = False
                                            index_list = 0
                                            match_list = 0
                                            while index_list < find_element.__len__():
                                                if "'" + find_element[index_list] + "'" in key_value:
                                                    match_list = match_list + 1
                                                index_list = index_list + 1

                                            if match_list == find_element.__len__():
                                                json_list_items = []
                                                for value1 in element:
                                                    type_value = value1.get("name")
                                                    text_value = value1[0].text
                                                    if text_value != None:
                                                        text_value = text_value.replace("'", "").replace('\"', "")
                                                    if text_value == "\n\t\t" or text_value == "\n":
                                                        text_value = None
                                                    if type_value != None and text_value != None:
                                                        json_list_items.append({"fval": type_value, "value": text_value, })
                            else:
                                value_reference = None

        if json_list_items.__len__() > 0:
            json_list.append({"type": "EnvironmentalizedFieldString", "keys": find_element, "properties": json_list_items})
    return json_list

def find_url(pk, filename):
    urlTemplate = ""
    if pk.__len__() > 0:
        pk_list = pk[0].get("keys")
        if pk_list.__len__() > 0:
            url_list = find_keys(pk_list, filename)
            for item in url_list:
                if item["type"] == "ConnectToURLFilter":
                    for subitem in item["properties"]:
                        if subitem["fval"] == "url":
                            urlTemplate = subitem["value"]
            env_list = find_EnvironmentalizedFieldString(find_element=pk_list, filename=filename)
            check_url_exists = False
            env_url = ""
            if env_list.__len__() > 0:
                for env_item in env_list[0]["properties"]:
                    if env_item["fval"] == "entityFieldName" and env_item["value"] == "url":
                        check_url_exists = True
                    if env_item["fval"] == "value":
                        env_url = env_item["value"]
                if  check_url_exists and env_url != "":
                    urlTemplate = env_url
    return urlTemplate

def find_urls(find_type, find_element, filename):
    json_list = []
    tree = etree.parse(filename)
    root = tree.getroot()
    namespaces = {    'xmlns': 'http://www.vordel.com/2005/06/24/entityStore',}
    found_elements = root.xpath(".//xmlns:entity[@type='" + find_type + "']", namespaces=namespaces)
    if found_elements:
        for element in found_elements:
            # print(element.tag)
            value_element = element.find('.//xmlns:fval[@name="' + find_element + '"]/xmlns:value', namespaces)
            circuit_element = element.find('.//xmlns:key[@type="CircuitContainer"]/xmlns:key[@type="CircuitContainer"]/xmlns:key[@type="CircuitContainer"]/xmlns:key[@type="CircuitContainer"]/xmlns:id', namespaces)
            if circuit_element != None:
                circuit = circuit_element.get("value")
            if value_element != None:
                value = value_element.text
            if value_element != None and circuit != None:
                json_list.append({"find_type": find_type, "element": find_element, "value": value, "key": circuit})
    return json_list

def find_next_process(properties):
    json_items = []
    for propertie in properties.get("properties"):
        if propertie.get("fval") == "successNode":
            json_items.append({"action": propertie.get("value")})
    return json_items

def find_processes(processes, filename):
    json_process = []
    json_items = []
    json_output = []
    for item in processes:
        properties = item["properties"]
        keys = item["keys"]

        process = item["process"]
        urlTemplate = None
        for propertie in properties:
            if propertie.get("fval") == "attributeValue":
                if propertie.get("value") != None:
                    urlTemplate = propertie.get("value")

            if propertie.get("fval") == "name":
                if process.__len__() == 0:
                    json_process.append(propertie.get("value"))
                else:
                    json_items.append({"process": process[0], "action": propertie.get("value"), "next_action": find_next_process(item), "url": urlTemplate})
    for process in json_process:
        json_output.append("  #" + process)
        # Find first
        next_action = ""
        for json_item in json_items:
            if process == json_item.get("process"):
                found = find_action(process, json_item.get("action"), json_items)
                next_action = find_next_action(process, json_item.get("action"), json_items)
                if not found:
                    action = json_item.get("action")
                    if json_item.get("url") != None:
                        action = action + " ---> " + json_item.get("url")
                    json_output.append("  #    " + action)
                    break

        while next_action != "":
            json_output.append("  #    " + next_action)
            next_action = find_next_action(process, next_action, json_items)
    return json_output

def find_action(process, action, json_items):
    found = False
    for json_item_next in json_items:
        if process == json_item_next["process"]:
            if json_item_next["next_action"].__len__() > 0:
                if action == json_item_next["next_action"][0]["action"]:
                    found = True
    return found

def find_next_action(process, action, json_items):
    next_action = ""
    for json_item_next in json_items:
        if process == json_item_next.get("process"):
            if json_item_next["next_action"].__len__() > 0:
                if action == json_item_next["action"]:
                    next_action =  json_item_next["next_action"][0]["action"]
    return next_action

def parse(filename):
    json_list = []
    tree = ET.parse(filename)
    root = tree.getroot()
    type = ""
    uriTemplate = None
    httpMethod = None
    hostName = None
    APIName = None
    method = None
    urlTemplate = None

    for entityType in root:

        for fval in entityType:
            if fval.get("name") == "name":
                for value in fval:
                    APIName = value.text
            if fval.get("name") == "httpMethod":
                for value in fval:
                    httpMethod = value.text
            if fval.get("name") == "hostname":
                for value in fval:
                    hostName = value.text
            if fval.get("name") == "method":
                for value in fval:
                    method = value.text
            if fval.get('name') == "uriTemplate":
                for value in fval:
                    type = "uriTemplate"
                    uriTemplate = value.text
            if fval.get('name') == "uriprefix":
                for value in fval:
                    type = "uriPrefix"
                    uriTemplate = value.text

        pk = find_pk(entityType)

        if urlTemplate == None:
            urlTemplate = ""
        if uriTemplate != None and {"apiName": APIName, "type": type, "uriTemplate": uriTemplate, "httpMethod": httpMethod, "host": urlTemplate, "pk": pk} not in json_list:
            json_list.append({"apiName": APIName, "type": type, "uriTemplate": uriTemplate, "httpMethod": httpMethod, "host": urlTemplate, "pk": pk})
            type = ""
            uriTemplate = None
            httpMethod = None
            hostName = None
            APIName = None
            method = None
            urlTemplate = None
            pk = []

    return json_list

def processing_paths(json_list):
    pairs = []
    json_duplicated_list = json_list
    for item in json_list:
        if item["uriTemplate"] == None:
            continue
        pair_found = find_pairs(item, json_duplicated_list)
        if {"api": pair_found} not in pairs:
            pairs.append({"api": pair_found})
    return pairs

#Add all the attributes for Swagger
def find_pairs(item_original, json_list):
    results = []
    final_result = None
    for item in json_list:
        if item_original["uriTemplate"] != item["uriTemplate"]:
            splited_path = item_original["uriTemplate"].split("/")
            splited_item = item["uriTemplate"].split("/")
            nivel = 0
            paths = []
            for splited_comparison in splited_path:
                try:
                    if splited_comparison == splited_item[nivel]:
                        if splited_comparison != "":
                            paths.append(splited_comparison)
                        nivel = nivel + 1
                    else:
                        break
                except:
                    break
            if {"apiName": item_original["apiName"],"path": item_original["uriTemplate"],"paths": paths, "method": item_original["httpMethod"], "host": item_original["host"], "pk": item_original["pk"]} not in results:
                results.append({"apiName": item_original["apiName"],"path": item_original["uriTemplate"],"paths": paths, "method": item_original["httpMethod"], "host": item_original["host"], "pk": item_original["pk"]})
    max = 0
    for item in results:
        counting = item["paths"].__len__()
        if counting > max:
            final_result = item
            max = counting
    return final_result


# Add all attributes for Swagger
def divide_paths(root):
    list_paths = root
    list_result = []
    for item in list_paths:
        counting = 0
        path_prefix = []
        path = []
        interrupt = False
        if item["api"] == None:
            continue
        all_path = item["api"]["path"].split("/")
        if all_path.__len__() > 0:
            all_path.pop(0)
        for subitem in all_path:
            try:
                if "{" in subitem and path_prefix.__len__() > 1:
                    path.append(all_path[counting - 1])
                    path_prefix.pop(counting - 1)
                    path.append(subitem)
                    counting = counting + 1
                    interrupt = True
                    continue
                if (counting < all_path.__len__() - 1) and not interrupt:
                    path_prefix.append(subitem)
                else:
                    path.append(subitem)
                counting = counting + 1
            except:
                continue
        if path_prefix != None:
            # path_prefix.pop(0)
            list_result.append({"apiName": item["api"]["apiName"], "uriTemplate": item["api"]["path"], "paths": item["api"]["paths"], "path_prefix": path_prefix, "path": path, "method": item["api"]["method"], "host": item["api"]["host"], "pk": item["api"]["pk"]})
        list_result = sorted(list_result, key=lambda k: [k['path_prefix'], k['path'], k['host']], reverse=True)
    return list_result

def join_paths(json_list):
    str = ""
    for item in json_list:
        str = str + "/" + item
    return str

def remove_http(value):
    returned = []
    if value != None and value != "":
        if "https://" in value:
            returned.append("https")
            returned.append(value.replace("https://", ""))
        else:
            if "http://" in value:
                returned.append("http")
                returned.append(value.replace("http://", ""))
            else:
                returned.append("")
                returned.append(value)
        if returned == None:
            returned.append("")
            returned.append(value)
    else:
        returned.append("")
        returned.append("localhost")
    return returned

def make_file(filename, json_list):
    template = []
    title = filename.split(".")[0]

    host = ""
    path_prefix = ""
    paths = ""

    for item in json_list:
        if item == None or item == []:
            continue
        if host != item["host"] or item["path_prefix"] != path_prefix:
            host = item["host"]
            host_schema = remove_http(host)
            template.append('swagger: "2.0"')
            template.append('info:')
            template.append('  title: ' + title)
            template.append('  description: Migrated from Oracle API Gateway.')

            if item["pk"][0]["keys"] != []:
                json_list_keys = find_keys(find_element=item["pk"][0]["keys"], filename=filename)
                if json_list_keys.__len__() > 0:
                    if json_list_keys[0]["keys"].__len__() > 0:
                        list_processes = find_processes(filename=filename, processes=json_list_keys)
                        if list_processes != None:
                            if list_processes.__len__() > 0:
                                for processed in list_processes:
                                    template.append(processed)

            template.append('  version: 1.0.0')
            template.append('host: ' + host_schema[1])

            if item["path_prefix"] != path_prefix:
                path_prefix = item["path_prefix"]
                template.append('basePath: ' + join_paths(path_prefix))
                template.append('schemes:')
                template.append('  - ' + host_schema[0])
                template.append('paths:')

        paths = join_paths(item["path"])

        apiName = "-"
        try:
            apiName = item["apiName"]
            if apiName == None:
                apiName = "-"
        except:
            apiName = "-"

        template.append('  ' + paths + ':')
        if item["method"] != "*":
            if item["method"] != None:
                template.append('    ' + item["method"].lower() + ':')
            else:
                template.append('    METHOD NOT FOUND:')
            template.append('      summary: ' + apiName)
            template.append('      description: ' + apiName)
            template.append('      produces:')
            template.append('        - application/json')
            template.append('      responses:')
            template.append('        200:')
            template.append('          description: OK')
            template = create_swagger_parameters(paths, template)
            if item["method"] != None:
                template = create_operation(item["method"].lower(), paths, template)
            else:
                template = create_operation("all_scope", paths, template)
        else:
            template.append('    ' + "get" + ':')
            template.append('      summary: ' + apiName)
            template.append('      description: ' + apiName)
            template.append('      produces:')
            template.append('        - application/json')
            template.append('      responses:')
            template.append('        200:')
            template.append('          description: OK')
            template = create_swagger_parameters(paths, template)
            template = create_operation("get", paths, template)
            template.append('    ' + "post" + ':')
            template.append('      summary: ' + apiName)
            template.append('      description: ' + apiName)
            template.append('      produces:')
            template.append('        - application/json')
            template.append('      responses:')
            template.append('        200:')
            template.append('          description: OK')
            template = create_swagger_parameters(paths, template)
            template = create_operation("post", paths, template)
            template.append('    ' + "put" + ':')
            template.append('      summary: ' + apiName)
            template.append('      description: ' + apiName)
            template.append('      produces:')
            template.append('        - application/json')
            template.append('      responses:')
            template.append('        200:')
            template.append('          description: OK')
            template = create_swagger_parameters(paths, template)
            template = create_operation("put", paths, template)
            template.append('    ' + "delete" + ':')
            template.append('      summary: ' + apiName)
            template.append('      description: ' + apiName)
            template.append('      produces:')
            template.append('        - application/json')
            template.append('      responses:')
            template.append('        200:')
            template.append('          description: OK')
            template = create_swagger_parameters(paths, template)
            template = create_operation("delete", paths, template)

    counting = 0
    f = title + "_" + str(counting) + ".yaml"
    for item in template:
        if item == 'swagger: "2.0"':
            f = title + "_" + str(counting) + ".yaml"
            counting = counting + 1
        print(item)
        #write_file(f, item)

def write_file(filename, content):
    path_name = "/Users/cristianohoshikawa/Desktop/"
    with open(path_name + filename, "a") as arquivo:
        arquivo.write(content + "\n")

def make_structure_file(filename, json_list):
    template = []
    title = filename.split(".")[0]

    host = ""
    path_prefix = ""
    paths = ""

    for item in json_list:
        if host != item["host"] or item["path_prefix"] != path_prefix:
            host = item["host"]
            host_schema = remove_http(host)

            template.append("----------------------")

            if item["pk"][0]["keys"] != []:
                json_list_keys = find_keys(find_element=item["pk"][0]["keys"], filename=filename)
                if json_list_keys.__len__() > 0:
                    if json_list_keys[0]["keys"].__len__() > 0:
                        list_processes = find_processes(filename=filename, processes=json_list_keys)
                        if list_processes != None:
                            if list_processes.__len__() > 0:
                                for processed in list_processes:
                                    template.append(processed)

            if item["path_prefix"] != path_prefix:
                path_prefix = item["path_prefix"]
                template.append('basePath: ' + join_paths(path_prefix))
                template.append('paths:')

        paths = join_paths(item["path"])

        apiName = "-"
        try:
            apiName = item["apiName"]
            if apiName == None:
                apiName = "-"
        except:
            apiName = "-"

        if item["method"] != None:
            template.append('  ' + item["method"].lower() + ' ' + paths + ':')

    counting = 0
    f = title + "_" + str(counting) + ".yaml"
    for item in template:
        if item == 'swagger: "2.0"':
            f = title + "_" + str(counting)
            counting = counting + 1
        #print(item)
        write_file(f, item)

def create_swagger_parameters(paths, template):
    splited_paths = paths.split("/")
    first_tag_parameters = False
    for subpaths in splited_paths:
        if "{" in subpaths:
            subpath_to_print = subpaths.replace("{", "").replace("}", "")
            if not first_tag_parameters:
                template.append('      parameters:')
                first_tag_parameters = True
            template.append('        - name: ' + subpath_to_print)
            template.append('          in: path')
            template.append('          description: ')
            template.append('          required: true')
            template.append('          type: string')
    return template

def create_operation(method, paths, template):
    template.append('      operationId: ' + method + "_" + paths.replace("{", "").replace("}", "").replace("/", ""))
    return template

def parse_oag(filename):
    paths = parse(filename)
    paths = processing_paths(paths)
    paths = divide_paths(paths)
    #make_structure_file(filename, paths)
    make_file(filename, paths)

# EXECUTION
filename = "InternetCorp.xml"
parse_oag(filename)