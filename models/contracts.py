-- Create contracts table
CREATE TABLE IF NOT EXISTS contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    commercial_id INT NOT NULL,
    total_amount DECIMAL(10,2),
    rest_amount DECIMAL(10,2),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (commercial_id) REFERENCES epic_users(id)
);