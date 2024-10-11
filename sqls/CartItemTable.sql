CREATE TABLE cart_item
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT not null,
    menu_item_id INT not null,
    quantity INT
);