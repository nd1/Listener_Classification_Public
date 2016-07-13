-- create a table with randown numbers between 1 and 333,291 (# of unique users)

CREATE TABLE random_raw (row bigint) ENGINE = innodb 

DELIMITER $$
CREATE PROCEDURE random_fill( IN cnt bigint )
BEGIN
    fold: LOOP
         IF cnt < 1 THEN
             LEAVE fold;
         END IF;
        INSERT INTO random_raw ( row ) VALUES ( round (RAND() * 333291) );
        SET cnt = cnt - 1;
    END LOOP fold;
END$$   
DELIMITER ;

CALL random_fill(10000);

