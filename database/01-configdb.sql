CREATE DATABASE companydb;

\c companydb;

CREATE TABLE "order" (
    "order_id" INT NOT NULL,
    "customer_id" INT NOT NULL,
    "status" VARCHAR(20),
    "original_value" FLOAT,
    "discount" FLOAT,
    "total_value" FLOAT,
    "updated_at" TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT "pk_order" PRIMARY KEY ("order_id")
);

CREATE TABLE "order_history" (
    "order_id" INT NOT NULL,
    "version" INT NOT NULL,
    "customer_id" INT NOT NULL,
    "status" VARCHAR(20),	
    "original_value" FLOAT,
    "discount" FLOAT,
    "total_value" FLOAT,
    "updated_at" TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT "pk_order_history" PRIMARY KEY ("order_id","version")
);

CREATE TABLE "order_item" (
    "order_id" INT NOT NULL,
    "product_id" INT NOT NULL,
    "quantity" INT NOT NULL,	
    "updated_at" TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT "pk_active_orders" PRIMARY KEY ("order_id","product_id")
);