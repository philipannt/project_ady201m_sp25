create database ADY4
use ADY4


create table tbl_Xemaychotot
(
ID INT IDENTITY(1,1) Primary Key,
Name_Bike nvarchar(100) not null,
Year_Of_Manufacture varchar(4) null,
Distance_of_Bike varchar(20) null,
Nationality varchar(20) null,
Location_bike nvarchar (200) null,
Listing_time varchar(30) null,
Price varchar(20),
Price_min varchar(20),
Price_max varchar(20)

);
--Drop table tbl_Xemaychotot

CREATE PROCEDURE prcInsertDataOfBike
(@json VARCHAR(MAX) = '')
AS
BEGIN
    INSERT INTO tbl_Xemaychotot (
        Name_Bike, 
        Year_Of_Manufacture,
        Distance_of_Bike,
        Nationality, 
        Location_bike, 
        Listing_time,
        Price, 
        Price_min, 
        Price_max
    )
    SELECT 
        Name_Bike,
        Year_of_Manufacture,
        Distance_of_Bike,
        Nationality,
        Location_bike,
        Listing_time,
        Price,
        Price_min,
        Price_max
    from openjson(@json)
    WITH (
        Name_Bike NVARCHAR(100) '$.name',
		Year_of_Manufacture VARCHAR(4) '$.Year_of_manufacture',
        Distance_of_Bike NVARCHAR(20) '$.Kilometers_driven',
        Nationality NVARCHAR(50) '$.Nationality',
        Location_bike NVARCHAR(200) '$.Location',
        Listing_time VARCHAR(30) '$.Listing_time',
        Price NVARCHAR(20) '$.price',
        Price_min VARCHAR(20) '$.price_min',
        Price_max VARCHAR(20) '$.price_max'
        
    );
END
--drop procedure prcInsertDataOfBike

SELECT * FROM tbl_Xemaychotot

	








