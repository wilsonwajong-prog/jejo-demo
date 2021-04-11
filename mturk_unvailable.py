#this module support the app (your app)
from helpers_mpux import is_assin

CONSTANTS = {}

def get_assin_from_str(s):
    #since you get the link from the form there's no need for regex parse
    #I dont really what the link looks like 
    global CONSTANTS
    try:
        b = s.split("_78%p3A")[1]
        if '&' in b:
            bb = b.split('&')
            b = bb[0]
        b = b[:10]
    except:
        return False, False, False
    else:
        if is_assin(b):
            region =None
            for reg in CONSTANTS["MARKETPLACES"]:
                if CONSTANTS["MARKETPLACES"][reg]['urlwww'] in s:
                    region = reg
                    break
            else:
                #me just pass cus i am not so sure
                pass
            keyword = None
            x= s.split("/")
            if len(x) >4:
                keyword = x[3].replace('-', ' ')
            return b, region, keyword
        else:
            return False, False, False

