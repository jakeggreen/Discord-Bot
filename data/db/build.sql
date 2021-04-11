CREATE TABLE IF NOT EXISTS tbl_commands_log (
user TEXT NULL,
command TEXT NULL, 
command_datetime datetime NULL
);

CREATE TABLE IF NOT EXISTS tbl_errors_log (
error_id int NOT NULL,
error_name TEXT NULL, 
error_message TEXT NULL, 
error_datetime datetime NULL,
error_exception TEXT NULL
);