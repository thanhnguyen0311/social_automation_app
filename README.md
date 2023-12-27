This is the LDPlayer management support version written in Python to optimize the management features of the emulators.<br>
pip install ttkbootstrap==0.5.3<br>
pip install appium-python-client==2.1.4<br>
pip install requests<br>
pip install pyautogui<br>
pip install pygetwindow<br>
pip install selenium Pillow<br>
pip install mysql-connector-python<br><br><br>

USE social_automation;

CREATE TABLE IF NOT EXISTS devices (
    device_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    imei VARCHAR(255),
    uuid VARCHAR(255),
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    imsi VARCHAR(255),
    android_id VARCHAR(255),
    sim_serial VARCHAR(255),
    mac_address VARCHAR(255),
    create_date DATETIME default now()
);
CREATE TABLE IF NOT EXISTS `users` (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255), 
    email VARCHAR(255),
    phone VARCHAR(20),
    is_active BIT default(0),
    is_deleted BIT default(0),
    last_seen DATETIME,
    create_date DATETIME default now()
);

CREATE TABLE IF NOT EXISTS emails (
    email_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    create_date DATETIME default now(),
    user_id BIGINT default(1),
    FOREIGN KEY (user_id) REFERENCES `users`(user_id)
);


CREATE TABLE IF NOT EXISTS fb_accounts (
    fb_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    device_id BIGINT,
    email_id BIGINT,
    user_id BIGINT default(1),
    last_login DATETIME,
    date DATETIME default now(),
    status VARCHAR(20) default('uncheck'),
    is_deleted BIT default(0),
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (user_id) REFERENCES `users`(user_id),
    FOREIGN KEY (email_id) REFERENCES emails(email_id)
);

INSERT INTO users (name, username, password, email, phone) VALUES ('Thanh', 'nct031194', '272337839', 'nct031194@icloud.com', '0937404039');