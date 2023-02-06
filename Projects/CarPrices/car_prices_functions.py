import pandas as pd
import numpy as np
from datetime import datetime,date,timedelta

def date_transformer(date : str) -> str:

    swedish_date_mapping = {'jan' : '01', 'feb' : '02', 'mar' : '03', 'apr' : '04', 'maj' : '05', 'jun' : '06', 'jul' : '07', 'aug' : '08', 'sep' : '09', 'okt' : '10', 'nov' : '11' ,'dec' : '12'}

    if 'idag' in date:
        return_date = datetime.now().strftime('%m-%d')
    elif 'igår' in date:
        return_date = (datetime.now() - timedelta(days=1)).strftime('%m-%d')
    else:
        day = date[0]
        month = swedish_date_mapping[date[1]]
        if int(day) < 10:
            return_date = f'{month}-0{day}'
        else:
            return_date = f'{month}-{day}'
        
    return return_date


def create_car_dataset(soup):
    car_price_s = soup.find_all(lambda tag: tag.name == "div" and tag.get("class") == ["Card-price"])
    time_s = soup.find_all("div", {"class" : "ImageInfoBox-date"})
    time_s = time_s[:int(len(time_s)/2)] # Time is duplicated. Reason unknown for now. Selecting only the first 
    car_name_s = soup.find_all("div", {"class" : "Card-image CardImage--boarder"})
    car_data_s = soup.find_all("div", {"class" : "Card-carData"})

    car_price_list = list()
    time_list = list()
    car_name_list = list()
    car_year_list = list()
    car_miles_list = list()

    for div_element in range(len(car_price_s)):
        car_price = car_price_s[div_element].find("p").text.strip()
        time_of_ad = time_s[div_element].text.strip()
        car_name = car_name_s[div_element].find('img', alt = True)['alt']
        car_year = car_data_s[div_element].text.strip().split(',')[0]
        amount_miles = car_data_s[div_element].text.strip().split(',')[1].replace(" ","").replace("mil","")

        car_price_list.append(car_price)
        time_list.append(time_of_ad)
        car_name_list.append(car_name)
        car_year_list.append(car_year)
        car_miles_list.append(amount_miles)

    car_dataset = pd.DataFrame(zip(car_price_list,time_list,car_name_list,car_year_list,car_miles_list))
    car_dataset.columns = ['price','timestamp','car_string','year','miles']

    car_dataset_copy =  car_dataset.copy()

    car_dataset['car_model'] = car_dataset.car_string.apply(lambda x : x.split()[0])
    car_dataset.price = car_dataset.price.apply(lambda x : x.replace("kr","").replace(" ",""))
    car_dataset.price = np.where(car_dataset.price == "", 0, car_dataset.price)
    car_dataset.price = car_dataset.price.astype(int)


    timestamp_list = list(car_dataset.timestamp)
    timestamp_list_split = [x.split() for x in timestamp_list]
    timestamp_list_modified = [x[:-1] for x in timestamp_list_split]


    timestamp_list_final = [date_transformer(x) for x in timestamp_list_modified ]
    car_dataset['timestamp'] = timestamp_list_final

    duplicated_index = car_dataset[car_dataset.duplicated()].index
    car_dataset = car_dataset.drop(duplicated_index, axis = 'index')
    
    return car_dataset, car_dataset_copy

def create_car_brand_dict():
    get_request = requests.get(f"https://bilweb.se/sok?offset=0&limit=1000&order_by=timestamp&order=desc&type=1&brand=517&have_mrf_association=&query=&price_min=0&price_max=500000&year_min=&year_max=&property_mileage_min=&property_mileage_max=&fuel%5B%5D=1&fuel%5B%5D=4&fuel%5B%5D=5&gear_box%5B%5D=2&region=12")
    html=get_request.content
    soup_initial = BeautifulSoup(html)

    car_brand_dict = dict() 
    car_brand_code_mapping = soup_initial.find_all("div", {"class" : "Grid-cell u-sm-size1of2 u-size1of2"})[0]
    for i,option in enumerate(car_brand_code_mapping.find_all('option')):
        if i == 0:
            continue
        brand_code = option['value']
        car_name = option.text
        car_brand_dict[car_name] = brand_code
        
    with open('car_brand_dict.pkl', 'wb') as f:
        pickle.dump(car_brand_dict, f)

