-- Create events table
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    client_id INT NOT NULL,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_stop DATETIME,
    support_contact_id INT,
    location varchar(255),
    attendees SMALLINT,
    notes TEXT,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (support_contact_id) REFERENCES epic_users(id)
);