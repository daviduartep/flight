#cp geckodriver /usr/bin/geckodriver
#sudo pip install splinter
#sudo pip install selenium

import time
from splinter import Browser   
from selenium.webdriver.common.keys import Keys
import pickle

def GetKey(info):
    return info["id"] + "_" + info["start"] + "_" + info["end"]

def GetFlightInfo(f, miles=False):
    if not f.has_class("flight-info"):
        return None
    
    info = {}
    
    for x in f.find_by_tag("div"):
        if x.has_class("dep-time"):
            info["start"] = x.text
        if x.has_class("dep-air"):
            info["origin"] = x.text
        if x.has_class("arr-time"):
            info["end"] = x.text
        if x.has_class("arr-air"):
            info["destination"] = x.text
    
    for x in f.find_by_tag("span"):
        if x.has_class("fare-price"):
            if miles:
                if not info.has_key("miles"):
                    info["miles"] = x.text
            else:
                info["price"] = x.text
    for x in f.find_by_tag("button"):
        if "Voo" in x.value:
            info["id"] = x.value[4:]
            
    for x in ["origin", "destination", "start", "end", "price", "id"]:
        if miles and x == "price":
            x = "miles"
        if not info.has_key(x):
            return None
    
    return info

def GetDate(start_date, end_date):
    browser = Browser()
    f_map = {}

    browser.visit("https://www.voeazul.com.br/")
    #print browser.is_text_present("Comprar")
    #browser.fill('ticket-origin1', 'recife')
    browser.find_by_id('ticket-origin1').type("recife")
    time.sleep(1)
    active_web_element = browser.driver.switch_to_active_element()  
    active_web_element.send_keys(Keys.ENTER)
    browser.find_by_id('ticket-destination1').type("belo")
    time.sleep(1)
    active_web_element = browser.driver.switch_to_active_element()  
    active_web_element.send_keys(Keys.ENTER)  
    time.sleep(1)
    browser.find_by_id('ticket-departure1').type(start_date)
    browser.find_by_id('ticket-arrival1').type(end_date)
    browser.find_by_text("Buscar passagens")[0].click()
    
    for f in (browser.find_by_id("tbl-depart-flights").find_by_tag("tr") +
         browser.find_by_id("tbl-return-flights").find_by_tag("tr")):
        info = GetFlightInfo(f, False)
        if info != None:
            print info
            key = GetKey(info)
            if f_map.has_key(key):
                print "ID is not unique as was expected!"
            f_map[key] = info
    
    browser.find_by_id("availability_pointsFareType").click()
    time.sleep(5)
    
    for f in (browser.find_by_id("tbl-depart-flights").find_by_tag("tr") +
         browser.find_by_id("tbl-return-flights").find_by_tag("tr")):
        info = GetFlightInfo(f, True)
        if info != None:
            print info
            key = GetKey(info)
            if not f_map.has_key(key):
                print "ID for miles not present in price request!"
                continue
            f_map[key]["miles"] = info["miles"]
            
    browser.quit()
    return f_map



def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

dates_map = {}

for x in open("dates.in", "r").read().split("\n"):
    s = x.split(" ")
    if len(s) < 4:
        break
        
    dates_map[s[0] + "_" + s[1] + "_" + s[2] + "_" + s[3]] = GetDate(s[0], s[2])
    
save_obj(dates_map, "dates_map")

