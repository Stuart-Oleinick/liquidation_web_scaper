from bs4 import BeautifulSoup
from tkinter import *
import csv
import os.path

def submitted(ment):
    textHTML = ment.get()
    processHTML(textHTML)

def clear(mE1):
    mE1.delete(0, 'end')

def makeBox():
    """Created an entry box that the user can submit html code into"""
    mGUI = Tk()
    ment=StringVar()
    mGUI.title('Enter paste html code here')
    mlabel2 = Label(mGUI,text="LIQUIDATION WEB SCRAPER").pack()
    mlabel = Label(mGUI,text="Paste html code below").pack()
    mEntry= Entry(mGUI,textvariable=ment)
    mEntry.pack()
    mbuttonSubmit = Button(mGUI,text="submit",command= lambda:submitted(ment),fg='red',bg='blue').pack()
    mbuttonClear = Button(mGUI,text="Clear",command= lambda:clear(mEntry),fg='red').pack()

def write_to_csv(item_info):
    #print("HERE")
    if os.path.exists('liquidation_data.csv') == False:
        with open('liquidation_data.csv', 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(item_info.keys())

    with open('liquidation_data.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(item_info.values())

def processHTML(user_input):
	soup = BeautifulSoup(user_input, 'html.parser')

	item_info_t = {}

	#this is where i get all of the data from the html code

	#Gathering a table that has some info in it
	column_names = soup.find("div",attrs={"class":"col-sm-6","id":"auctionData"}).find_all("div",attrs={"class":"col-xs-4"})
	column_names = [name.text.strip().lower() for name in column_names ]

	column_data = soup.find("div",attrs={"class":"col-sm-6","id":"auctionData"}).find_all("div",attrs={"class":"col-xs-8"})
	column_data = [data.text.strip() for data in column_data ]

	for index in range(min(len(column_data),len(column_names))):
		item_info_t[column_names[index]] = column_data[index]
	#end of first table
	

	#this is the collapsable shipping 
	shipping_info_table = soup.find("div",attrs={"class":"row panel-group","id":"auctionDataAccordion2"}).find("div",attrs={"class":"col-sm-12"})
	
	shipping_info_table_names = shipping_info_table.find_all("div",attrs={"class":"col-sm-3"})
	shipping_info_table_names = [name.text.strip().lower() for name in shipping_info_table_names]

	shipping_info_table_data = shipping_info_table.find_all("div",attrs={"class":"col-sm-9"})
	shipping_info_table_data = [data.text.strip() for data in shipping_info_table_data]

	for index in range(min(len(shipping_info_table_names),len(shipping_info_table_data))):
		item_info_t[shipping_info_table_names[index]] = shipping_info_table_data[index]
	#end of shipping 

	#auctionStats table
	auction_stats=  soup.find("div",attrs={"class":"row","id":"auctionStats"})
	auction_stats_columns = auction_stats.find_all("div",attrs={"class":"col-xs-3 bg-info"})
	auction_stats_columns = [column.text.strip() for column in auction_stats_columns]
	mid = int(len(auction_stats_columns)/2)
	
	auction_stats_data = auction_stats_columns[mid:]
	auction_stats_columns = auction_stats_columns[:mid]
	auction_stats_columns = [column.lower() for column in auction_stats_columns]
	
	for i in range(mid):
		item_info_t[auction_stats_columns[i]] = auction_stats_data[i]



	#product description table
	product_description = soup.find("div",attrs={"class":"row panel-group","id":"auctionDataAccordion1"}).find("div",attrs={"class":"content", "id":"description_table" ,"itemprop":"description"} ).text.split('\n')[2].split('-')
	
	#print(product_description)

	category = product_description[0].strip()
	product_name = product_description[1].strip()
	retail_price = product_description[2].split()[1].strip()

	item_info_t['category'] = category
	item_info_t['product_name'] = product_name
	item_info_t['retail_price'] = retail_price
	

	for key in item_info_t.items():
		print(key)

	#auction end time
	try:
		auction_end = item_info_t['time left'].split()
		auction_end_date = auction_end[2]
		auction_end_time = " ".join(auction_end[3:5])
	except:
		auction_end_date = ''
		auction_end_time = ''

	#current bid
	try:
		current_bid = item_info_t['winning bid'].split('\n')[0]
		item_info_t['current_bid'] = current_bid
	except:
		current_bid = ''
		item_info_t['current_bid'] = current_bid

	#bid no bid 
	try:
		if int(item_info_t['bids'])>0:
			bid_no_bid = 1
		else:
			bid_no_bid = 0
	except:
		bid_no_bid = 0

	#bid retail

	try:
		bid_retail = float(item_info_t['bids'])/float(item_info_t['retail_price'].replace('$','').replace(',',''))

	except:
		bid_retail = ''
	

	item_info = {}
	#making the item info table########################
	item_info['auction_id'] = item_info_t['auction id']
	item_info['product_name'] = item_info_t['product_name']
	item_info['category'] = item_info_t['category']
	item_info['cepa'] = '' ####
	item_info['bf'] = '' ####
	item_info['retail_price'] = item_info_t['retail_price']
	item_info['current_bid_ammount'] = item_info_t['current_bid']
	item_info['bid_number'] = item_info_t['bids']
	item_info['bid_no_bid'] = bid_no_bid
	item_info['bid_retail'] = bid_retail
	item_info['units'] = item_info_t['quantity in lot'].split()[0]
	item_info['price_per_unit'] = '' ####
	item_info['condition'] = item_info_t['condition']
	item_info['auction_end_date'] = auction_end_date
	item_info['auction_end_time'] = auction_end_time
	item_info['shipping_cost'] = item_info_t['minimum shipping fee']
	item_info['shiping_info'] = '' ####
	item_info['seller_membership_length'] = '' ####
	item_info['ninety_day_completed_transactions'] = ''
	item_info['twelve_month_completed_transactions'] = ''
	item_info['ninety_day_purchases_from_repeat_buyers'] = ''
	item_info['twelve_month_purchases_from_repeat_buyers'] = ''
	item_info['ninety_day_buyer_dispute_rate'] = ''
	item_info['twelve_month_buyer_dispute_rate'] = ''
	item_info['ninety_day_unresolved_dispute_rate'] = ''
	item_info['twelve_month_unresolved_dispute_rate'] = ''
	item_info['location'] = item_info_t['location']
	item_info['seller'] = item_info_t['seller'].split('\n')[0]
	item_info['shipping_terms'] = item_info_t['shipping terms'].split('\n')[0]
	item_info['total_weight'] = item_info_t['total weight']
	item_info['buyers_premium'] = item_info_t["buyer's premium"]
	item_info['auction_type'] = item_info_t['auction type']
	item_info['zip_code'] = item_info_t['zip code']
	item_info['size_classification'] = item_info_t['size classification']
	item_info['available_lots'] = item_info_t['available lot(s)']
	item_info['shipping_restrictions'] = item_info_t['shipping restrictions']
	item_info['views'] = item_info_t['views']
	item_info['bidders'] = item_info_t['bidders']
	item_info['watching'] = item_info_t['watching']


	###################################################


	for item in item_info.items():
		print(item)

	write_to_csv(item_info)
        
makeBox()
