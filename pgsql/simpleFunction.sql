--simple function
create function sales_tax1(subtotal real) returns real AS $$
begin
		return subtotal * 0.06;
end;
$$ language plpgsql;
--use alias for args    
create function sales_tax2(real) returns real AS $$
declare
    subtotal alias for $1;
begin
	return subtotal * 0.06;
end;
$$ language plpgsql;

--with out args
create function sales_tax3(subtotal real, out tax real) AS $$
begin
	tax := subtotal * 0.06;
end;
$$ language plpgsql;

select sales_tax1(100),sales_tax2(200), sales_tax3(300);
