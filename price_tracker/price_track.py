import requests
from bs4 import BeautifulSoup
import sys

def get_links() :
    
    with open('prod_urls.txt' , 'r') as f :
        links = f.readlines()
        
    return links


def get_content(url, img=False) :
    '''
    It takes url and returns html content using requests library !!!
    
    Since we need to fetch both text and images we have flag variable correspondingly...
    
    '''

    new_header  = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
               "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    try :
        
        response = requests.get(url, headers = new_header)

        if response.status_code != 200 :

            print('Request Failed')
            return None

        if img :
            return response.content   # for non text content (imgs, pdfs...)
        
        return response.text

    except requests.exceptions.ConnectionError :
        print('Connection Error')
        sys.exit()


def save_image(soup, uid) :
    
    # given html soup, it will fetch and store the image.
    # pending - Image name should be product id   --done
    
    image_div = soup.find('div', class_='imgTagWrapper')
    #soup.find_all(id="imgTagWrapperId")

    img = image_div.find('img')['src']
    img_data = get_content(img, img=True)
    
    with open(f'price_tracker/static/{uid}.jpg', 'wb') as f :
        f.write(img_data)
    


def format_price(price) :
    
    rupee_sym = price[0]
    remove = [ rupee_sym, ',' ]
    
    for sym in remove :
        price = price.replace(sym, '')
        
    return float(price)

def get_prices(soup) :

    '''
    It will take soup object and retrieve all the prices.
    It will extract MRP, current offer price
    
    '''
    price_lists = soup.find(id="price").get_text().strip().split()
    # sample format
    # ['M.R.P.:', '₹2,800.00', 'Deal', 'Price:', '₹1,793.60', 'You', 'Save:', '₹1,202.00', '(34%)', 
    #   'You', 'Save:', '₹1,006.40', '(36%)', 'Inclusive', 'of','all','taxes']
    price_dict = {}

    if price_lists[0] == 'M.R.P.:' :
        mrp = price_lists[1]
        
    rupee_sym = mrp[0]  # rupee symbol
    current = 0 # if code fails -> worst case...
    
    
    for item in price_lists[2:] :
        if rupee_sym in item :
            current = item
            break
    
    # format the price -> str to float
    mrp = format_price(mrp)
    current = format_price(current)
    
    price_dict['mrp'] = mrp
    price_dict['cmp'] = current
    
    return price_lists, price_dict


def price_wrapper(link) :


    link = link.strip()
    # unique_id = link.split('/')[5]

    split = link.split('/')
    ind = split.index('dp')
    unique_id = split[ind+1]

    prod = get_content(link)  # requests
    

    soup = BeautifulSoup(prod, 'html.parser')
    prod_title = soup.find(id="productTitle").get_text().strip()

    # print('Unique ID :', unique_id)
    # print(f'Title : {prod_title}')
    
    save_image(soup, unique_id)
    price_dict = get_prices(soup)[1]

    out = []
    # prod_title = 'abc'
    out.extend([unique_id, prod_title])
    out.extend(list(price_dict.values()))

    return out
