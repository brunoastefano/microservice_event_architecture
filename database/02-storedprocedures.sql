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

    insert into order_history(order_id, customer_id, status, original_value, discount, total_value)
    values(new_id, customer_id, 0, original_value, 0.0, original_value);

    return new_id;

    commit;
end;$$;