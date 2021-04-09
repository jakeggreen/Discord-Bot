CREATE TABLE IF NOT EXISTS tbl_commands_log (
user varchar(max) NULL,
command varchar(max) NULL, 
command_datetime datetime NULL
);

CREATE TABLE IF NOT EXISTS tbl_errors_log (
error_id int NOT NULL,
error_name varchar(max) NULL, 
error_message varchar(max) NULL, 
error_datetime datetime NULL,
error_exception varchar(255) NULL
);