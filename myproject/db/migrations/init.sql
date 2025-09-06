CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;


CREATE TABLE user_audit_log (
    id SERIAL PRIMARY KEY,
    user_id INT,
    username TEXT,
    email TEXT,
    role TEXT,
    action TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by TEXT
);

CREATE OR REPLACE FUNCTION log_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_audit_log(user_id, username, email, role, action, changed_by)
        VALUES (NEW.id, NEW.username, NEW.email, NEW.role, 'INSERT', current_user);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_audit_log(user_id, username, email, role, action, changed_by)
        VALUES (NEW.id, NEW.username, NEW.email, NEW.role, 'UPDATE', current_user);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO user_audit_log(user_id, username, email, role, action, changed_by)
        VALUES (OLD.id, OLD.username, OLD.email, OLD.role, 'DELETE', current_user);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_user_audit
AFTER INSERT OR UPDATE OR DELETE ON users_customuser
FOR EACH ROW
EXECUTE FUNCTION log_user_changes();