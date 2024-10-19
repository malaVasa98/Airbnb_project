# Import necessary packages
import json
import pandas as pd
import streamlit as st
import re
import pydeck as pdk
from sqlalchemy import create_engine

engine = create_engine('sqlite:///AirBnB_data.db', echo=True)
# loading the airbnb json file
with open('sample_airbnb.json') as airbnb:
    airbnb_data = json.load(airbnb)

# ------ PROPERTY TABLE & AVAILABILITY TABLE------
id_ = []
listing_url = []
name = []
description = []
property_type = []
room_type = []
bed_type = []
min_nights = []
max_nights = []
canc_policy = []
accommodates = []
bedrooms = []
beds = []
bathrooms = []
amenities = []
price = []
extra_ppl = []
guests_inc = []
availability_30 = []
availability_60 = []
availability_90 = []
availability_365 = []
num_reviews = []
for i in range(len(airbnb_data)):
    id_.append(airbnb_data[i]['_id'])
    listing_url.append(airbnb_data[i]['listing_url'])
    name.append(airbnb_data[i]['name'])
    description.append(airbnb_data[i]['description'])
    property_type.append(airbnb_data[i]['property_type'])
    room_type.append(airbnb_data[i]['room_type'])
    bed_type.append(airbnb_data[i]['bed_type'])
    min_nights.append(int(airbnb_data[i]['minimum_nights']))
    max_nights.append(int(airbnb_data[i]['maximum_nights']))
    canc_policy.append(airbnb_data[i]['cancellation_policy'])
    accommodates.append(airbnb_data[i]['accommodates'])
    bedrooms.append(int(airbnb_data[i]['bedrooms']) if 'bedrooms' in airbnb_data[i].keys() else None)
    beds.append(int(airbnb_data[i]['beds']) if 'beds' in airbnb_data[i].keys() else None)
    bathrooms.append(int(airbnb_data[i]['bathrooms']) if 'bathrooms' in airbnb_data[i].keys() else None)
    amenities.append(', '.join(map(str,airbnb_data[i]['amenities'])))
    price.append(airbnb_data[i]['price'])
    extra_ppl.append(airbnb_data[i]['extra_people'])
    guests_inc.append(airbnb_data[i]['guests_included'])
    availability_30.append(airbnb_data[i]['availability']['availability_30'])
    availability_60.append(airbnb_data[i]['availability']['availability_60'])
    availability_90.append(airbnb_data[i]['availability']['availability_90'])
    availability_365.append(airbnb_data[i]['availability']['availability_365'])
    num_reviews.append(int(airbnb_data[i]['number_of_reviews']))
AIRBNB_prop = {
    'ID':id_,
    'listing_url':listing_url,
    'Name':name,
    'Description':description,
    'Property_type':property_type,
    'Room_type':room_type,
    'Bed_type':bed_type,
    'Minimum_nights':min_nights,
    'Maximum_nights':max_nights,
    'Cancellation_policy':canc_policy,
    'Accommodates':accommodates,
    'Bedrooms':bedrooms,
    'Beds':beds,
    'Bathrooms':bathrooms,
    'Amenities':amenities,
    'Price':price,
    'Extra_people':extra_ppl,
    'Guests_included':guests_inc,
    'No_of_reviews':num_reviews
}
AIRBNB_avail = {
    'ID':id_,
    'Availability_30':availability_30,
    'Availability_60':availability_60,
    'Availability_90':availability_90,
    'Availability_365':availability_365    
}
# Property table
df_Airbnb_prop = pd.DataFrame(AIRBNB_prop)
# Data Preprocessing
# To fill in the empty strings
df_Airbnb_prop.replace(to_replace='',value='Unavailable',inplace=True)
# To fill in the NaN values
values = {'Bedrooms':0,'Beds':0,'Bathrooms':1}
df_Airbnb_prop.fillna(value=values,inplace=True)
df_Airbnb_prop.to_csv('Property_table.csv',index=False)

# Availability table
df_airbnb_avail = pd.DataFrame(AIRBNB_avail)
# Saving
df_airbnb_avail.to_csv('Availability_table.csv',index=False)

# ------ HOST TABLE ------
AIRBNB_host = {
    'ID':id_,
    'Host_id':[],
    'Host_name':[],
    'Host_response_time':[],
    'Is_superhost':[],
    'Identity_verified':[],
    'Total_listings_count':[],
    'Verifications':[]
}
for val in airbnb_data:
    AIRBNB_host['Host_id'].append(val['host']['host_id'])
    AIRBNB_host['Host_name'].append(val['host']['host_name'])
    AIRBNB_host['Host_response_time'].append(val['host']['host_response_time'] if 'host_response_time' in val['host'].keys() else 'Unavailable')
    AIRBNB_host['Is_superhost'].append('Yes' if val['host']['host_is_superhost']==True else 'No')
    AIRBNB_host['Identity_verified'].append('Yes' if val['host']['host_identity_verified']==True else 'No')
    AIRBNB_host['Total_listings_count'].append(val['host']['host_total_listings_count'])
    AIRBNB_host['Verifications'].append(', '.join(map(str,val['host']['host_verifications'])))

df_airbnb_host = pd.DataFrame(AIRBNB_host)
# Data preprocessing
#df_airbnb_host.drop_duplicates(subset=['Host_name'],inplace=True,ignore_index=True)

# Saving
df_airbnb_host.to_csv('Host_table.csv',index=False)

# ------ LOCATION TABLE ------
AIRBNB_location = {
    'ID':id_,
    'City_or_Town':[],
    'Address':[],
    'Country':[],
    'Country_code':[],
    'Coordinates':[],
    'Latitude':[],
    'Longitude':[]
}
for val in airbnb_data:
    AIRBNB_location['City_or_Town'].append(val['address']['market'])
    AIRBNB_location['Address'].append(val['address']['street'])
    AIRBNB_location['Country'].append(val['address']['country'])
    AIRBNB_location['Country_code'].append(val['address']['country_code'])
    AIRBNB_location['Coordinates'].append(val['address']['location']['coordinates'])
    AIRBNB_location['Latitude'].append(val['address']['location']['coordinates'][1])
    AIRBNB_location['Longitude'].append(val['address']['location']['coordinates'][0])
df_airbnb_location = pd.DataFrame(AIRBNB_location)
df_airbnb_coord = df_airbnb_location[['ID','Coordinates']]
# Data Preprocessing
df_airbnb_location.replace(to_replace='',value='Unavailable',inplace=True)
df_airbnb_location.replace(to_replace='Other (Domestic)',value='Hawaii',inplace=True)
df_airbnb_location.loc[597,'City_or_Town']= 'Sydney'
df_airbnb_location.loc[617,'City_or_Town']= 'New York'
df_airbnb_location.loc[639,'City_or_Town']= 'Rio De Janeiro'
df_airbnb_location.loc[656,'City_or_Town']= 'Montreal'
df_airbnb_location.loc[788,'City_or_Town']= 'Barcelona'
df_airbnb_location.loc[836,'City_or_Town']= 'Hawaii'
df_airbnb_location.loc[2945,'City_or_Town']='Aveiro'
df_airbnb_location.loc[3949,'City_or_Town']='Istanbul'
df_airbnb_location.replace(to_replace='Other (International)',value='Rio De Janeiro',inplace=True)
df_airbnb_location.replace({'City_or_Town':['Oahu','The Big Island', 'Maui', 'Kauai']},value='Hawaii',inplace=True)
Len = len(df_airbnb_location)
for i in range(Len):
    if df_airbnb_location.iloc[i]['Country']=='China':
        df_airbnb_location.loc[i,'City_or_Town']='Guangdong Sheng'

# Saving
df_airbnb_location.to_csv('Location_table.csv',index=False)

# ------ REVIEW SCORES TABLE ------
AIRBNB_review_scores = {
    'ID':id_,
    'Accuracy':[],
    'Cleanliness':[],
    'Checkin':[],
    'Communication':[],
    'Location':[],
    'Value':[]
}
for val in airbnb_data:
    AIRBNB_review_scores['Accuracy'].append(val['review_scores']['review_scores_accuracy'] if 'review_scores_accuracy' in val['review_scores'].keys() else None)
    AIRBNB_review_scores['Cleanliness'].append(val['review_scores']['review_scores_cleanliness'] if 'review_scores_cleanliness' in val['review_scores'].keys() else None)
    AIRBNB_review_scores['Checkin'].append(val['review_scores']['review_scores_checkin'] if 'review_scores_checkin' in val['review_scores'].keys() else None)
    AIRBNB_review_scores['Communication'].append(val['review_scores']['review_scores_communication'] if 'review_scores_communication' in val['review_scores'].keys() else None)
    AIRBNB_review_scores['Location'].append(val['review_scores']['review_scores_location'] if 'review_scores_location' in val['review_scores'].keys() else None)
    AIRBNB_review_scores['Value'].append(val['review_scores']['review_scores_value'] if 'review_scores_value' in val['review_scores'].keys() else None)

df_airbnb_review_scores = pd.DataFrame(AIRBNB_review_scores)
# Data preprocessing
df_airbnb_review_scores.fillna(0,inplace=True)

# Saving
df_airbnb_review_scores.to_csv('Review_scores_table.csv',index=False)

# ------ STREAMLIT APP FOR AIRBNB LISTINGS ------
st.markdown(
    """
    <style>
    .centered-title {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 48px;
        font-weight: bold;
        color: red;
    }
    </style>
    <div class="centered-title">AIRBNB</div>
    """,
    unsafe_allow_html=True
)
st.write("Welcome to AirBnB. Explore various accommodations at different prices at your preferred destination.")
dest = st.selectbox('**Choose a destination**',tuple(df_airbnb_location.City_or_Town.unique()),key='destination',index=None,placeholder='Select one')
if dest:
    col1,col2 = st.columns(2)
    with col1:
        accomodation_type = st.selectbox('**Choose an accommodation**',tuple(df_Airbnb_prop.Property_type.unique()),index=None,key='accod',placeholder='Select one')
    with col2:
        price = st.selectbox('**Price range (in dollars)**',['$0-$500','$500-$1000','$1000-$1500','$1500-$2000','$2000 and above'],index=None,key='price',placeholder='Select a price range')
    if (accomodation_type)and(price):
        df_prop =  df_Airbnb_prop[df_Airbnb_prop['Property_type']==accomodation_type]
        df_acc = df_prop.merge(df_airbnb_location,on='ID',how='inner')
        df_des = df_acc[df_acc.City_or_Town==dest]
        del df_des['Coordinates']
        df_des.to_sql('Property_table', con=engine, if_exists='replace', index=False)
        if price!='$2000 and above':
            Pr = re.findall('[0-9]*',price)
            Pr = [int(x) for x in Pr if x!='']
            pr_min,pr_max = Pr
            prop_det = pd.read_sql_query('''select Name from Property_table where (price>=?)and(price<?)''',con=engine,params=(pr_min,pr_max))
        else:
            prop_det = pd.read_sql_query('''select Name from Property_table where price>=2000''',con=engine)
        if prop_det.empty:
            st.write('No Data Available')
        else:
            #st.dataframe(prop_det)
            optz = st.selectbox(f'**Select any {accomodation_type}**',tuple(prop_det.Name),index=None,key='optz',placeholder='Choose one')
            if (optz)and(st.button('Get details')):
                st.markdown(
    """
    <style>
    .subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="subtitle">ACCOMMODATION DETAILS</div>
    """,
    unsafe_allow_html=True
)
                desc = df_des[['Description']][df_des.Name==optz]
                st.write(':green[**Description**]')
                st.write(desc.iloc[0]['Description'])
                ameni = df_des[['Amenities']][df_des.Name==optz]
                st.write(':green[**Amenities**]')
                st.write(ameni.iloc[0]['Amenities'])
                col1,col2 = st.columns(2)
                with col1:
                    room_type = df_des[['Room_type']][df_des.Name==optz]
                    st.write(f':green[**Room Type**]:',room_type.iloc[0]['Room_type'])
                    bed_type = df_des[['Bed_type']][df_des.Name==optz]
                    st.write(f':green[**Bed Type**]:',bed_type.iloc[0]['Bed_type'])
                    bedrooms = df_des[['Bedrooms']][df_des.Name==optz]
                    st.write(f':green[**Bedrooms**]:',str(bedrooms.iloc[0]['Bedrooms']))
                    beds = df_des[['Beds']][df_des.Name==optz]
                    st.write(f':green[**Beds**]:',str(beds.iloc[0]['Beds']))
                    bathrooms = df_des[['Bathrooms']][df_des.Name==optz]
                    st.write(f':green[**Bathrooms**]:',str(bathrooms.iloc[0]['Bathrooms']))
                    price_1 = df_des[['Price']][df_des.Name==optz]
                    st.write(f':green[**Price**]:','$'+str(price_1.iloc[0]['Price']))
                with col2:
                    min_nights = df_des[['Minimum_nights']][df_des.Name==optz]
                    st.write(f':green[**Minimum Nights**]:',str(min_nights.iloc[0]['Minimum_nights']))
                    max_nights = df_des[['Maximum_nights']][df_des.Name==optz]
                    st.write(f':green[**Maximum Nights**]:',str(max_nights.iloc[0]['Maximum_nights']))
                    canc = df_des[['Cancellation_policy']][df_des.Name==optz]
                    st.write(f':green[**Cancellation Policy**]:',canc.iloc[0]['Cancellation_policy'])
                    Accom = df_des[['Accommodates']][df_des.Name==optz]
                    st.write(f':green[**Accommodates**]:',str(Accom.iloc[0]['Accommodates']))
                    xtra = df_des[['Extra_people']][df_des.Name==optz]
                    st.write(f':green[**Extra People**]:',str(xtra.iloc[0]['Extra_people']))
                    guests = df_des[['Guests_included']][df_des.Name==optz]
                    st.write(f':green[**Guests Included**]:',str(guests.iloc[0]['Guests_included']))
                st.markdown(
    """
    <style>
    .subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="subtitle">HOST DETAILS</div>
    """,
    unsafe_allow_html=True
)
                # host details
                # merge property and host table
                df_des_1 = df_des[['ID','Name','Property_type','City_or_Town']]
                df_hos = df_des_1.merge(df_airbnb_host,on='ID',how='inner')
                col1,col2 = st.columns(2)
                with col1:
                    hos_n = df_hos[['Host_name']][df_hos.Name==optz]
                    st.write(f':green[**Host Name**]:',hos_n.iloc[0]["Host_name"])
                    hos_rt = df_hos[['Host_response_time']][df_hos.Name==optz]
                    st.write(f':green[**Host Response Time**]:',hos_rt.iloc[0]["Host_response_time"])
                    hos_id = df_hos[['Identity_verified']][df_hos.Name==optz]
                    st.write(f':green[**Identity Verified**]:',hos_id.iloc[0]["Identity_verified"])
                with col2:
                    hos_tlc = df_hos[['Total_listings_count']][df_hos.Name==optz]
                    st.write(f':green[**Total Listings Count**]:',str(hos_tlc.iloc[0]["Total_listings_count"]))
                    hos_suph = df_hos[['Is_superhost']][df_hos.Name==optz]
                    st.write(f':green[**Superhost**]:',hos_suph.iloc[0]["Is_superhost"])
                    hos_verf = df_hos[['Verifications']][df_hos.Name==optz]
                    st.write(f':green[**Verifications**]:',hos_verf.iloc[0]["Verifications"])
                
                # review scores
                st.markdown(
    """
    <style>
    .subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="subtitle">REVIEW SCORES (OUT OF 10)</div>
    """,
    unsafe_allow_html=True
)
                # merge property and review scores table
                df_rev = df_des_1.merge(df_airbnb_review_scores,on='ID',how='inner')
                col1,col2 = st.columns(2)
                with col1:
                    acc = df_rev[['Accuracy']][df_rev.Name==optz]
                    st.write(f':green[**Accuracy**]:',str(acc.iloc[0]["Accuracy"]))
                    clean = df_rev[['Cleanliness']][df_rev.Name==optz]
                    st.write(f':green[**Cleanliness**]:',str(clean.iloc[0]["Cleanliness"]))
                    checkin = df_rev[['Checkin']][df_rev.Name==optz]
                    st.write(f':green[**Check In**]:',str(checkin.iloc[0]["Checkin"]))
                with col2:
                    comm = df_rev[['Communication']][df_rev.Name==optz]
                    st.write(f':green[**Communication**]:',str(comm.iloc[0]["Communication"]))
                    loca = df_rev[['Location']][df_rev.Name==optz]
                    st.write(f':green[**Location**]:',str(loca.iloc[0]["Location"]))
                    valu = df_rev[['Value']][df_rev.Name==optz]
                    st.write(f':green[**Value**]:',str(valu.iloc[0]["Value"]))
                # Availability details
                st.markdown(
    """
    <style>
    .subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="subtitle">AVAILABILITY FOR BOOKING</div>
    """,
    unsafe_allow_html=True
)
                df_avail = df_des_1.merge(df_airbnb_avail,on='ID',how='inner')
                col1, col2 = st.columns(2)
                with col1:
                    ava_30 = df_avail[['Availability_30']][df_avail.Name==optz]
                    st.write(f':green[**Availability for booking in next 30 days**]:',str(ava_30.iloc[0]['Availability_30']))
                    ava_60 = df_avail[['Availability_60']][df_avail.Name==optz]
                    st.write(f':green[**Availability for booking in next 60 days**]:',str(ava_60.iloc[0]['Availability_60']))
                with col2:
                    ava_90 = df_avail[['Availability_90']][df_avail.Name==optz]
                    st.write(f':green[**Availability for booking in next 90 days**]:',str(ava_90.iloc[0]['Availability_90']))
                    ava_365 = df_avail[['Availability_365']][df_avail.Name==optz]
                    st.write(f':green[**Availability for booking in next 365 days**]:',str(ava_365.iloc[0]['Availability_365']))
                # Location for geo-visualisation
                st.markdown(
    """
    <style>
    .subtitle {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: blue;
    }
    </style>
    <div class="subtitle">LOCATION</div>
    """,
    unsafe_allow_html=True
)
                df_location = df_des[df_des.Name==optz]
                df_loc_up = df_location.merge(df_airbnb_coord,on='ID',how='inner')
                long = df_loc_up.iloc[0]['Longitude']
                lat = df_loc_up.iloc[0]['Latitude']
                #st.dataframe(df_loc_up)
                # Define a layer to display on a map
                layer = pdk.Layer(
        "ScatterplotLayer",
        df_loc_up,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position="Coordinates",
        get_radius=100,
        get_fill_color=[255, 140, 0],
        get_line_color=[0, 0, 0],
    )

                # Set the viewport location
                view_state = pdk.ViewState(latitude=lat, longitude=long, zoom=10, bearing=0, pitch=0)

                st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Address}"}))
                
                
                
                    
                    
                
                    
                    
         
                    
                        
       