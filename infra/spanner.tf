variable "spanner_instance_name" {
  description = "The name of the Spanner instance"
  type        = string
  default     = "finance-instance"
}

variable "spanner_database_name" {
  description = "The name of the Spanner database"
  type        = string
  default     = "finance-db"
}

resource "google_spanner_instance" "finance_instance" {
  name             = var.spanner_instance_name
  config           = "regional-${var.region}"
  display_name     = "Finance Instance"
  edition          = "ENTERPRISE"
  num_nodes        = 1
  project          = var.project_id

  # For europe-west1, we should update the config
  # For demo purposes, keeping it regional
}

resource "google_spanner_database" "finance_db" {
  instance = google_spanner_instance.finance_instance.name
  name     = var.spanner_database_name
  project  = var.project_id

  # DDL to create the schema and property graph
  ddl = [
    "CREATE TABLE Account (id INT64 NOT NULL, create_time TIMESTAMP, is_blocked BOOL, nick_name STRING(MAX)) PRIMARY KEY(id)",
    "CREATE TABLE Person (id INT64 NOT NULL, name STRING(MAX), birthday TIMESTAMP, country STRING(MAX), city STRING(MAX)) PRIMARY KEY(id)",
    "CREATE TABLE AccountTransferAccount (id INT64 NOT NULL, to_id INT64 NOT NULL, amount FLOAT64, create_time TIMESTAMP NOT NULL, order_number STRING(MAX)) PRIMARY KEY(id, to_id, create_time), INTERLEAVE IN PARENT Account ON DELETE CASCADE",
    "CREATE TABLE PersonOwnAccount (id INT64 NOT NULL, account_id INT64 NOT NULL, create_time TIMESTAMP) PRIMARY KEY(id, account_id), INTERLEAVE IN PARENT Person ON DELETE CASCADE",
    "CREATE PROPERTY GRAPH FinGraph NODE TABLES(Account KEY(id) LABEL Account PROPERTIES(create_time, id, is_blocked, nick_name), Person KEY(id) LABEL Person PROPERTIES(birthday, city, country, id, name)) EDGE TABLES(AccountTransferAccount KEY(id, to_id, create_time) SOURCE KEY(id) REFERENCES Account(id) DESTINATION KEY(to_id) REFERENCES Account(id) LABEL Transfers PROPERTIES(amount, create_time, id, order_number, to_id), PersonOwnAccount KEY(id, account_id) SOURCE KEY(id) REFERENCES Person(id) DESTINATION KEY(account_id) REFERENCES Account(id) LABEL Owns PROPERTIES(account_id, create_time, id))"
  ]

  deletion_protection = false
}

output "spanner_instance" {
  value = google_spanner_instance.finance_instance.name
}

output "spanner_database" {
  value = google_spanner_database.finance_db.name
}
