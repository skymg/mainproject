from django.shortcuts import render
from django.http import JsonResponse
import json
import requests
from ncclient import manager
import xml.dom.minidom
import xmltodict
requests.packages.urllib3.disable_warnings()

# Create your views here.
def index(request):
    # return render(request,'indexTest.html')
    return  render(request, 'indexEmpty.html')
def cal(request):

    return render(request,"Cal.html")

def caltwonumber(request):
    valueA = request.POST['valueA']
    valueB = request.POST['valueB']
    res = int(valueA)+int(valueB)
    print(int(valueB))
    # return valueB+valueA
    return render(request,'result.html',context={'data':res})
def cisco(request):
    api_url = "https://192.168.56.101/restconf/data/ietf-interfaces:interfaces"

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

    return render(request,'cisco.html',context={'data':json_data})
    #print(json.dumps(response_json, indent=4))


    # 保存xml
def save_xml(reques):
    m = manager.connect(
        host="192.168.56.101",
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
    fo = open("save.xml1", "w")
    fo.write(xml_data)
    fo.close()
    with  open('save.xml1', 'r') as f:
        xmlStr = f.read()
        f.close()

    convertedDict = xmltodict.parse(xmlStr);
    jsonStr = json.dumps(convertedDict, indent=1);
    # return render(reques,'netconfig.html',context={"data":jsonStr})
    return render(reques, 'xmlToJson.html',context={"data":jsonStr})
    #return JsonResponse(json.loads(jsonStr),safe=False)
    # print(xml_data)

