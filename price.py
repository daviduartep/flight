import pickle

origin_airport = "REC"
destination_airport = "CNF"

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def MilesToPrice(miles_string):
    return int((float(miles_string.replace(".", ""))/10000.0)*250.0)

def FormatPrice(string_price):
    return float(string_price.replace(".", "").split(",")[0])*0.83

def GetBestPrice(date, date_info):
    start_limit = int(date.split("_")[1])
    end_limit = int(date.split("_")[3])
    end_limit = 25
    
    origin = []
    destination = []
    
    for k in date_info:     
        miles_price = MilesToPrice(date_info[k]["miles"])
        price = FormatPrice(date_info[k]["price"])
        date_info[k]["adjusted_price"] = round(min(price, miles_price), 0)
        date_info[k]["type"] = "miles"
        if price < miles_price:
            date_info[k]["type"] = "price"
        if date_info[k]["origin"] == origin_airport:   
            if int(date_info[k]["start"].split(":")[0]) < start_limit:
                continue
            origin.append(date_info[k])
        else:
            if int(date_info[k]["end"].split(":")[0]) > end_limit:
                continue
            destination.append(date_info[k])
        date_info[k]["ratio"] = round(price/miles_price, 2)
    
    origin = sorted(origin, key = lambda x : x["adjusted_price"])
    destination = sorted(destination, key = lambda x : x["adjusted_price"])
    
    print "Best price: %d" % (origin[0]["adjusted_price"] + destination[0]["adjusted_price"])
    
    for i in range(0,min(7, len(origin))):
        print (origin_airport, origin[i]["start"], origin[i]["end"], 
            origin[i]["adjusted_price"], origin[i]["type"], origin[i]["ratio"])
    
    for i in range(0,min(7, len(destination))):
        print (destination_airport, destination[i]["start"], destination[i]["end"], 
            destination[i]["adjusted_price"], destination[i]["type"], destination[i]["ratio"])
        
    

dates_map = load_obj("dates_map")

for k in dates_map:
    print k
    GetBestPrice(k, dates_map[k])
    print ""
