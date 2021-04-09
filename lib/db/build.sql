CREATE TABLE IF NOT EXISTS tbl_commands_log (
user varchar NULL,
command varchar NULL, 
command_datetime datetime NULL
);

CREATE TABLE IF NOT EXISTS tbl_errors_log (
error_id int NOT NULL,
error_name varchar NULL, 
error_message varchar NULL, 
error_datetime datetime NULL,
error_exception varchar NULL
);