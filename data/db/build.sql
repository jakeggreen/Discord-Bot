CREATE TABLE IF NOT EXISTS tbl_commands_log (
command_id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT NULL,
command TEXT NULL, 
command_datetime datetime NULL
);

CREATE TABLE IF NOT EXISTS tbl_errors_log (
error_id INTEGER PRIMARY KEY AUTOINCREMENT,
error_name TEXT NULL, 
error_message TEXT NULL, 
error_datetime datetime NULL,
error_exception TEXT NULL
);

CREATE TABLE IF NOT EXISTS tbl_game_activity_log (
activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
game_name TEXT NULL,
user TEXT NULL,
activity_start_time datetime NULL
);