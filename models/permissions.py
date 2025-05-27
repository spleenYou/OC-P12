-- Create permissions table
CREATE TABLE IF NOT EXISTS permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT UNIQUE,
    create_client BOOLEAN DEFAULT FALSE,
    update_client BOOLEAN DEFAULT FALSE,
    delete_client BOOLEAN DEFAULT FALSE,
    create_contract BOOLEAN DEFAULT FALSE,
    update_contract BOOLEAN DEFAULT FALSE,
    delete_contract BOOLEAN DEFAULT FALSE,
    create_event BOOLEAN DEFAULT FALSE,
    update_event BOOLEAN DEFAULT FALSE,
    delete_event BOOLEAN DEFAULT FALSE,
    create_user BOOLEAN DEFAULT FALSE,
    update_user BOOLEAN DEFAULT FALSE,
    delete_user BOOLEAN DEFAULT FALSE,
    update_support_on_event BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);