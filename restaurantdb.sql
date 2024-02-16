USE restaurantdb;

SELECT * FROM menue;
SELECT * FROM customer;
SELECT * FROM orders;

ALTER TABLE orders 
MODIFY COLUMN itemID VARCHAR(30);

DELETE FROM customer WHERE customer_id >= 1;
DELETE FROM orders WHERE orders_id >= 1;
DELETE FROM customer WHERE customer_name = 'Fattaneh';
DELETE FROM customer WHERE customer_name = 'Be';
DELETE FROM orders WHERE customerID = 5;

SELECT customer_id FROM customer WHERE customer_name = 'Behniya';

ALTER TABLE orders DROP COLUMN itemID;
ALTER TABLE orders DROP COLUMN orders_count;
ALTER TABLE menue DROP COLUMN  customerID;

DELETE FROM orders WHERE orders_id = 1;

ALTER TABLE customer auto_increment = 1;
ALTER TABLE orders auto_increment = 1;

ALTER TABLE orders DROP FOREIGN KEY orders_ibfk_1;
ALTER TABLE cost DROP FOREIGN KEY cost_ibfk_2;
ALTER TABLE cost DROP FOREIGN KEY cost_ibfk_1;
ALTER TABLE menue DROP FOREIGN KEY menue_ibfk_1;

ALTER TABLE orders DROP FOREIGN KEY orders_cost;
ALTER TABLE orders DROP COLUMN orders_count;
ALTER TABLE menue DROP CONSTRAINT item_cost;

ALTER TABLE orders
DROP INDEX orders_cost;

DROP TABLE cost;

ALTER TABLE menue DROP COLUMN customerID;

SHOW keys FROM orders;