
-- donor values
insert into donor (name, `type`, email) 
    values
        ('Save the Children', 'organization', 'savethechildren@gmail.com'),
        ('Bill Gates', 'individual', 'billgates11@gmail.com'),
        ('The Mormon Church', 'organization', 'mormonchurchofutah@gmail.com');
        


-- donation values
insert into donation (submitDate, description, amount, units,`type`, donorID) 
    values
        ('2018-11-07', 'Winter Sleeping Bags', 4, 'bags', 'supplies', 1),
        ('2018-02-24', 'carrots', 4, 'bushels','food', 1),
        ('2018-10-07', 'blankets', 20, 'pairs','supplies', 2),
        ('2018-10-31', 'arts and crafts supplies', 4, 'bags', 'supplies', 2),
        ('2018-11-07', 'flour', 20, 'food', 2, 'pounds', 2),
        ('2018-11-07', 'eggs', 48, 'food', 3, 'cartons', 1);

-- inventory
insert into inventory (description, `type`, amount, units) 
    values 
        ('carrots', 'food', 3, 'bushels'),
        ('Winter sleeping bags', 'supplies', 2, 'bags'),
        ('blankets', 'supplies', 12, 'pairs'),
        ('eggs', 'food', 24, 'cartons'),
        ('flour', 'food', 1, 'pounds');

-- expenditure, 
insert into expenditure (description, `type`, `date`, amount) 
    values 
        ('weekly payroll', 'in house', '2018-11-05', 585),
        ('bandages', 'medical', '2018-11-06', 75),
        ('eggs', 'food', '2018-11-02', 50),
        ('blankets', 'supplies', '2018-11-06', 100);
