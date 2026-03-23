# Seed Spanner Finance Data
INSERT INTO Account (id, create_time, is_blocked, nick_name) VALUES (1, CURRENT_TIMESTAMP(), false, 'Acct1'), (2, CURRENT_TIMESTAMP(), false, 'Acct2');
INSERT INTO Person (id, name, birthday, country, city) VALUES (1, 'Karol', '1990-01-01 00:00:00', 'Poland', 'Warsaw'), (2, 'John', '1985-05-05 00:00:00', 'USA', 'New York');
INSERT INTO PersonOwnAccount (id, account_id, create_time) VALUES (1, 1, CURRENT_TIMESTAMP()), (2, 2, CURRENT_TIMESTAMP());
INSERT INTO AccountTransferAccount (id, to_id, amount, create_time, order_number) VALUES (1, 2, 100.0, CURRENT_TIMESTAMP(), 'ORD123');
