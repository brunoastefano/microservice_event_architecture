create database companydb;

\c companydb;



create table "order" (
    order_id int generated by default as identity,
    customer_id int not null,
    status int,
    original_value float,
    discount float,
    total_value float,
    updated_at timestamptz default now(),
    constraint pk_order primary key (order_id)
);

create table order_history (
    order_id int not null,
    version int generated by default as identity,
    customer_id int not null,
    status int, 
    original_value float,
    discount float,
    total_value float,
    updated_at timestamptz default now(),
    constraint pk_order_history primary key (order_id,version)
);

create table order_item (
    order_id int not null,
    product_id int not null,
    quantity int not null,  
    updated_at timestamptz default now(),
    constraint pk_active_orders primary key (order_id,product_id)
);