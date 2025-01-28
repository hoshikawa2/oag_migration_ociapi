from typing import List, Dict, Any

from lxml import etree
import xml.etree.ElementTree as ET

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

def find_remote_host(find_element, filename):
    json_list = []
    json_list_items = []
    tree = etree.parse(filename)
    root = tree.getroot()
    namespaces = {    'xmlns': 'http://www.vordel.com/2005/06/24/entityStore',}
    found_elements = root.xpath(".//xmlns:entity[@type='RemoteHost']", namespaces=namespaces)
    if found_elements:
        for element in found_elements:
            if element != None:
                for value in element:
                    type_value = value.get("name")
                    text_value = value[0].text
                    if text_value != None:
                        text_value = text_value.replace("'", "").replace('\"', "")
                    if text_value == "\n\t\t" or text_value == "\n":
                        text_value = None
                    if type_value != None and text_value != None:
                        json_list_items.append({"fval": type_value, "value": text_value, })
        if json_list_items != None:
            json_list.append({"entity_type": "RemoteHost", "items": json_list_items})
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

def find_all_keys(filename):
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

            if json_list_items != None and json_list_items2 != None:
                json_list.append({"type": element_type, "keys": json_list_items, "properties": json_list_items2, "process": json_list_process})
    return json_list

def find_by_key(key_elements, key):
    json_list = []
    for key_element in key_elements:
        if key_element["properties"] != None:
            for item in key_element["properties"]:
                if item["fval"] != None:
                    if key_element["keys"] == key and item["fval"] == "name":
                        json_list.append(key_element)
    return json_list

def find_pk(element, filename):
    json_list = []
    json_list_items = []
    element_type = element.get("type")
    json_list_items = []
    if element != None:
        for value in element:
            type_value = value.get("type")
            if type_value == "CircuitContainer":
                value_reference = value
                while value_reference != None:
                    if value_reference.__len__() > 0:
                        key_value = value_reference[0].get("value")
                        json_list_items.append(key_value)
                        for value_item in value_reference:
                            value_reference = value_item
                    else:
                        value_reference = None

        if json_list_items != None:
            json_list.append({"keys": json_list_items})
    return json_list

def find_paths(find_type, filename):
    json_list = []
    tree = etree.parse(filename)
    root = tree.getroot()
    namespaces = {    'xmlns': 'http://www.vordel.com/2005/06/24/entityStore',}
    found_elements = root.xpath(".//xmlns:entity", namespaces=namespaces)
    if found_elements:
        for entityType in found_elements:
            json_list_items = []
            entity_type = None
            circuit_element = entityType.find('.//xmlns:key[@type="CircuitContainer"]/xmlns:key[@type="CircuitContainer"]/xmlns:key[@type="CircuitContainer"]/xmlns:id[@value="' + find_type + '"]', namespaces)
            if circuit_element != None:
                entity_type = circuit_element.attrib.get("value")
                for fval in entityType:
                    if fval != None:
                        for value in fval:
                            type_value = fval.get("name")
                            text_value = value.text
                            if text_value != None:
                                text_value = text_value.replace("'", "").replace('\"', "")
                            if text_value == "\n\t\t" or text_value == "\n":
                                text_value = None
                            if type_value != None and text_value != None:
                                json_list_items.append({"fval": type_value, "value": text_value, })
            if entity_type != None and json_list_items != None:
                json_list.append({"entity_type": entity_type, "items": json_list_items})

    return json_list

def find_next_process(properties):
    json_items = []
    for propertie in properties.get("properties"):
        if propertie.get("fval") == "successNode":
            json_items.append({"action": propertie.get("value")})
    return json_items

def find_process_by_key(key, filename):
    x = find_all_keys(filename)
    k = find_by_key(key_elements=x, key=key)
    find_processes(processes=k, filename=filename)
    return k

def find_all_processes(filename):
    x = find_all_keys(filename)
    return x

def find_processes(processes, filename):
    json_process = []
    json_items = []
    json_output = []
    x = find_all_keys(filename)
    for item in processes:
        properties = item["properties"]
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
                    json_items.append({"process": process[0], "action": propertie.get("value"), "next_action": find_next_process(item), "url": urlTemplate, "keys": item["keys"]})
    for process in json_process:
        print(process)
        # Find first
        for json_item in json_items:
            if process == json_item.get("process"):
                found = find_action(process, json_item.get("action"), json_items)
                next_action = find_next_action(process, json_item.get("action"), json_items)
                if not found:
                    action = json_item.get("action")
                    if json_item.get("url") != None:
                        action = action + " ---> " + json_item.get("url")
                    print("    " + action)
                    break

        while next_action != "":
            print("    " + next_action)
            next_action = find_next_action(process, next_action, json_items)

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

def make_mapping(filename, output_filename):
    json_list = find_all_processes(filename=filename)
    keys = []
    for item2 in json_list:
        last_key = []
        actual_key = item2["keys"]
        if actual_key == []:
            continue
        loop = False
        for i in keys:
            if i == actual_key:
                loop = True
        if loop:
            continue
        for item in json_list:
            if item["keys"] == []:
                continue
            if actual_key != item["keys"]:
                continue
            if last_key != item["keys"]:
                write_file(content="===========================================================", filename=output_filename)
                last_key = item["keys"]
                keys.append(last_key)
                str_key = "['"
                for k in last_key:
                    str_key = str_key + k + "','"
                str_key = str_key[:len(str_key) -2] + "']"
                write_file(content="  KEY: " + str_key, filename=output_filename)
            for property in item["properties"]:
                if (property["fval"] == "name"):
                    write_file(content="  -----------------------------------------------------------", filename=output_filename)
                    write_file(content="  " + property["value"] + ":", filename=output_filename)
                    for property2 in item["properties"]:
                        if property2["fval"] != "name":
                            write_file(content="       (" + item["type"] + "): " + property2["fval"] + ": " + property2["value"] + "   " + str(item["process"]), filename=output_filename)

def write_file(filename, content):
    path_name = "/Users/cristianohoshikawa/Dropbox/ORACLE/TIM/FY25/oag_varejo/"
    with open(path_name + filename, "a") as arquivo:
        arquivo.write(content + "\n")

make_mapping(filename="Export_OAG.xml", output_filename="OAG-mapping.txt")