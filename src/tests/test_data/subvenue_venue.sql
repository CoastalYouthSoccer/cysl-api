INSERT INTO address(id, address1, city, state, zip_code, active) VALUES
('558a0e81ea454e3bac9d936a75136ef5', '85 Main St', 'Boston', 'MA', '02135', True);
INSERT INTO venue(id, name, active, address_id, association_id) VALUES 
('a6d69d3ede154d4e8c185aa6252f0bd3', 'Boston Venue 1', True, '558a0e81ea454e3bac9d936a75136ef5', 'a3cb9efb73e84758b5476b8fb5fd2ba1');
INSERT INTO sub_venue(id, name, venue_id, active) VALUES 
('6ad491f106e84f58905ea4f9786bba24', 'Field 1', 'a6d69d3ede154d4e8c185aa6252f0bd3', True);
INSERT INTO sub_venue(id, name, venue_id, active) VALUES 
('52219ddad78f40d6924069745d101d39', 'Field 2', 'a6d69d3ede154d4e8c185aa6252f0bd3', True);
INSERT INTO address(id, address1, city, state, zip_code, active) VALUES
('b95e92ea3dc8419cb102979e64ed8f63', '20 Maple St.', 'Boston', 'MA', '02132', True);
INSERT INTO venue(id, name, active, address_id, association_id) VALUES 
('ec9e8bf02c864bc9b1ebf52166c930ff', 'Boston Venue 2', True, 'b95e92ea3dc8419cb102979e64ed8f63', 'a3cb9efb73e84758b5476b8fb5fd2ba1');
INSERT INTO sub_venue(id, name, venue_id, active) VALUES 
('0bb6d640de0f4c6db7ea7d548f5ca53a', 'Field 3', 'ec9e8bf02c864bc9b1ebf52166c930ff', True);
INSERT INTO address(id, address1, city, state, zip_code, active) VALUES
('41a6ae75aa9d4c19857d0be3c95f703a', '100 Main Street', 'Atlanta', 'GA', '30303', True);
INSERT INTO venue(id, name, active, address_id, association_id) VALUES 
('b6a95d67954249a59e20b4732fd68309', 'Atlanta Venue', True, '41a6ae75aa9d4c19857d0be3c95f703a', '53aeb5c2590d43328dec591b1c276d83');
INSERT INTO sub_venue(id, name, venue_id, active) VALUES 
('552b13c1e788466fa0912ef9673bb5d0', 'Atlanta Field 1', 'b6a95d67954249a59e20b4732fd68309', True);
