# Project Overview

Resource Aid Directory (RAD) is an application which stores information and
data about resources and expenditures. 

# Feature Documentation

## Donation Form

URL: `/donation-form`

 <draft version> This feature allows users to add new donations and donors to
 the database tables. Upon successful submission, it flashes the IDs of the new
 table rows as confirmation.
 
 Inputs: 
 
 Donor:
    - Type: Select between individual or organization, whichever is a more
    suitable description
    - Name
    - Phone
    - Address
    - Email
    - Description: Any other notes or information about this donor that can be
    stored in the database instead of passed between the 'institutional memory,'
    ex: 'Youth Group from Hogwarts School'
    
 Donation:
    - Donation Description: Nature of the donation, ex: 'Bandages', 'Blankets',
    'Carrots (lbs)'
    - Amount: Integer describing quantity of donation
    - Select Donation Category
 
 Future versions will:
    - Allow for donor selection from a dropdown menu containing all donors, 
    which will automatically populate the known fields
    
    - Respond with more useful feedback after updates
    
    - Validate data entered by user (amount must be an integer, validity of
    phone number, email, XSS safety, etc.)