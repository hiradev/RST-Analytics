from urllib.request import Request, urlopen
import json
from datetime import date, timedelta
import sys
from datetime import datetime

entities = {
    "Australia": '1591',
    "Bangladesh": '2010',
    "Cambodia": '305',
    "Hong Kong": '1594',
    "India": '1585',
    "Indonesia": '1539',
    "Japan": '1615',
    "Korea": '1562',
    "Mainland of China": '1613',
    "Malaysia": '1611',
    "Mongolia": '409',
    "Myanmar": '4',
    "Nepal": '112',
    "New Zealand": '1616',
    "Pakistan": '1603',
    "Philiphines": '1604',
    "Singapore": '1575',
    "Sri Lanka": '1623',
    "Taiwan": '1561',
    "Thailand": '1607',
    "Vietnam": '504',
}

stages = {
    "OP": "openings",
    "APP": "applied",
    "ACC": "an_accepted",
    "APD": "approved",
    "RE": "realized",
    "FI": "finished",
    "CO": "completed"
}

products = {
    "GV": [7],
    "GTa": [8],
    "GTe": [9],
}

types = {
    "Incoming": "i",
    "Outgoing": "o"
}

access_token = ""

def get(start, end):
    print("Generating from ", start, " to ", end);
    try:
        url = "https://analytics.api.aiesec.org/v2/applications/analyze.json?access_token="+access_token+"&start_date="+start+"&end_date="+end+"&performance_v3%5Boffice_id%5D=1623"
        page = urlopen(url)
        json_str = page.read()
        json_obj = json.loads(json_str)
    except():
        print("ERROR");
        return;

    res = {}

    for type, type_code in types.items():

        for product, product_codes in products.items():
            res[type_code+product] = {}

            for stage, stage_code in stages.items():
                res[type_code+product][stage] = {}
                res[type_code+product][stage]["RST"] = 0

                for entity, entity_code in entities.items():
                    res[type_code+product][stage][entity] = 0

                    for product_code in product_codes:

                        if(stage == "OP"):
                            tag = "open" + "_" + type_code + "_" "programme" + "_" + str(product_code)
                            val = val = json_obj[entity_code][tag]["doc_count"]
                        else:
                            tag = type_code + "_" + stage_code + "_" + str(product_code)
                            val = json_obj[entity_code][tag]["applicants"]["value"]

                        res[type_code+product][stage][entity] += val

                for product_code in product_codes:

                    if(stage == "OP"):
                        tag = "open" + "_" + type_code + "_" "programme" + "_" + str(product_code)
                        val = json_obj[tag]["doc_count"]
                    else:
                        tag = type_code + "_" + stage_code + "_" + str(product_code)
                        val = json_obj[tag]["applicants"]["value"]

                    res[type_code+product][stage]["RST"] += val


    for product, product_dict in res.items():

        f = open("full20211111.csv", "a")

        for stage, stage_dict in product_dict.items():
            vals = []

            for entity, value in stage_dict.items():
                vals.append(str(value))

            vals2 = ",".join(vals)

            txt = "{0},{1},{2},{3}\n"
            txt = txt.format(start, product, stage, vals2)
            #print(txt)
            f.write(txt)

        f.close()

        #print(start, "\t", product, "\t", "\t".join(p_vals))

access_token = sys.argv[1]
start_date = datetime.strptime(sys.argv[2], '%Y-%m-%d')
end_date = datetime.strptime(sys.argv[3], '%Y-%m-%d')
#delta = timedelta(days=6)
delta2 = timedelta(days=1)
while start_date <= end_date:
    s = start_date.strftime("%Y-%m-%d")
    start_date += delta2
    #e = start_date.strftime("%Y-%m-%d")
    #start_date += delta2
    get(s, s)
