from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from ncclient import manager
import xml.dom.minidom
import xmltodict
from django.shortcuts import redirect
from xml.dom.minidom import parse
requests.packages.urllib3.disable_warnings()


# Create your views here.
def index(request):
    # return render(request,'indexTest.html')
    # parsexml()
    return render(request, 'indexEmpty.html')


def templefile(request):
    return render(request,'templefile.html')

def cal(request):
    return render(request, "Cal.html")


def caltwonumber(request):
    valueA = request.POST['valueA']
    valueB = request.POST['valueB']
    res = int(valueA) + int(valueB)
    print(int(valueB))
    # return valueB+valueA
    return render(request, 'result.html', context={'data': res})


def cisco(request):
    api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces"

    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }

    basicauth = ("cisco", "cisco123!")

    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)

    response_json = resp.json()
    rs_e = response_json["ietf-interfaces:interfaces"]["interface"]
    print("============")
    print(rs_e)
    print("==========")
    json_data = json.dumps(response_json)
    print(type(json_data))
    # print(json.dumps(response_json))

    return render(request, 'cisco.html', context={'data': json_data})
    # print(json.dumps(response_json, indent=4))

    # 保存xml


def save_xml(request):
    m = manager.connect(
        host="192.168.56.102",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

    # define a NETCONF filter to get only the required data
    # w/o this filter the NETCONF GET operation will try to
    # return everything and will crash (aka. similar to 'debug all')
    # the filter defines that we want to get only data defined
    # in the ietf-interfaces model in the interfaces-state container
    netconf_filter = """
    <filter>
     <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """

    # using the NETCONF get method, get data:
    netconf_reply = m.get(filter=netconf_filter)
    # print("=========")
    # print(netconf_reply)
    # print("-----------")
    # converteJson = xmltodict.parse(netconf_reply,encoding='utf-8')
    # json_str = json.dumps(converteJson)
    # 将xml数据保存在本地
    xml_data = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    fo = open("save.xml", "w")
    fo.write(xml_data)
    fo.close()
    with  open('save.xml', 'r') as f:
        xmlStr = f.read()
        f.close()

    convertedDict = xmltodict.parse(xmlStr);
    jsonStr = json.dumps(convertedDict);
    # back_msg = {"name": "xiaoming", 'age': 123}
    # return render(reques,'netconfig.html',context={"data":jsonStr})
    print(jsonStr)
    return render(request, 'xmlToJson.html', context={"data": jsonStr})
    # return JsonResponse(json.dumps(back_msg),safe=False)
    # print(xml_data)

# add new interface
def add_interface(request):
    api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }

    basicauth = ("cisco", "cisco123!")

    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback778",
            "description": "apple",
            "type": "iana-if-type:softwareLoopback",

            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "99.99.99.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    resp = requests.post(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
    else:
        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
    return render(request, 'addInterface.html', context={"data": json.dumps(yangConfig)})


def load_deletp_page(request):
    return render(request, 'get_interfaceName.html')


# get interface name from html input form
# delete interface by interfacename
def get_interface_name(request):
    interfaceName = request.POST.get('interface_name')
    api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces/interface="+interfaceName
    # api_url =api_url+"aaa"
    # print(api_url)
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }

    basicauth = ("cisco", "cisco123!")

    resp = requests.delete(api_url, auth=basicauth, headers=headers, verify=False)
    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        # add interface success redirect to "show_all_interface"
        return redirect('/show_all_interface/')
    else:
        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
    print(type(interfaceName))
    #
    return render(request, 'show_all_interface.html')

# show_all_interface
def show_all_interface(request):
    m = manager.connect(
        host="192.168.56.102",
        port=830,
        username="cisco",
        password="cisco123!",
        hostkey_verify=False
    )

    # define a NETCONF filter to get only the required data
    # w/o this filter the NETCONF GET operation will try to
    # return everything and will crash (aka. similar to 'debug all')
    # the filter defines that we want to get only data defined
    # in the ietf-interfaces model in the interfaces-state container
    netconf_filter = """
    <filter>
     <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
    </filter>
    """
    # using the NETCONF get method, get data:
    netconf_reply = m.get(filter=netconf_filter)
    # 将xml数据保存在本地
    xml_data = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    fo = open("all_interface.xml", "w")
    fo.write(xml_data)
    fo.close()
    with  open('all_interface.xml', 'r') as f:
        xmlStr = f.read()
        # print(xmlStr)
        f.close()

    convertedDict = xmltodict.parse(xmlStr);
    data = json.dumps(convertedDict);
    return render(request, 'show_all_interface.html', context={"data": xmlStr})

#interface form
def add_interFaceFromTable(request):
    return render(request,'add_interface_form.html')

# get interface information from html form
def add_inter_with_form(request):
    interfaceName = request.POST.get('interface_name')
    interfaceDescription = request.POST.get('interface_description')
    interfaceType = request.POST.get('interface_type')
    interfaceIP = request.POST.get('interface_ip')
    print(interfaceName,interfaceDescription,interfaceType,interfaceIP)

    api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces"
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"
               }

    basicauth = ("cisco", "cisco123!")
    yangConfig = {
        'ietf-interfaces:interface': {'ietf-ip:ipv6': {}, 'enabled': False, 'type': interfaceType,
                                      'name': interfaceName,
                                      'ietf-ip:ipv4': {'address': [{'ip': interfaceIP, 'netmask': '255.255.255.0'}]},
                                      'description': interfaceDescription}}

    # print("4444444444")
    # print(yangConfig)
    # print("444444")
    resp = requests.post(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return redirect('/show_all_interface/')
    else:
        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))
    return render(request, 'show_all_interface.html')

# parse xml file
def parsexml(request):
    dom1 = parse('all_interface.xml')
    data = dom1.documentElement
    interfaces = data.getElementsByTagName('interface')
    interfaceNameList = []
    for interface in interfaces:
        interfaceName = interface.getElementsByTagName('name')[0].childNodes[0].nodeValue
        interfaceNameList.append(interfaceName)
    with open('interface_name.txt','w') as f:
        f.write(str(interfaceNameList))
        f.close()
    return render(request,'show_interface_name.html',{"data":interfaceNameList})
    # print(interfaceNameList)


# get url parameter from <a> table
def edit_show(request):
    name = request.GET.get('name')
    print(name)
    data = get_one_interface_information(name)
    dict = {"Name": "Zara", "Age": 7, "Class": "First"}
    # data = json.loads(data)
    # return JsonResponse({"data":data},safe=False,json_dumps_params={'ensure_ascii':False})

    return render(request,'detal_interface_byName.html',context={"data":data})
# get interface by interfaceName
def get_one_interface_information(interfacename):
    api_url = "https://192.168.56.102/restconf/data/ietf-interfaces:interfaces/interface="+interfacename
    headers = {
        "Accept": "application/yang-data+json",
        "Content-type": "application/yang-data+json"
    }
    basicauth = ("cisco", "cisco123!")
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = resp.json()
    data = json.dumps(response_json)
    return data