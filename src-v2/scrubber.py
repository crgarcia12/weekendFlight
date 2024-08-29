# https://dev.to/chukhraiartur/scrape-google-flights-with-python-4dln

# you have to do:
# pip install -r requirements.txt
# playwright install
# python scrubber.py
# Use the Testing VSCode extension to easily find components in the UI
# If you see online syntax like getByRole, getByLabel, etc, it's because of the Testing extension uses TYPSCRIPT and not python

#ASYNC from playwright.sync_api import sync_playwright, Locator, Page
from playwright.async_api import async_playwright
from selectolax.lexbor import LexborHTMLParser
import json, time
import asyncio




# html_content = '''
# <span aria-hidden="true" class="PTuQse sSHqwe tPgKwe ogfYpf"><div class="QylvBf">
# <span jsaction="wGOFk:pCNdcd;AHEEwb:QsRKXb;DJL8Fd:pCNdcd;z0rlDb:QsRKXb" jsshadow="" jscontroller="E0AZj" data-position="2" data-caret-position="2" data-max-width="400px"><span jsslot="">
# <span jscontroller="cNtv4b" jsaction="focus:AHmuwe; blur:O22p3e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchend:yfqBxc" aria-describedby="gEvJbfc162" tabindex="-1" aria-label="">ZRH</span>
# </span>
# <div jsname="bN97Pc" id="gEvJbfc162" style="display: none;">
# <span class="eoY5cb">Zurich Airport</span></div></span></div>–<div class="QylvBf">
# <span jsaction="wGOFk:pCNdcd;AHEEwb:QsRKXb;DJL8Fd:pCNdcd;z0rlDb:QsRKXb" jsshadow="" jscontroller="E0AZj" data-position="2" data-caret-position="2" data-max-width="400px">
# <span jsslot="">
# <span jscontroller="cNtv4b" jsaction="focus:AHmuwe; blur:O22p3e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchend:yfqBxc" aria-describedby="gEvJbfc163" tabindex="-1" aria-label="">GIG</span>
# </span><div jsname="bN97Pc" id="gEvJbfc163" style="display: none;">
# <span class="eoY5cb">RIOgaleão - Aeroporto Internacional Tom Jobim</span></div></span></div></span>
# '''

# # Initialize the parser
# parser = LexborHTMLParser(html_content)

# # Extract airport codes
# airport_codes = [node.text() for node in parser.root.css('span[jscontroller="cNtv4b"]')]


# print(airport_codes)






def json_to_csv(file_descriptor, json_data, header = True):
    if header:
        file_descriptor.write(
            'category,flight_class,departure_date,return_date,price,price_type,departure_time,arrival_time,company,duration,stops,emissions,emission_comparison,departure_airport,arrival_airport\n'
        )
    for flight in json_data:
    # flight = json_data
        file_descriptor.write(
            str(flight['category']).replace(',','')+',' +
            str(flight['flight_class']).replace(',','') + ',' +
            str(flight['departure_date']).replace(',','') + ',' +
            str(flight['return_date']).replace(',','')+',' +
            str(flight['price']).replace(',','').replace('CHF ', '') +',' +
            str(flight['price_type']).replace(',','')+',' +
            str(flight['departure_time']).replace(',','') + ',' +
            str(flight['arrival_time']).replace(',','')+',' +
            str(flight['company']).replace(',','')+',' +
            str(flight['duration']).replace(',','')+',' +
            str(flight['stops']).replace(',','')+',' +
            str(flight['emissions']).replace(',','')+',' +
            str(flight['emission_comparison']).replace(',','')+',' +
            str(flight['departure_airport']).replace(',','')+',' +
            str(flight['arrival_airport']).replace(',','') + '\n'

    )

async def get_page_async(page, from_place, to_place, flight_class, departure_date, return_date):
    await page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CHF')

    accept_terms_button = page.get_by_role('button', name = 'Accept all')
    if await accept_terms_button.is_visible(timeout=3000): 
        await accept_terms_button.click()
    else:
        print('Accept terms button not found')

    print('Select class')
    if flight_class != 'Economy':
        await page.getByLabel('Economy').locator('div').click()
        await page.getByRole('option', name=flight_class).click()

    print('Setting passengers')
    await page.get_by_label('1 passenger, change number of').click()
    await page.get_by_label('Add adult').click()
    await page.get_by_label('Add child').click()
    await page.get_by_role('button', name ='Done').click()

    print('from_place:', from_place)
    await page.get_by_label('Where from?').click()
    await page.get_by_role('combobox', name = 'Where else?').fill(from_place)
    await asyncio.sleep(1)
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    await asyncio.sleep(1)

    print('to_place:', to_place)
    await page.get_by_label('Where to?').click()
    await page.get_by_role('combobox', name = 'Where to?').fill(to_place)
    await asyncio.sleep(1)
    await page.keyboard.press('Tab')
    await page.keyboard.press('Tab')
    await asyncio.sleep(1)

    print('departure_date:', departure_date)
    await page.get_by_role('textbox', name = 'Departure').click()
    await page.get_by_role('textbox', name = 'Departure').fill(departure_date)
    await page.get_by_role('textbox', name = 'Departure').press('Tab')
    await asyncio.sleep(1)

    print('return_date:', return_date)
    await page.get_by_role('textbox', name = 'Return').click()
    await page.get_by_role('textbox', name = 'Return').fill(return_date)
    await page.get_by_role('textbox', name = 'Return').press('Tab')
    #await page.get_by_role('textbox', name='Return').press('Enter')
    #await page.get_by_label('Done').click()
    await asyncio.sleep(1)
    
    #await page.get_by_label('Explore destinations').click()
    await page.get_by_label('Search', exact = True).click()

    await asyncio.sleep(5)

    parser = LexborHTMLParser(await page.content())
    return parser

def get_page(page, playwright, from_place, to_place, flight_class, departure_date, return_date):
    # click "Economy" (flight class) and change it
    # page.get_by_label('Economy').click()
    # #page.get_by_role('option', name='Economy').click()
    # page.get_by_role('option', name=flight_class).click()
    time.sleep(1)
    
    page.get_by_label('1 passenger, change number of').click()
    page.get_by_label('Add adult').click()
    page.get_by_label('Add child').click()
    page.get_by_role('button', name='Done').click()
    page.get_by_role('combobox', name='Where from?').fill('ZRH')
    page.get_by_role('combobox', name='Where to?').click()
    page.get_by_role('combobox', name='Where to?').fill('GRU').press('Enter')


    # # add an adult
    # print('Adding an adult')
    # # page.get_by_placeholder('Where to?').click()[0]
    # page.get_by_label('1 passenger').click()
    # page.get_by_label('Add adult').click()
    # page.get_by_label('Add child').click()
    # page.get_by_role('button', name='Done').click()
    # time.sleep(1)

    # # type "From"
    # print('Typing from place')
    # #from_place_field = page.query_selector_all('.e5F5td')[0]
    # from_place_field = page.locator('input[aria-label="Where from?"]')[0]
    # from_place_field.click()
    # time.sleep(1)
    # from_place_field.type(from_place)
    # time.sleep(0.5)
    # page.keyboard.press('Enter')

    # # type "To"
    # print('Typing to place')
    # to_place_field = page.locator('input[aria-label="Where to?"]') #= page.query_selector_all('.e5F5td')[1]
    # to_place_field.click()
    # time.sleep(1)
    # to_place_field.type(to_place)
    # time.sleep(0.5)
    # page.keyboard.press('Enter')

    # # type "Departure date"
    # print('Typing departure date')
    # departure_date_field = page.query_selector_all('[aria-label="Departure"]')[0]
    # departure_date_field.click()
    # time.sleep(0.5)
    # departure_date_field.type(departure_date)
    # time.sleep(0.5)
    # page.keyboard.press('Enter')
    # # page.query_selector('.WXaAwc .VfPpkd-LgbsSe',).click()
    # time.sleep(0.5)

    # # type "Return date"  pxWpE
    # print('Typing return date')
    # return_date_field = page.query_selector_all('[aria-label="Return"]')[1]
    # return_date_field.click()
    # time.sleep(0.5)
    # return_date_field.type(return_date)
    # time.sleep(0.5)
    # page.keyboard.press('Enter')
    # #page.query_selector('.WXaAwc .VfPpkd-LgbsSe').click()
    # time.sleep(0.5)
    # page.keyboard.press('Enter')

    # # press "Explore"
    # print('Pressing explore')
    # page.query_selector('.MXvFbd .VfPpkd-LgbsSe').click()
    # time.sleep(0.5)

    # # press "More flights"
    # try:
    #     page.query_selector('.zISZ5c button').click()
    #     time.sleep(2)
    # except:
    #     print('---------------')
    #     print('No more flights')
    #     print('---------------')

    parser = LexborHTMLParser(page.content())
    return parser

def scrape_google_flights(parser, flight_class, departure_date, return_date):
    data = []

    # Google flights usually split the flights in "Categories". For example": "Best departing flights", "other departing flights"
    # Usually you look at the fitst category and can expand the rest to get more flights
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
                airport_codes = [node.text() for node in airports.css('span[jscontroller="cNtv4b"]')]
                flight_data['departure_airport'] = airport_codes[0]
                flight_data['arrival_airport'] = airport_codes[1]

            flight_data['category'] = category.text().lower().replace(' ', '_')
            data.append(flight_data)
        #data[category.text().lower().replace(' ', '_')] = category_data
    return data

async def run_async(pw):
    airports = ['ZRH', 'MXP']
    departure_dates = ['6/21/2025']
    return_dates = ['7/21/2025']
    flight_class = 'Economy'
    arrival_airports = ['GIG', 'GRU'] 

    with open('outputs.csv', 'w', encoding="utf-8") as csv_file:
        with open("outputs.json", "w", encoding="utf-8") as json_file:
            try:
                browser = await pw.chromium.launch(headless=False)
                page = await browser.new_page()
                # There is a accept cookies button from google that shows up once:
                
                for from_place in airports:
                    for departure_date in departure_dates:
                        for return_date in return_dates:
                            for arrival_airport in arrival_airports:
                                try:
                                    # ASYNC parser = get_page(page, pw, from_place, arrival_airport, flight_class, departure_date, return_date)
                                    parser = await get_page_async(page, from_place, arrival_airport, flight_class, departure_date, return_date)
                                    google_flights_results = scrape_google_flights(parser, flight_class, departure_date, return_date)
                                    if(len(google_flights_results) == 0):
                                        print(f'[ERROR] No results for {from_place} - {arrival_airport} - {departure_date} - {return_date}')
                                        csv_file.write(f'[ERROR] No results for {from_place} - {arrival_airport} - {departure_date} - {return_date}')
                                        continue
                                    json_file.write(json.dumps(google_flights_results, indent=2, ensure_ascii=False) + ',')
                                    json_to_csv(csv_file, google_flights_results)
                                except Exception as e:
                                    print('-------------------')
                                    print(f'Error processing {from_place} - {arrival_airport} - {departure_date} - {return_date}: {e}')
                                    print(e)
                                    print('-------------------')
                                time.sleep(5)
                await page.close()
            except Exception as e:
                print(e)

async def main():
    async with async_playwright() as pw:
        await run_async(pw)


# Check if there's an existing event loop
try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # No event loop is running
    loop = None

if loop and loop.is_running():
    # If there's an existing event loop, run the main function within it
    loop.create_task(main())
else:
    # If no event loop is running, create a new one and run the main function
    asyncio.run(main())


#[ERROR] No results for ZRH - GIG - 6/21/2025 - 7/21/2025