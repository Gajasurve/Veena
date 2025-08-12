import requests
from bs4 import BeautifulSoup
import datetime
import os
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

LINK_DAY = "https://www.drikpanchang.com/telugu/panchanga/telugu-day-panchanga.html"
LOCATION = "1269843"  
def get_soup(url, params=None):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status() 
    return BeautifulSoup(response.content, 'html.parser')


def get_today_panchang():
    today = datetime.date.today()
    formatted_date = today.strftime("%d/%m/%Y")

    
    soup = get_soup(LINK_DAY, params={"geoname-id": LOCATION, "date": formatted_date})
    
    date_section = soup.find("div", {"class": "dpPHeaderRightContent"})
    if date_section:
        date = " ".join([x.text.strip() for x in date_section.contents if x.text.strip()])
    else:
        date = "Error: Date info not found"
    
    location_section = soup.find("div", {"class": "dpPHeaderLeftWrapper"})
    location = location_section.find_all("div")[-1].text.strip() if location_section else "Unknown Location"
    
    # Extract Panchang details (Tithi, Nakshatra, etc.)
    #Mo		Chandra				Cp 0°1'32''	4°39'39''	-16°44'34''		Uttarāṣāḍha(21) Su		2	Deva	1 // You were born under this. 
    #Mo		Chandra				Le 7°2'19''	-4°56'11''	6°34'6''		Maghā(10) Ke		3	Deva	3  // And i am under this.  
    panchang_table = soup.find("div", {"class": "dpTableCardWrapper"})
    if panchang_table:
        rows = panchang_table.find_all("div", {"class": "dpTableRow"})
        panchang_details = {}
        for row in rows:
            key = row.find("div", {"class": "dpTableKey"})
            value = row.find("div", {"class": "dpTableValue"})
            if key and value:
                panchang_details[key.text.strip()] = value.text.strip()
            else:
                print("\u0950")
    else:
        panchang_details = "Error: Panchang details not found"

    
    chandramasa_section = soup.find("div", string="Chandramasa")  
    if chandramasa_section:
        chandramasa = chandramasa_section.find_next("div").text.strip()
    else:
        chandramasa = "Not available"

    
    panchang_details['Chandramasa'] = chandramasa
    
    return {
        "date": date,
        "location": location,
        "panchang_details": panchang_details
    }

# Main function to fetch and print required Panchang data in one line
def print_panchang_details():
   
    today_data = get_today_panchang()
    
    
    panchang_details = today_data['panchang_details']

    
    today_date = datetime.datetime.today().strftime('%d %b %Y')
    
    
    output = (
        f"Today is {today_date}, "
        f"{panchang_details.get('Weekday', 'Not available')}, "
        f"{panchang_details.get('Tithulu', 'Not available')}, "
        f"and year {panchang_details.get('Vikram Samvat', 'Not available')} of "
        f"{panchang_details.get('Drik Ritu', 'Not available')}. "
        f"Brahma muhurtha is from {panchang_details.get('Brahma Muhurta', 'Not available')}. "
        f"Chandramasa is {panchang_details.get('Chandramasa', 'Not available')}"
    )
    
    
    print(output)

# Vishnu Shloka file paths and functions
vishnu_file = '/wwebjs-bot/Vishnu.txt'
status_file = '/wwebjs-bot/status.txt'

# Function to read all blocks (separated by "**") from Vishnu.txt
def read_shlokas(vishnu_file):
    with open(vishnu_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    
    blocks = content.split('**')
    
    
    blocks = [block.strip() for block in blocks if block.strip()]
    
    return blocks


def get_last_shloka_index(status_file):
    if os.path.exists(status_file):
        with open(status_file, 'r') as f:
            return int(f.read().strip())  
    else:
        return 0  # If no status file exists, start from the first block


def update_status(status_file, index):
    with open(status_file, 'w') as f:
        f.write(str(index))

# Function to print the current shloka block (from "*" to "*")
def print_shloka_block(shloka_block):
    # Print the entire block as-is
    print(shloka_block)


def print_shloka():

    shlokas = read_shlokas(vishnu_file)
    

    current_index = get_last_shloka_index(status_file)
    

    if current_index >= len(shlokas):
        current_index = 0  # Reset to the first block
    

    current_shloka_block = shlokas[current_index]
    

    print_shloka_block(current_shloka_block)
    

    update_status(status_file, current_index + 1)  

# Run both Panchang and Shloka functions
if __name__ == "__main__":
    try:
        # Print Panchang details
        print_panchang_details()
        print("\n\n\n")
        # Print Shloka
        print_shloka()
    
    except Exception as e:
        print(f"Error occurred: {e}")
#Most of the code was written by everyday eveving talks with jindyal, The abaondon shiva temple, Nagarkot, Nepal. 
