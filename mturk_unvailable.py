#this module support the app (your app)
import re

CONSTANTS = {}
#I implement my own is_asin function 
def is_assin(a):
    count = 0
    for n in a:
        try:
            int(n)
            count = count + 1
        except ValueError:
            continue
    if 4 <= count <= 5:
        return True
    else:
        return False




def get_assin_from_str(s):
    #since you get the link from the form there's no need for regex parse
    #I dont really what the link looks like 
    global CONSTANTS
    link = s[::-1]
    pattern = r'((?!\d{4}\b)[A-Z\d]{4,}\b)'
    asin_search = []
    try:
        asin_search = [a[:10][::-1] for a in re.findall(pattern, link) if len(a)>=10]
   
    except:
        return False, False, False
    else:
        for b in asin_search:
            if is_assin(b):
                asin = b
                region =None
                '''
                for reg in CONSTANTS["MARKETPLACES"]:
                    if CONSTANTS["MARKETPLACES"][reg]['urlwww'] in s:
                        region = reg
                        break
                else:
                    #me just pass cus i am not so sure
                    pass
                '''
                keyword = None
                '''
                x= s.split("/")
                if len(x) >4:
                    keyword = x[3].replace('-', ' ')
                '''
                return asin, region, keyword
            else:
                return False, False, False
        return False, False, False

