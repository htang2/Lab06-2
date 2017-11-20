import string,random,time,azurerm,json
from azure.storage.table import TableService, Entity

# Define variables to handle Azure authentication
auth_token = azurerm.get_access_token_from_cli()
subscription_id = azurerm.get_subscription_from_cli()

# Define variables with random resource group and storage account names
resourcegroup_name = 'htang'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
storageaccount_name = 'htang'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
location = 'eastus'

###
# Create the a resource group for our demo
# We need a resource group and a storage account. A random name is generated, as each storage account name must be globally unique.
###
response = azurerm.create_resource_group(auth_token, subscription_id, resourcegroup_name, location)
if response.status_code == 200 or response.status_code == 201:
    print('Resource group: ' + resourcegroup_name + ' created successfully.')
else:
    print('Error creating resource group')

# Create a storage account for our demo
response = azurerm.create_storage_account(auth_token, subscription_id, resourcegroup_name, storageaccount_name,  location, storage_type='Standard_LRS')
if response.status_code == 202:
    print('Storage account: ' + storageaccount_name + ' created successfully.')
    time.sleep(2)
else:
    print('Error creating storage account')


###
# Use the Azure Storage Storage SDK for Python to create a Table
###
print('\nLet\'s create an Azure Storage Table to store some data.')
input('Press Enter to continue...')

# Each storage account has a primary and secondary access key.
# These keys are used by aplications to access data in your storage account, such as Tables.
# Obtain the primary storage access key for use with the rest of the demo

response = azurerm.get_storage_account_keys(auth_token, subscription_id, resourcegroup_name, storageaccount_name)
storageaccount_keys = json.loads(response.text)
storageaccount_primarykey = storageaccount_keys['keys'][0]['value']

# Create the Table with the Azure Storage SDK and the access key obtained in the previous step
table_service = TableService(account_name=storageaccount_name, account_key=storageaccount_primarykey)
response = table_service.create_table('htangitemstable')
if response == True:
    print('Storage Table: htangitemstable created successfully.\n')
else:
    print('Error creating Storage Table.\n')

time.sleep(1)


###
# Use the Azure Storage Storage SDK for Python to create some entries in the Table
###
print('Now let\'s add some entries to our Table.\nRemember, Azure Storage Tables is a NoSQL datastore, so this is similar to adding records to a database.')
input('Press Enter to continue...')

# Each entry in a Table is called an 'Entity'. 
# Here, we add five entries for cars with five pieces of data: 1) make, 2) model, 3) year, 4) color, 5) price
#
# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. This makes queries much quicker.

cars = Entity()
cars.PartitionKey = 'car_selections'
cars.RowKey = '001'
cars.make = 'Volkswagen'
cars.model = 'Jetta'
cars.year = 2010
cars.color = 'silver'
cars.price = 13300
table_service.insert_entity('htangitemstable', cars)
print('Created entry for Volkswagen/Jetta...')

cars = Entity()
cars.PartitionKey = 'car_selections'
cars.RowKey = '002'
cars.make = 'Ford'
cars.model = 'Focus'
cars.year = 2011
cars.color = 'white'
cars.price = 13600
table_service.insert_entity('htangitemstable', cars)
print('Created entry for Ford/Focus...')

cars = Entity()
cars.PartitionKey = 'car_selections'
cars.RowKey = '003'
cars.make = 'Toyota'
cars.model = 'Corolla'
cars.year = 2013
cars.color = 'black'
cars.price = 10300
table_service.insert_entity('htangitemstable', cars)
print('Created entry for Toyota/Corolla...\n')

cars = Entity()
cars.PartitionKey = 'car_selections'
cars.RowKey = '004'
cars.make = 'Renault'
cars.model = 'Laguna'
cars.year = 2015
cars.color = 'blue'
cars.price = 14700
table_service.insert_entity('htangitemstable', cars)
print('Created entry for Renault/Laguna...\n')

cars = Entity()
cars.PartitionKey = 'car_selections'
cars.RowKey = '005'
cars.make = 'Alfa Romeo'
cars.model = '159'
cars.year = 2017
cars.color = 'red'
cars.price = 17000
table_service.insert_entity('htangitemstable', cars)
print('Created entry for Alfa Romeo/159...\n')


# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. This makes queries much quicker.

coffee = Entity()
coffee.PartitionKey = 'coffeemenu'
coffee.RowKey = '006'
coffee.brand = 'Starbucks'
coffee.flavor = 'Balanced and nutty'
coffee.size = 'tall'
coffee.price = 2.95
table_service.insert_entity('htangitemstable', coffee)
print('Created entry for Starbucks...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeemenu'
coffee.RowKey = '007'
coffee.brand = 'Maxwell House'
coffee.flavor = 'French vanilla'
coffee.size = 'grande'
coffee.price = 3.95
table_service.insert_entity('htangitemstable', coffee)
print('Created entry for Maxwell House...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeemenu'
coffee.RowKey = '008'
coffee.brand = 'Philz'
coffee.flavor = 'Dark chocolate'
coffee.size = 'mini'
coffee.price = 4.00
table_service.insert_entity('htangitemstable', coffee)
print('Created entry for Philz...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeemenu'
coffee.RowKey = '009'
coffee.brand = 'Folgers'
coffee.flavor = 'Dark roast'
coffee.size = 'venti'
coffee.price = 4.45
table_service.insert_entity('htangitemstable', coffee)
print('Created entry for Folgers...\n')
time.sleep(1)

coffee = Entity()
coffee.PartitionKey = 'coffeemenu'
coffee.RowKey = '010'
coffee.brand = 'Nescafe'
coffee.flavor = 'Classic roast'
coffee.size = 'grande'
coffee.price = 3.95
table_service.insert_entity('htangitemstable', coffee)
print('Created entry for Nescafe...\n')
time.sleep(1)

###
# Use the Azure Storage Storage SDK for Python to query for entities in our Table
###
print('With some data in our Azure Storage Table, we can query the data.\nLet\'s see what the car selection looks like.')
input('Press Enter to continue...')

# In this query, you define the partition key to search within, and then which properties to retrieve
# Structuring queries like this improves performance as your application scales up and keeps the queries efficient
items = table_service.query_entities('htangitemstable', filter="PartitionKey eq 'car_selections'", select='make,model,year,color,price')
for item in items:
    print('Make: ' + item.make)
    print('Model: ' + item.model)
    print('Year: ' + str(item.year) + '\n')
    print('Color: ' + item.color)
    print('Price: ' + str(item.price) + '\n')

items = table_service.query_entities('htangitemstable', filter="PartitionKey eq 'coffeemenu'", select='brand,flavor,size,price')
for item in items:
    print('Brand: ' + item.brand)
    print('Flavor: ' + item.flavor)
    print('Size: ' + item.size)
    print('Price: ' + str(item.price) + '\n')

time.sleep(1)


###
# This was a quick demo to see Tables in action.
# Although the actual cost is minimal (fractions of a cent per month) for the three entities we created, it's good to clean up resources when you're done
###
print('\nThis is a basic example of how Azure Storage Tables behave like a database.\nTo keep things tidy, let\'s clean up the Azure Storage resources we created.')
input('Press Enter to continue...')

response = table_service.delete_table('htangitemstable')
if response == True:
    print('Storage table: htangitemstable deleted successfully.')
else:
    print('Error deleting Storage Table')

response = azurerm.delete_resource_group(auth_token, subscription_id, resourcegroup_name)
if response.status_code == 202:
    print('Resource group: ' + resourcegroup_name + ' deleted successfully.')
else:
    print('Error deleting resource group.')

