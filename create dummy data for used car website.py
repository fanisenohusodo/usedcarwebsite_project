#Install library Faker
get_ipython().system('pip install Faker')
get_ipython().system('pip install tabulate')

#Import Library yang akan digunakan
from faker import Faker
from tabulate import tabulate
import random
from datetime import datetime, timedelta
import csv

#Definisikan bahwa data yang digunakan menggunakan format Indonesia
FAKER = Faker('id_ID')

#Buat function untuk menampilkan data
def show_data(table):
    tab = tabulate(tabular_data = table,
                   headers = table.keys(),
                   tablefmt = "psql",
                   numalign = "center")
    print(tab)

def csv_to_dict(filename):

    # buka file csv
    with open(f'{filename}', mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)

        # simpan dalam bentuk list of dictionary
        data = {}
        for row in csv_reader:
            for key, value in row.items():
                data.setdefault(key, []).append(value)

    return data

#Ekstrak file city.csv menjadi list of dictionary
city = csv_to_dict('city.csv')

#Menampilkan data tabel city
show_data(city)

def tabel_users (n_data, is_print):
    
    # mendefinisikan tanggal awal 
    start_date = datetime(2023, 6, 1)

    # mendefinisikan tanggal akhir 
    end_date = datetime(2023, 12, 31, 23, 59, 59)

    # Buat table
    table = {}
    table["user_id"] = [i+1 for i in range(n_data)]
    table["first_name"] = [FAKER.first_name() for i in range(n_data)]
    table["last_name"] = [FAKER.last_name() for i in range(n_data)]
    table["phone"] = [FAKER.phone_number() for i in range(n_data)]
    
    #Buat username berdasarkan kombinasi first name dan last name
    table["username"] = []
    for i in range(n_data):
        first_name = table["first_name"][i]  
        last_name = table["last_name"][i]
        email = f"{first_name}{last_name}_{FAKER.pyint()}"
        table["username"].append(email)
    
    #Buat email berdasarkan kombinasi first name dan last name
    table["email"] = []
    for i in range(n_data):
        first_name = table["first_name"][i].lower()  
        last_name = table["last_name"][i].lower()
        email = f"{first_name}_{last_name}{FAKER.pyint()}@{FAKER.free_email_domain()}"  
        table["email"].append(email)

    table["city_id"] = [random.choice(city['city_id']) for i in range(n_data)]
    table["password"] = [FAKER.password() for i in range(n_data)]
    table["joined_date"] = [FAKER.date_time_between(start_date=start_date, end_date=end_date) for i in range(n_data)]

    # Print table
    if is_print:
        show_data(table)

    return table

#Membuat 100 baris data tabel users
users = tabel_users(n_data = 100, is_print = True)

#Ekstrak file car_product.csv menjadi list of dictionary
product = csv_to_dict('car_product.csv')

#Menampilkan data tabel product
show_data(product)

def tabel_advertisement(n_data, is_print):
   
    # Mendefinisikan tanggal awal, minimal tanggal saat user terdaftar
    start_date = min(users["joined_date"])
    # Mendefinisikan tanggal akhir, maksimal tanggal hari ini 
    end_date = datetime.now()

    # Buat table
    table = {}
    table["adv_id"] = [i + 1 for i in range(n_data)]
    table["date_created"] = [FAKER.date_time_between(start_date=start_date, end_date=end_date) for i in range(n_data)]
    table["user_id_seller"] = [random.choice(users["user_id"]) for i in range(n_data)]
    table["product_id"] = [random.choice(product["product_id"]) for i in range(n_data)]
    table["title"] = [f"Dijual murah {product['model'][product['product_id'].index(i)]} 
                      {product['year'][product['product_id'].index(i)]}" for i in table["product_id"]]
    table["description"] = [f"Minat hubungi {users['phone'][users['user_id'].index(i)]}" for i in table["user_id_seller"]]
    table["sell_price"] = []    
    for product_id in table["product_id"]:  #Menetapkan harga maksimum dan minimum sesuai model mobil
        if product['model'][product['product_id'].index(product_id)] == "Toyota Yaris":
            sell_price = FAKER.random_int(124_000_000, 240_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)]  == "Toyota Agya":
            sell_price = FAKER.random_int(97_000_000, 155_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Toyota Calya":
            sell_price = FAKER.random_int(104_000_000, 137_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Daihatsu Ayla":
            sell_price = FAKER.random_int(83_000_000, 120_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)]  == "Daihatsu Terios":
            sell_price = FAKER.random_int(166_000_000, 223_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Daihatsu Xenia":
            sell_price = FAKER.random_int(100_000_000, 220_500_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Honda Jazz":
            sell_price = FAKER.random_int(178_000_000, 250_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Honda CR-V":
            sell_price = FAKER.random_int(116_000_000, 415_000_000, 10_000_000)
        elif product['model'][product['product_id'].index(product_id)] == "Honda Civic":
            sell_price = FAKER.random_int(186_000_000, 397_500_000, 10_000_000)
        else:
            sell_price = FAKER.random_int(100_000_000, 178_000_000, 10_000_000)
        table["sell_price"].append(sell_price)
    #Mendefinisikan fitur bid dengan 95% data memungkinkan fitur bid    
    table["can_bid"] = [FAKER.boolean(chance_of_getting_true = 95) for i in range(n_data)]
    
    # Print table
    if is_print:
        show_data(table)

    return table

#Membuat 400 baris data tabel advertisement
advertisement = tabel_advertisement(n_data = 400, is_print = True)

def tabel_search(n_data, is_print):
    
    # Mendefinisikan tanggal awal, minimal tanggal ketika advertisement dibuat
    start_date = min(advertisement["date_created"])
    # Mendefinisikan tanggal akhir, maksimal tanggal hari ini
    end_date = datetime.now()

    # Buat table
    table = {}
    table["search_id"] = [i + 1 for i in range(n_data)]
    table["date_created"] = [FAKER.date_time_between(start_date=start_date, end_date=end_date) for i in range(n_data)]
    table["adv_id"] = [random.choice(advertisement["adv_id"]) for i in range(n_data)]
                      
    # Print table
    if is_print:
        show_data(table)

    return table
 
#Membuat 700 baris data tabel product_search
product_search = tabel_search(n_data = 700, is_print = True)


def tabel_bid(n_data, is_print):
    
    # Mendefinisikan awal tanggal
    start_date = min(advertisement["date_created"])
    # Mendefinisikan akhir tanggal
    end_date = datetime.now()

    # Buat table
    table = {}
    table["bid_id"] = [i + 1 for i in range(n_data)]
    table["date_created"] = [FAKER.date_time_between(start_date=start_date, end_date=end_date) for i in range(n_data)]
    
    adv_ids = [random.choice(advertisement["adv_id"]) for i in range(n_data)]
    table["adv_id"] = adv_ids
    
    table["user_id_buyer"] = []
    for adv_id in adv_ids:
        #Ambil data user_id_seller
        used_user_ids = {advertisement["user_id_seller"][i] for i, aid in enumerate(advertisement["adv_id"]) if aid == adv_id}  
        #Daftar user_id tersedia karena user_id_buyer tidak boleh sama dengan user_id_seller
        available_user_ids = set(users["user_id"]) - used_user_ids
        #Pilih random user_id_buyer
        table["user_id_buyer"].append(random.choice(list(available_user_ids)))  
    
    # Mendefinisikan bid price
    min_prices = [0.5 * advertisement["sell_price"][advertisement["adv_id"].index(adv_id)] for adv_id in adv_ids]
    max_prices = [advertisement["sell_price"][advertisement["adv_id"].index(adv_id)] for adv_id in adv_ids]
    
    #Membuat looping bid price
    table["bid_price"] = []
    
    for adv_id in adv_ids:
        bid_price = None
        if advertisement['can_bid'][advertisement['adv_id'].index(adv_id)] == False:
            bid_price = max_prices[advertisement["adv_id"].index(adv_id)]  
            #jika tidak ada fitur can_bid, harga yang bisa dimasukkan = sell_price
        else:
            bid_price = FAKER.random_int(min=min_prices[advertisement["adv_id"].index(adv_id)],  
                                     max=max_prices[advertisement["adv_id"].index(adv_id)],  
                                     step=500_000)
        table["bid_price"].append(bid_price)  # Append the generated bid_price
    
    # Print table
    if is_print:
        show_data(table)

    return table
 
#Membuat 550 baris data tabel bid
bid = tabel_bid(n_data = 550, is_print = True)

def save_to_csv(data, nama_file):
    '''
    Fungsi untuk menyimpan data dummy ke csv

    args:
        - data (list)     : list of dictionary data yang akan dijadikan csv
        - nama_file (str) : nama untuk file csv

    return:
    - None
    '''
   
    # Membuat file csv
    with open(file = f"{nama_file}.csv", mode = 'w', newline = '') as csv_file:
        # Membuat writer csv
        writer = csv.writer(csv_file)

        # write header csv
        writer.writerow(list(data.keys()))
        
        # mengetahui panjang data
        len_data = len(list(data.items())[0][1])
        
        # write data ke file csv
        for i in range(len_data):
            row = []
            for key in data.keys():
                row.append(data[key][i])
            writer.writerow(row)

#export data user ke file csv
save_to_csv(data = users,
            nama_file = 'users')

#export data advertisement ke file csv
save_to_csv(data = advertisement,
            nama_file = 'advertisement')

#save data product_search ke file csv
save_to_csv(data = product_search,
            nama_file = 'product_search')

#save data bid ke file csv
save_to_csv(data = bid,
            nama_file = 'bid')

