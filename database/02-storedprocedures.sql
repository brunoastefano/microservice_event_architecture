\c companydb;

create or replace function create_order(
   customer_id int,
   original_value float
) returns int
language plpgsql    
as $$
declare
  new_id int;
begin
    insert into "order"(customer_id, status, original_value, discount, total_value)
    values(customer_id, 0, original_value, 0.0, original_value)
    returning order_id into strict new_id; 

    insert into order_history(order_id, version, customer_id, status, original_value, discount, total_value)
    values(new_id, 1, customer_id, 0, original_value, 0.0, original_value);

    return new_id;

    commit;
end;$$;


create or replace function update_order_discount(
   var_order_id int,
   var_discount float,
   var_total_value float
) returns void
language plpgsql    
as $$
declare
  var_customer_id int;
  var_original_value float;
  var_version int;
begin
    update "order"
    set status = 1, discount = var_discount, total_value = var_total_value, updated_at = now()
    where order_id = var_order_id;

    select customer_id, original_value
    into var_customer_id, var_original_value
    from "order"
    where order_id = var_order_id;

    select version 
    into var_version
    from order_history 
    where order_id = var_order_id
    order by version desc
    limit 1;

    insert into order_history(order_id, version, customer_id, status, original_value, discount, total_value)
    values(var_order_id, var_version+1, var_customer_id, 1, var_original_value, var_discount, var_total_value);

    return;

    commit;
end;$$;


create or replace function insert_order_item(
   order_id int,
   product_id int,
   quantity int
) returns void
language plpgsql    
as $$
begin

    insert into order_item(order_id, product_id, quantity)
    values(order_id, product_id, quantity);

    return;

    commit;
end;$$;

create or replace function insert_log(
  log_level int,
  log_level_name text,
  log_message text,
  log_owner text
) returns void
language plpgsql    
as $$
begin

    insert into logging(log_level, log_level_name, log_message, log_owner)
    values(log_level, log_level_name, log_message, log_owner);

    return;

    commit;
end;$$;