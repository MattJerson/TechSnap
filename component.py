import pandas as pd
import numpy as np

cpu_path = 'csv/cpu.csv'  # Replace with your CSV file path
ram_path = 'csv/memory.csv'
psu_path = 'csv/power-supply.csv'
gpu_path = 'csv/video-card.csv'
mobo_path = 'csv/motherboard.csv'
storage_path = 'csv/internal-hard-drive.csv'

def ramfunc(budget, selectedoption):
    table = []
    # Reading the CSV file using pandas
    data = pd.read_csv(ram_path)

    # Calculating 'price' multiplied by 50
    data['price_peso'] = data['price'] * 50
    data['peso_per_gb'] = data['price_per_gb'] * 50

    # Filtering rows with price below the budget
    fildata = data[data['price_peso'] <= budget].copy()

    # Splitting and formatting 'speed', 'price_peso', 'peso_per_gb' column
    fildata['speed'] = fildata['speed'].astype(str).str.replace(',', '')
    #fildata['speed'] = 'DDR' + fildata['speed'].str[0] + '-' + fildata['speed'].str[1:] + 'mhz'
    fildata['ddrver'] = 'DDR' + fildata['speed'].str[0]
    fildata['speed'] = fildata['speed'].astype(str).apply(lambda x: x[1:]) + 'mhz'

    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)
    #fildata['peso_per_gb'] = '₱' + fildata['peso_per_gb'].astype(str)
    #fildata['peso_per_gb'] = round(fildata['peso_per_gb'], 2)
    fildata['peso_per_gb'] = fildata['peso_per_gb'].apply(lambda x: '₱' + str(round(x, 2)))

    # Filtering data based on the selectedoption
    if selectedoption:
        fildata = fildata[fildata['ddrver'] == selectedoption]

    # Sorting data based on 'speed' and 'modules'
    sorted_data = fildata.sort_values(by=['ddrver','speed', 'modules'], ascending=False)

    # Displaying the top 10 rows with highest 'speed' and 'modules' within the budget
    top_10 = sorted_data.head(10)
    
    # Converting the top 10 rows to dictionaries and appending to a list
    for _, row in top_10.iterrows():
        data_dict = {
            'name': row['name'],
            'price_peso': '₱' + str(row['price_peso']),
            'ddrver': row['ddrver'],
            'speed': row['speed'],
            'modules': row['modules'],
            'peso_per_gb': row['peso_per_gb']
            
        }
        table.append(data_dict)

    return table

def cpufunc(budget, selectedoption):
    table = []
    data = pd.read_csv(cpu_path)
    data['price_peso'] = data['price'] * 50
    data['performance'] = data['core_clock'] * data['core_count']

    fildata = data[data['price_peso'] <= budget].copy()

    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)
    fildata['performance'] = round(fildata['performance'], 2)

    # Extracting brand information and adding it to a new 'brand' column
    fildata['brand'] = np.where(fildata['name'].str.contains('AMD', case=False), 'AMD',
                            np.where(fildata['name'].str.contains('Intel', case=False), 'Intel', 'Other'))
    
    # Filtering data based on the selectedoption
    if selectedoption:  
        fildata = fildata[fildata['brand'] == selectedoption]

    sorted_data = fildata.sort_values(by=['core_clock', 'core_count'], ascending=False)
    ten = sorted_data.head(10)
    
    for _, row in ten.iterrows():
        data_dict = {
            'name': row['name'],
            'price_peso': '₱' + str(row['price_peso']),
            'core_clock': str(row['core_clock']) + 'GHz',
            'core_count': row['core_count'],
            'performance': row['performance']
        }
        table.append(data_dict)
    return table


def gpufunc(budget, selectedoption):
    table = []
    data = pd.read_csv(gpu_path)
    data['price_peso'] = data['price'] * 50

    fildata = data[data['price_peso'] <= budget].copy()
    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)

    # Function to identify brand from 'chipset' column
    def get_brand(chipset):
        brands = ['GeForce', 'Radeon', 'VEGA', 'Arc', 'Quadra', 'FirePro ', 'RTX', 'Ada Generation']
        for brand in brands:
            if brand in str(chipset):
                return brand
        return 'Other'  # If no matching brand is found

    # Apply get_brand function to create a new 'brand' column
    fildata['brand'] = fildata['chipset'].apply(get_brand)

    # Filtering data based on the selectedoption
    if selectedoption:  
        fildata = fildata[fildata['brand'] == selectedoption]

    sorted_data = fildata.sort_values(by=['memory', 'core_clock', 'boost_clock'], ascending=False)
    ten = sorted_data.head(10)
    for _, row in ten.iterrows():
        data_dict = {
            'name': row['name'],
            'chipset': row['chipset'],
            'price_peso': '₱' + str(row['price_peso']),
            'memory': row['memory'],
            'core_clock': row['core_clock'],
            'brand': row['brand'], #checking if get_brand is working
            'boost_clock': row['boost_clock']
        }
        table.append(data_dict)
    return table


def psufunc(budget, selectedoption):
    table = []
    data = pd.read_csv(psu_path)
    data['price_peso'] = data['price'] * 50

    fildata = data[data['price_peso'] <= budget].copy()
    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)

    # Filtering data based on the selectedoption
    if selectedoption:
        fildata = fildata[fildata['type'] == selectedoption]

    sorted_data = fildata.sort_values(by=['efficiency', 'price_peso', 'wattage'], ascending=False)
    ten = sorted_data.head(10)
    for _, row in ten.iterrows():
        data_dict = {
            'name': row['name'],
            'price_peso': '₱' + str(row['price_peso']),
            'efficiency': row['efficiency'],
            'wattage': row['wattage'],
            'type': row['type'],
            'modular': row['modular']
        }
        table.append(data_dict)
    return table

def mobofunc(budget, selectedoption):
    table = []
    data = pd.read_csv(mobo_path)
    data['price_peso'] = data['price'] * 50

    fildata = data[data['price_peso'] <= budget].copy()
    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)

    # Filtering data based on the selectedoption
    if selectedoption:
        fildata = fildata[fildata['form_factor'] == selectedoption]

    sorted_data = fildata.sort_values(by=['memory_slots', 'max_memory'], ascending=False)
    ten = sorted_data.head(10)
    for _, row in ten.iterrows():
        data_dict = {
            'name': row['name'],
            'price_peso': '₱' + str(row['price_peso']),
            'memory_slots': row['memory_slots'],
            'max_memory': row['max_memory'],
            'socket': row['socket'],
            'form_factor': row['form_factor']
        }
        table.append(data_dict)
    return table

def storfunc(budget, selectedoption):
    table = []
    data = pd.read_csv(storage_path)
    data['price_peso'] = data['price'] * 50

    fildata = data[data['price_peso'] <= budget].copy()
    fildata['price_peso'] = round(fildata['price_peso'], 2).astype(str)

    def modify_capacity(row):
        if row['type'] != 'SSD':
            return f'HDD-{row["type"]}rpm'
        return row['type']
    fildata['type'] = fildata.apply(modify_capacity, axis=1)

    # Filtering data based on the selectedoption
    if selectedoption:
        fildata = fildata[fildata['type'] == selectedoption]

    sorted_data = fildata.sort_values(by=['capacity', 'type', 'price_peso'], ascending=False)
    ten = sorted_data.head(10)
    for _, row in ten.iterrows():
        data_dict = {
            'name': row['name'],
            'price_peso': '₱' + str(row['price_peso']),
            'type': row['type'],
            'capacity': row['capacity'],
            'interface': row['interface']
        }
        table.append(data_dict)
    return table