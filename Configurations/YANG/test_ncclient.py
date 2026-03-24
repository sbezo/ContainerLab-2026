from ncclient import manager

router = {
    "host": "10.208.116.71",
    "port": 2312,
    "username": "clab",
    "password": "clab@123",
    "hostkey_verify": False
}

with manager.connect(**router) as m:
    print("Connected!")

    # Get running config (filtered)
    config = m.get_config(source="running")
    # print(config.xml)

    
    #for cap in m.server_capabilities:
    #    print(cap)
    


    filter_xml = """
    <filter>
      <system xmlns="http://openconfig.net/yang/system"/>
    </filter>
    """

    reply = m.get(filter_xml)
    print(reply.xml)