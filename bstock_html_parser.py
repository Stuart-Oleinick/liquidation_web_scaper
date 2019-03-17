from bs4 import BeautifulSoup
from tkinter import *
import csv
import os.path


def submitted(ment):
    textHTML = ment.get()
    processHTML(textHTML)

def clear(mE1):
    mE1.delete(0, 'end')

def create_auction_details_dict(categories,data):
    auction_details_dict = {}
    for i in range(len(categories)):
        auction_details_dict[categories[i].text.strip().lower()] = data[i].text

    return auction_details_dict

def parse_seller_profile_table(seller_profile_table):
    table = {}
    for row in seller_profile_table.findAll('tr'):
        header = row.find('th').text
        header.strip()
        col = row.findAll('td')
        col = [val.text for val in col]
        #print(col)
        if col == []:
            continue
        table[header] = {}
        table[header]['90_Day'] = col[0]
        table[header]['12_Month'] = col[1]

    return table


def write_to_csv(item_info):
    if os.path.exists('bstock_data.csv') == False:
        with open('bstock_data.csv', 'a',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(item_info.keys())

    with open('bstock_data.csv', 'a',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(item_info.values())


def processHTML(user_input):
    soup = BeautifulSoup(user_input, 'html.parser')

    item_info = {}

    #this is where i get all of the data from the html code

    #auction id

    try:
        auction_id = soup.find('input', {'id': 'auction_id'}).get('value')

    except:
        auction_id = ''


    #auction end time
    try:
        auction_end = soup.find("span", id="auction_end_time").text.strip().split()
        auction_end_date = ' '.join(auction_end[0:4])
        auction_end_time = ' '.join(auction_end[4:])
    except:
        auction_end_date = ''
        auction_end_time = ''

    #current bid ammount
    try:
        current_bid_amount = soup.find("span", id="current_bid_amount").text.strip()
    except:
        current_bid_amount = ''

    #product_name
    try:
        product_name = soup.find('div', {'class' :'product-name'}).text.strip()

    except:
        product_name = ''


    #auction details to get condition and shipping info
    try:
        auction_details_categories =soup.find('div', {'class' :'auction-details'}).find_all('dt') #these are the categories for the auction details
        auction_details_data =soup.find('div', {'class' :'auction-details'}).find_all('dd') #this is the data from the auction details

        auction_details_dict = create_auction_details_dict(auction_details_categories,auction_details_data)

        condition = auction_details_dict['condition']

    except:
        condition = ''


    #shipping info
    try:
        auction_details_categories =soup.find('div', {'class' :'auction-details'}).find_all('dt') #these are the categories for the auction details
        auction_details_data =soup.find('div', {'class' :'auction-details'}).find_all('dd') #this is the data from the auction details

        auction_details_dict = create_auction_details_dict(auction_details_categories,auction_details_data)
        shipping_info = auction_details_dict['shipping'].strip()
    except:
        shipping_info = ''

    try:
        auction_details_categories =soup.find('div', {'class' :'auction-details'}).find_all('dt') #these are the categories for the auction details
        auction_details_data =soup.find('div', {'class' :'auction-details'}).find_all('dd') #this is the data from the auction details

        auction_details_dict = create_auction_details_dict(auction_details_categories,auction_details_data)
        description = auction_details_dict['description'].strip()
    except:
        description = ''




    #retail price
    try:
        retailPrice = soup.find('input', {'id': 'retailPrice'}).get('value')
    except:
        retailPrice = ''

    #category
    try:
        category = soup.find('input', {'id': 'categoryName'}).get('value')

        category_lower = category.lower()
        cepa_words = "computers electronics cell phones accesssories"
        bf_words = "books fashion"

        cepa = 0
        bf = 0
        for word in category_lower.split():
            if word in cepa_words:
                cepa = 1
            if word in bf_words:
                bf = 1
    except:
        category = ''
        cepa = 0
        bf = 0

    #units
    try:
        units = soup.find('input', {'id': 'productUnits'}).get('value')
    except:
        units = ''

    #price per unit
    try:
        price_per_unit = soup.find('input', {'id': 'pricePerUnitOrigin'}).get('value')
    except:
        price_per_unit = ''

    #bid number
    try:
        bid_number = soup.find("span", id="bid_number").text.strip()
        if int(bid_number) >0:
            bid_no_bid = 1
        else:
            bid_no_bid = 0
    except:
        bid_number = ''
        bid_no_bid = 0

    #bid retail
    try:
        bid_retail = int(bid_number)/int(retailPrice)
    except:
        bid_retail = 0

    #shipping cost
    try:
        shipping_cost =  soup.find("span", id="shipping_cost").text.strip()
    except:
        shipping_cost = ''

    #seller length membership
    try:
        seller_membership_length = soup.find('div', {'class' :'seller-membership-length'}).text.strip()
    except:
        seller_membership_length = ''

    #all of the seller profile
    try:
        seller_profile_table = soup.find("table", {"class" : "table table-condensed table-hover table-striped"})
        seller_profile_table = parse_seller_profile_table(seller_profile_table)

        ninety_day_completed_transactions = seller_profile_table['Completed Transactions ']['90_Day']
        twelve_month_completed_transactions = seller_profile_table['Completed Transactions ']['12_Month']
        ninety_day_purchases_from_repeat_buyers = seller_profile_table['Purchases from Repeat Buyers ']['90_Day']
        twelve_month_purchases_from_repeat_buyers = seller_profile_table['Purchases from Repeat Buyers ']['12_Month']
        ninety_day_buyer_dispute_rate = seller_profile_table['Buyer Dispute Rate ']['90_Day']
        twelve_month_buyer_dispute_rate = seller_profile_table['Buyer Dispute Rate ']['12_Month']
        ninety_day_unresolved_dispute_rate = seller_profile_table['Unresolved Dispute Rate ']['90_Day']
        twelve_month_unresolved_dispute_rate = seller_profile_table['Unresolved Dispute Rate ']['12_Month']
    except:
        ninety_day_completed_transactions = ''
        twelve_month_completed_transactions = ''
        ninety_day_purchases_from_repeat_buyers = ''
        twelve_month_purchases_from_repeat_buyers = ''
        ninety_day_buyer_dispute_rate = ''
        twelve_month_buyer_dispute_rate = ''
        ninety_day_unresolved_dispute_rate = ''
        twelve_month_unresolved_dispute_rate = ''
        twelve_month_unresolved_dispute_rate = ''


    ###################################################################################################


    #creating the dictionary that has all of the data within it	#######################################
    item_info['auction_id'] = auction_id
    item_info['product_name'] = product_name
    item_info['category'] = category
    item_info['cepa'] = cepa
    item_info['bf'] = bf
    item_info['retail_price'] = retailPrice
    item_info['current_bid_ammount'] = current_bid_amount
    item_info['bid_number'] = bid_number
    item_info['bid_no_bid'] = bid_no_bid
    item_info['bid_retail'] = bid_retail
    item_info['units'] = units
    item_info['price_per_unit'] = price_per_unit
    item_info['condition'] = condition
    item_info['auction_end_date'] = auction_end_date
    item_info['auction_end_time'] = auction_end_time
    item_info['shipping_cost'] = shipping_cost
    item_info['shiping_info'] = shipping_info
    item_info['seller_membership_length'] = seller_membership_length
    item_info['ninety_day_completed_transactions'] = ninety_day_completed_transactions
    item_info['twelve_month_completed_transactions'] = twelve_month_completed_transactions
    item_info['ninety_day_purchases_from_repeat_buyers'] = ninety_day_purchases_from_repeat_buyers
    item_info['twelve_month_purchases_from_repeat_buyers'] = twelve_month_purchases_from_repeat_buyers
    item_info['ninety_day_buyer_dispute_rate'] = ninety_day_buyer_dispute_rate
    item_info['twelve_month_buyer_dispute_rate'] = twelve_month_buyer_dispute_rate
    item_info['ninety_day_unresolved_dispute_rate'] = ninety_day_unresolved_dispute_rate
    item_info['twelve_month_unresolved_dispute_rate'] = twelve_month_unresolved_dispute_rate
    item_info['location'] = ''
    item_info['seller'] = ''
    item_info['shipping_terms'] = ''
    item_info['total_weight'] = ''
    item_info['buyers_premium'] = ''
    item_info['auction_type'] = ''
    item_info['zip_code'] = ''
    item_info['size_classification'] = ''
    item_info['available_lots'] = ''
    item_info['shipping_restrictions'] = ''
    item_info['views'] = ''
    item_info['bidders'] = ''
    item_info['watching'] = ''
    item_info['description'] = description
    ####################################################################################################


    #print(product_image_count)
    for key,val in item_info.items():
        print('\n{}: {}'.format(key,val))


    if auction_id:
        write_to_csv(item_info)

def makeBox():
    """Created an entry box that the user can submit html code into"""
    mGUI = Tk()
    ment=StringVar()
    mGUI.title('Enter paste html code here')
    mlabel2 = Label(mGUI,text="BSTOCK WEB SCRAPER").pack()
    mlabel = Label(mGUI,text="Paste html code below").pack()
    mEntry= Entry(mGUI,textvariable=ment)
    mEntry.pack()
    mbuttonSubmit = Button(mGUI,text="submit",command= lambda:submitted(ment),fg='red',bg='blue').pack()
    mbuttonClear = Button(mGUI,text="Clear",command= lambda:clear(mEntry),fg='red').pack()


makeBox()


#-----------UNDONE------------#
#number of images
#company selling
#manufacturer(this is part of the javascript)
#whats bidretail
#-----------------------------#


#------------DONE-------------#
#get category name(categoryName)
#number of units(productUnits)
#price per item
#retail price (id=retailPrice)
#condition (new or used is most important)
#all the product description
#product title
#seperate date and time
#number of bids
#get auction id
#get bid no bid
#seller-membership-length (i can for sure get this)
#shipping ammount and zip code
#------------DONE-------------#
