COPY orders
FROM '/data/olist_orders_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY order_items
FROM '/data/olist_order_items_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY order_payments
FROM '/data/olist_order_payments_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY order_reviews
FROM '/data/olist_order_reviews_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY products
FROM '/data/olist_products_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY sellers
FROM '/data/olist_sellers_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY geolocation
FROM '/data/olist_geolocation_dataset.csv'
DELIMITER ','
CSV HEADER;

COPY category_translation
FROM '/data/product_category_name_translation.csv'
DELIMITER ','
CSV HEADER;