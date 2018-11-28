use c9;

-- Donor table
-- Holds contact information and donor ID 
drop table if exists donor;
create table donor (
    `donorID` int auto_increment,
    `name` varchar(30),
    `description` varchar(30),
    `type` enum('individual', 'organization'),
    `phoneNum` varchar(10),
    `email` varchar(30),
    `address` varchar(30),
    primary key (donorID)
    )ENGINE = InnoDB;

-- Define donation table
-- Primary key as donationID
-- Foreign key references "donorID" from donor table
drop table if exists donation;
create table donation (
    `donationID` int auto_increment,
    `donorID` int,
    `submitDate` date,
    `description` varchar(30),
    `amount` int,
    `type` set ('food', 'medical', 'clothing', 'supplies', 'money', 'other'),
    primary key (donationID),
    foreign key (donorID) references donor(donorID) on delete cascade on update cascade
    )ENGINE = InnoDB;

    
-- Inventory Table
-- status is the amount left
-- relevance is a flag of whether we need more
drop table if exists inventory;
CREATE TABLE inventory(
    `item_id` int auto_increment,
    `description` varchar(30),
    `status` int,
    `relevance` bit,
    `type` set('food', 'medical', 'clothing', 'supplies', 'other'),
    primary key (item_id)
    )ENGINE=InnoDB;

-- Expenditure Table
drop table if exists expenditure;
CREATE TABLE expenditure(
    `expend_id` int auto_increment,
    `description` varchar(30),
    `type` set('food', 'medical', 'clothing', 'supplies', 'in house', 'other'),
    `date` date,
    amount  int,
    primary key (expend_id)
    )ENGINE=InnoDB;
    

