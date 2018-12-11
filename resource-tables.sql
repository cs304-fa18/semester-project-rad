use c9;
drop table if exists setStatus;
drop table if exists expenditure;
drop table if exists inventory;
drop table if exists donation;
drop table if exists donor;


-- Donor table
-- Holds contact information and donor ID 
create table donor (
    `donorID` int auto_increment,
    `name` varchar(30),
    `description` varchar(50),
    `type` enum ('individual', 'organization'),
    `phoneNum` varchar(10),
    `email` varchar(50),
    `address` varchar(30),
    primary key (donorID)
    )ENGINE = InnoDB;

-- Define donation table
-- Primary key as donationID
-- Foreign key references "donorID" from donor table
create table donation (
    `donationID` int auto_increment,
    `donorID` int,
    `submitDate` date,
    `description` varchar(50),
    `amount` int,
    `units` varchar(30),
    `type` set ('food', 'medical', 'clothing', 'supplies', 'money', 'other'),
    primary key (donationID),
    foreign key (donorID) references donor(donorID) on delete cascade on update cascade
    )ENGINE = InnoDB;

    
-- Inventory Table
-- status is the amount left
-- relevance is a flag of whether we need more
CREATE TABLE inventory(
    `item_id` int auto_increment,
    `description` varchar(50),
    `submitDate` date,
    `amount` int,
    `units` varchar(30),
    `status` set('high','low', 'null') default 'null',
    `type` set('food', 'medical', 'clothing', 'supplies', 'other'),
    primary key (item_id, status)
    )ENGINE=InnoDB;

-- Expenditure Table
CREATE TABLE expenditure(
    `expend_id` int auto_increment,
    `description` varchar(30),
    `type` set('food', 'medical', 'clothing', 'supplies', 'in house', 'other'),
    `date` date,
    `amount`  int,
    primary key (expend_id)
    )ENGINE=InnoDB;

-- Setting Status for all Items
-- Currently this table is not linked to inventory, this will need to be done
CREATE TABLE setStatus(
    `item_id` int,
    `threshold` int, -- if amount is equal to or less than this threshold status is low otherwise high
    primary key(item_id),
    foreign key (item_id) references inventory(item_id) on delete cascade on update cascade
    )ENGINE=InnoDB;

    
