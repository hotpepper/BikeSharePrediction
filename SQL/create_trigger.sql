



--DROP TRIGGER tgr_sum ON rawcitibike CASCADE;
--drop function sum();

CREATE FUNCTION sum() RETURNS TRIGGER AS $_$
begin
	insert into test2 (id, name) values (1,'test');
RETURN NULL;
END; --$_$ LANGUAGE 'plpgsql';

CREATE TRIGGER tgr_sum
after insert ON rawcitibike
execute procedure sum();
 
