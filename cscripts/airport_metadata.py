import pandas as pd
import airportsdata


def gen_airport_metadata(airports_iata_code, csv_file='data/raw/airport_metadata.csv'):
    airport_metadata = airportsdata.load()
    
    filtered_airport_metadata_lid = {}

    for icao, airport_info in airport_metadata.items():
        lid = airport_info['lid']
        country = airport_info['country']
        if lid != '': # only keep airports with lid code
            airport_info.pop('icao', None)  # Remove the 'icao' field
            filtered_airport_metadata_lid[lid] = airport_info
            
    filtered_airport_metadata = {}

    for icao, airport_info in airport_metadata.items():
        iata = airport_info['iata']
        country = airport_info['country']
        if iata != '': # only keep airports with lid code
            airport_info.pop('icao', None)  # Remove the 'icao' field
            filtered_airport_metadata[iata] = airport_info
            
    enriched_airports = []
    for index, row in airports_iata_code.iterrows():
        airport_id = row['id']
        iata = row['code']
        metadata = filtered_airport_metadata.get(iata, {})
        enriched_airport = {
            'id': airport_id,
            'code': iata,
            'name': metadata.get('name', None),
            'city': metadata.get('city', None),
            'country': metadata.get('country', None),
            'subd': metadata.get('subd', None),
            'elevation': metadata.get('elevation', None),
            'lat': metadata.get('lat', None),
            'lon': metadata.get('lon', None),
            'tz': metadata.get('tz', None),
        }
        enriched_airports.append(enriched_airport)
        
    # Convert enriched_airports to DataFrame
    enriched_airports_df = pd.DataFrame(enriched_airports)
    
    # Enrich the first 27 rows of enriched_airports_df with metadata from filtered_airport_metadata_lid
    for index, row in enriched_airports_df.iloc[:27].iterrows():
        lid = row['code']
        metadata = filtered_airport_metadata_lid.get(lid, {})
        enriched_airports_df.loc[index, 'name'] = metadata.get('name', None)
        enriched_airports_df.loc[index, 'city'] = metadata.get('city', None)
        enriched_airports_df.loc[index, 'country'] = metadata.get('country', None)
        enriched_airports_df.loc[index, 'subd'] = metadata.get('subd', None)
        enriched_airports_df.loc[index, 'elevation'] = metadata.get('elevation', None)
        enriched_airports_df.loc[index, 'lat'] = metadata.get('lat', None)
        enriched_airports_df.loc[index, 'lon'] = metadata.get('lon', None)
        enriched_airports_df.loc[index, 'tz'] = metadata.get('tz', None)
        
    additional_data = [
    {'code': 'A02', 'city': 'Deadmans Bay', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 55.11669921875, 'lon': -131.56689453125, 'tz': 'America/Juneau', 'name': 'Deadmans Bay Airport'},
    {'code': 'A03', 'city': 'Hallo Bay', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 58.89830017089844, 'lon': -153.18099975585938, 'tz': 'America/Anchorage', 'name': 'Hallo Bay Airport'},
    {'code': 'A07', 'city': 'Selawik', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 66.60009765625, 'lon': -159.98599243164062, 'tz': 'America/Nome', 'name': 'Roland Norton Memorial'},
    {'code': 'A12', 'city': 'Cinnabar', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 45.18330001831055, 'lon': -110.93399810791016, 'tz': 'America/Denver', 'name': 'Cinnabar Airport'},
    {'code': 'A23', 'city': 'Bradley Lake', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 60.483299255371094, 'lon': -151.0330047607422, 'tz': 'America/Anchorage', 'name': 'Bradley Lake Airport'},
    {'code': 'A27', 'city': 'Pogo Mines', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 64.8499984741211, 'lon': -141.14999389648438, 'tz': 'America/Yakutat', 'name': 'Pogo Mines Airport'},
    {'code': 'A29', 'city': 'Kiluda Bay', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -151.60000610351562, 'tz': 'America/Anchorage', 'name': 'Kiluda Bay Airport'},
    {'code': 'A37', 'city': 'Kako', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -152.58399963378906, 'tz': 'America/Anchorage', 'name': 'Kako Airport'},
    {'code': 'A40', 'city': 'Cape Simpson', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 70.7332992553711, 'lon': -157.14999389648438, 'tz': 'America/Nome', 'name': 'Cape Simpson Airport'},
    {'code': 'A52', 'city': 'Silver Salmon Creek', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -153.5, 'tz': 'America/Anchorage', 'name': 'Silver Salmon Creek Airport'},
    {'code': 'A71', 'city': 'Homer', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.63330078125, 'lon': -151.5500030517578, 'tz': 'America/Anchorage', 'name': 'Bear Cove Farm'},
    {'code': 'A72', 'city': 'Chinitna Bay', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -153.5, 'tz': 'America/Anchorage', 'name': 'Chinitna Bay Airport'},
    {'code': 'A74', 'city': 'Nanwalek', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.43330001831055, 'lon': -151.8000030517578, 'tz': 'America/Anchorage', 'name': 'Dog Fish Bay'},
    {'code': 'A83', 'city': 'Petrof Point', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -153.5, 'tz': 'America/Anchorage', 'name': 'Petrof Point Airport'},
    {'code': 'A97', 'city': 'Akulik', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -153.5, 'tz': 'America/Anchorage', 'name': 'Akulik Air Strip'},
    {'code': 'A98', 'city': 'Deadfall', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 59.83330154418945, 'lon': -153.5, 'tz': 'America/Anchorage', 'name': 'Deadfall Air Strip'},
    {'code': 'AA8', 'city': 'Deadhorse', 'country': 'US', 'subd': 'Alaska', 'elevation': 0, 'lat': 70.19999694824219, 'lon': -148.4669952392578, 'tz': 'America/Anchorage', 'name': 'Badami'},
    ]

    # Add the additional data to enriched_airports_df
    for data in additional_data:
        code = data['code']
        matching_index = enriched_airports_df[enriched_airports_df['code'] == code].index
        if not matching_index.empty:
            matching_index = matching_index[0]
            for key, value in data.items():
                enriched_airports_df.loc[matching_index, key] = value
                
    enriched_airports_df.to_csv(csv_file, index=False)
                
    return enriched_airports_df