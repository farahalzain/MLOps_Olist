# MLOps Task 1 - Olist Dataset

This repository contains my work for Task 1 of the MLOps Training track.

## Task Objective

Understand the Olist Brazilian E-Commerce dataset, load the CSV files into a relational database, and verify that the data can be queried and joined successfully.

The final machine learning problem is to predict whether an order will be delivered late or on time.

## Technologies Used

- Docker
- PostgreSQL
- SQL
- Olist Brazilian E-Commerce Dataset

## Database

PostgreSQL was run locally using Docker.

The database contains 9 tables:

- customers
- orders
- order_items
- order_payments
- order_reviews
- products
- sellers
- geolocation
- category_translation

## Main Relationships

- `customers` → `orders` using `customer_id`
- `orders` → `order_items` using `order_id`
- `order_items` → `products` using `product_id`
- `order_items` → `sellers` using `seller_id`
- `orders` → `order_payments` using `order_id`
- `orders` → `order_reviews` using `order_id`

## SQL Files

The `sql` directory contains:

- `create_tables.sql` - creates the database tables.
- `load_data.sql` - loads the CSV data into PostgreSQL.
- `queries.sql` - contains basic queries and a JOIN used to test the database.

## Verification

The database was successfully tested by:

- Reading data from the tables.
- Counting the orders in the dataset.
- Joining the `orders` and `customers` tables using `customer_id`.

The `orders` table contains 99,441 rows.

## Dataset

The original CSV files are not included in this repository.

They can be downloaded from the Olist Brazilian E-Commerce Public Dataset on Kaggle.

## Status

completed successfully.