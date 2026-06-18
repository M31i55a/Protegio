import sqlite3

conn = sqlite3.connect('db.sqlite3')

conn.execute('''CREATE TABLE IF NOT EXISTS burp_suite_suite_proxyrequest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    url TEXT NOT NULL,
    host VARCHAR(255) NOT NULL DEFAULT '',
    path TEXT NOT NULL DEFAULT '',
    request_headers TEXT NOT NULL DEFAULT '{}',
    request_body TEXT NOT NULL DEFAULT '',
    response_status INTEGER NULL,
    response_headers TEXT NOT NULL DEFAULT '{}',
    response_body TEXT NOT NULL DEFAULT '',
    response_length INTEGER NULL,
    response_time REAL NULL,
    intercepted BOOL NOT NULL DEFAULT 0,
    modified BOOL NOT NULL DEFAULT 0,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS burp_suite_suite_intruderpayload (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    attack_type VARCHAR(50) NOT NULL DEFAULT 'sniper',
    target_url TEXT NOT NULL DEFAULT '',
    request_template TEXT NOT NULL DEFAULT '',
    payloads TEXT NOT NULL DEFAULT '[]',
    results TEXT NOT NULL DEFAULT '[]',
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS burp_suite_suite_repeaterrequest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL DEFAULT 'Request',
    method VARCHAR(10) NOT NULL DEFAULT 'GET',
    url TEXT NOT NULL DEFAULT '',
    headers TEXT NOT NULL DEFAULT '{}',
    body TEXT NOT NULL DEFAULT '',
    response_status INTEGER NULL,
    response_headers TEXT NOT NULL DEFAULT '{}',
    response_body TEXT NOT NULL DEFAULT '',
    response_time REAL NULL,
    history TEXT NOT NULL DEFAULT '[]',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)''')

conn.execute('''CREATE TABLE IF NOT EXISTS burp_suite_suite_decoderdata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_data TEXT NOT NULL,
    output_data TEXT NOT NULL,
    encoding_type VARCHAR(50) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()
conn.close()
print('4 tables creees avec succes !')
