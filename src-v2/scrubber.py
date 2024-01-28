# https://dev.to/chukhraiartur/scrape-google-flights-with-python-4dln

# you have to do:
# pip install -r requirements.txt
# playwright install  

from playwright.sync_api import sync_playwright, Locator, Page
from selectolax.lexbor import LexborHTMLParser
import json, time


def json_to_csv(file_descriptor, json_data):
    for flight in json_data:
    # flight = json_data
        file_descriptor.write(
            str(flight['category']).replace(',','')+',' +
            str(flight['flight_class']).replace(',','') + ',' +
            str(flight['departure_date']).replace(',','') + ',' +
            str(flight['return_date']).replace(',','')+',' +
            str(flight['departure_time']).replace(',','') + ',' +
            str(flight['arrival_time']).replace(',','')+',' +
            str(flight['company']).replace(',','')+',' +
            str(flight['duration']).replace(',','')+',' +
            str(flight['stops']).replace(',','')+',' +
            str(flight['emissions']).replace(',','')+',' +
            str(flight['emission_comparison']).replace(',','')+',' +
            str(flight['price']).replace(',','')+',' +
            str(flight['price_type']).replace(',','')+',' +
            str(flight['departure_airport']).replace(',','')+',' +
            str(flight['arrival_airport']).replace(',','') + '\n'

    )

def get_page(page, playwright, from_place, to_place, departure_date, return_date):
    page.goto('https://www.google.com/travel/flights?hl=en-US&curr=USD')

    # click "Economy" (flight class) and change it
    page.get_by_label('Economy').click()
    #page.get_by_role('option', name='Premium economy').click()
    page.get_by_role('option', name='Business').click()
    time.sleep(1)
    
    # add an adult
    page.get_by_placeholder('Where to?').click()
    page.get_by_label('1 passenger').click()
    page.get_by_label('Add adult').click()
    page.get_by_role('button', name='Done').click()

    # type "From"
    from_place_field = page.query_selector_all('.e5F5td')[0]
    from_place_field.click()
    time.sleep(1)
    from_place_field.type(from_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # type "To"
    to_place_field = page.query_selector_all('.e5F5td')[1]
    to_place_field.click()
    time.sleep(1)
    to_place_field.type(to_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # type "Departure date"
    departure_date_field = page.query_selector_all('[jscontroller="s0nXec"] [aria-label="Departure"]')[0]
    departure_date_field.click()
    time.sleep(1)
    departure_date_field.type(departure_date)
    time.sleep(1)
    page.keyboard.press('Enter')
    # page.query_selector('.WXaAwc .VfPpkd-LgbsSe',).click()
    time.sleep(1)

    # type "Return date"  pxWpE
    return_date_field = page.query_selector_all('[jscontroller="OKD1oe"] [aria-label="Return"]')[1]
    return_date_field.click()
    time.sleep(1)
    return_date_field.type(return_date)
    time.sleep(1)
    page.keyboard.press('Enter')
    #page.query_selector('.WXaAwc .VfPpkd-LgbsSe').click()
    time.sleep(1)
    page.keyboard.press('Enter')

    # press "Explore"
    page.query_selector('.MXvFbd .VfPpkd-LgbsSe').click()
    time.sleep(2)

    # press "More flights"
    try:
        page.query_selector('.zISZ5c button').click()
        time.sleep(2)
    except:
        print('---------------')
        print('No more flights')
        print('---------------')

    parser = LexborHTMLParser(page.content())
    return parser

def scrape_google_flights(parser, flight_class, departure_date, return_date):
    data = []

    categories = parser.root.css('.zBTtmb')
    category_results = parser.root.css('.Rk10dc')

    for category, category_result in zip(categories, category_results):
        category_data = []

        for result in category_result.css('.yR1fYc'):
            date = result.css('[jscontroller="cNtv4b"] span')
            departure_time = date[0].text()
            arrival_time = date[1].text()
            company = result.css_first('.Ir0Voe .sSHqwe').text()
            duration = result.css_first('.AdWm1c.gvkrdb').text()
            stops = result.css_first('.EfT7Ae .ogfYpf').text()
            emissions = result.css_first('.V1iAHe .AdWm1c').text()
            emission_comparison = result.css_first('.N6PNV').text()
            price = result.css_first('.U3gSDe .FpEdX span').text()
            price_type = result.css_first('.U3gSDe .N872Rd').text() if result.css_first('.U3gSDe .N872Rd') else None

            flight_data = {
                'flight_class': flight_class,
                'departure_date': departure_date,
                'return_date': return_date,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'company': company,
                'duration': duration,
                'stops': stops,
                'emissions': emissions,
                'emission_comparison': emission_comparison,
                'price': price,
                'price_type': price_type
            }

            airports = result.css_first('.Ak5kof .sSHqwe')
            service = result.css_first('.hRBhge')

            if service:
                flight_data['service'] = service.text()
            else:
                flight_data['departure_airport'] = airports.css_first('span:nth-child(1) .eoY5cb').text()
                flight_data['arrival_airport'] = airports.css_first('span:nth-child(2) .eoY5cb').text()
            flight_data['category'] = category.text().lower().replace(' ', '_')
            data.append(flight_data)
        #data[category.text().lower().replace(' ', '_')] = category_data
    return data


def run(playwright):
    airports = ['ZRH', 'MXP', 'MAD', 'CDG']
    departure_dates = ['12/28/2023','12/29/2023','12/30/2023','12/31/2023','1/1/2024']
    return_dates = ['1/16/2024','1/17/2024','1/18/2024']

    to_place = 'HAV' 

    with open('outputs.csv', 'w', encoding="utf-8") as csv_file:
        with open("outputs.json", "w", encoding="utf-8") as json_file:
            page = playwright.chromium.launch(headless=False).new_page()
            # There is a accept cookies button from google that shows up once:
            page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CHF')
            page.get_by_role('button', name='Accept all').click()
            
            for from_place in airports:
                for departure_date in departure_dates:
                    for return_date in return_dates:
                        try:
                            parser = get_page(page, playwright, from_place, to_place, departure_date, return_date)
                            google_flights_results = scrape_google_flights(parser, 'Premium economy', departure_date, return_date)
                            json_file.write(json.dumps(google_flights_results, indent=2, ensure_ascii=False) + ',')
                            json_to_csv(csv_file, google_flights_results)
                        except Exception as e:
                            print('-------------------')
                            print(f'Error processing {from_place} - {to_place} - {departure_date} - {return_date}: {e}')
                            print(e)
                            print('-------------------')
                        time.sleep(5)
            page.close()

with sync_playwright() as playwright:
    run(playwright)