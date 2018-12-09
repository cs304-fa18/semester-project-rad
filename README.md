
# Project Overview

Resource Aid Directory (RAD) is an application which stores information and
data about resources and expenditures. 

# Feature Documentation

## 3.  Donation Table Page (copied from README.md):
 This page displays all the donations in the donation table. By selecting a donation type on the drop down menu, users can filter donations by type.
 
 Run: `python search_donation_history.py`
 URL: /donations/
 http://private-arivera4-arivera4.c9users.io:8081/donations/

 Browser Navigation: Home page →  Search through donations
 Inputs: Filter Drop Down, Donation Table
 
 
 Filter Drop Down: The donations types are listed below
 Food: Many varieties, both fresh and canned
 Medical: Any medicine, first aid kits, doctor’s supplies
 Clothes: Includes shoes, jackets, etc. 
 Supplies: Any supplies for kitchen, bedding, toiletries
 Money: Donations in any currency
 Other: Anything other than hard-coded types above
 Donation Table:
 Date of Submission: date of submission 
 Amount: Integer describing quantity of donation 
 Type: Category of inventory item, types listed above in drop down 

 Future versions will:
 Add a units attribute to the donations table, so that users can specify the currency if the donation is money 
 (Ex: 100 kuna of money) or units of food 
 (Ex: bushels of corn) or toiletries (Ex: 3.4 oz. lotion)
 Figure out how to display the description attribute of the donation table on the web page (Currently does not display due to syntax error)


## 3.  Donation Table Page
 This page displays all the donations in the donation table. By selecting a donation type on the drop down menu, users can filter donations by type.
 
 Run: `python search_donation_history.py`
 URL: /donations/
 http://private-arivera4-arivera4.c9users.io:8081/donations/

 Browser Navigation: Home page →  Search through donations
 Inputs: Filter Drop Down, Donation Table
 
 
 Filter Drop Down: The donations types are listed below
 Food: Many varieties, both fresh and canned
 Medical: Any medicine, first aid kits, doctor’s supplies
 Clothes: Includes shoes, jackets, etc. 
 Supplies: Any supplies for kitchen, bedding, toiletries
 Money: Donations in any currency
 Other: Anything other than hard-coded types above
 Donation Table:
 Date of Submission: date of submission 
 Amount: Integer describing quantity of donation 
 Type: Category of inventory item, types listed above in drop down 

 Future versions will:
 Add a units attribute to the donations table, so that users can specify the currency if the donation is money 
 (Ex: 100 kuna of money) or units of food 
 (Ex: bushels of corn) or toiletries (Ex: 3.4 oz. lotion)
 Figure out how to display the description attribute of the donation table on the web page (Currently does not display due to syntax error)

## 4.  Inventory Table Page (copied from README.md):
This page displays all the items in the inventory table. By selecting an item type on the drop down menu, users can search for inventory items by type.
Run: `python search_inventory_history.py`
URL: /inventory/
http://private-arivera4-arivera4.c9users.io:8081/inventory/
 
Browser Navigation: Home page →  Explore inventory
Inputs: Filter Drop Down, Inventory Table
 
Filter Drop Down: The inventory types listed below 
*** These inventory types are identical to donation types except there is no money type because it will be in its own separate table in the future called “Expenditures” 
Food: Many varieties, both fresh and canned
Medical: Any medicine, first aid kits, doctor’s supplies
Clothes: Includes shoes, jackets, etc. 
Supplies: Any supplies for kitchen, bedding, toiletries
Other: Anything other than hard-coded types above
Inventory Table:
Item Name: Name of the item along with its unit
Type: Category of inventory item, types listed above in drop down
Status: Integer describing quantity of donation 
(Ex: Eggs has status of 24 meaning there are 24 eggs while blankets have status of 12 meaning there are 12 blankets, so eggs have a higher status than blankets which means there is less need for eggs)
Future versions will:
Change the ‘status’ attribute to be a string set (either low, medium, high) which depends on a new amount attribute (quantity of inventory item)
Not only filter inventory by type, but also filter by inventory name, donor name, donation date and amount
Will display description on the inventory web page and add units as a new attribute to the inventory table (Similar to donations table future task)

- Select Donation Category
 
 Future versions will:
- Allow for donor selection from a dropdown menu containing all donors, 
which will automatically populate the known fields

- Respond with more useful feedback after updates

- Validate data entered by user (amount must be an integer, validity of
    phone number, email, XSS safety, etc.)

