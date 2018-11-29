
-- donor values
insert into donor (name, `type`, email) 
    values
        ('Save the Children', 'organization', 'savethechildren@gmail.com'),
        ('Bill Gates', 'individual', 'billgates11@gmail.com'),
        ('The Mormon Church', 'organization', 'mormonchurchofutah@gmail.com');
        


-- donation values
insert into donation (submitDate, description, amount, `type`, donorID) 
    values
        ('2018-11-07', 'Winter Sleeping Bags', 4, 'supplies', 1),
        ('2018-02-24', 'carrots (bushels)', 4, 'food', 1),
        ('2018-10-07', 'blankets', 20, 'supplies', 2),
        ('2018-10-31', 'arts and crafts supplies', 4, 'supplies', 2),
        ('2018-11-07', 'flour (pounds)', 20, 'food', 2),
        ('2018-11-07', 'eggs', 48, 'food', 3);

-- inventory
insert into inventory (description, `type`, status, relevance) 
    values 
        ('carrots (bushels)', 'food', 3, true),
        ('Winter Sleeping Bags', 'supplies', 2, true),
        ('blankets', 'supplies', 12, true),
        ('eggs', 'food', 24, true),
        ('flour (pounds)', 'food', 1, true);

-- expenditure, 
insert into expenditure (description, `type`, `date`, amount) 
    values 
        ('weekly payroll', 'in house', '2018-11-05', 585),
        ('bandages', 'medical', '2018-11-06', 75),
        ('eggs', 'food', '2018-11-02', 50),
        ('blankets', 'supplies', '2018-11-06', 100);
    
