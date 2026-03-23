resource "google_sql_database_instance" "jobs_db" {
  name             = var.db_instance_name
  database_version = "POSTGRES_17"
  region           = var.region
  project          = var.project_id

  settings {
    tier    = "db-custom-1-3840"
    edition = "ENTERPRISE"

    database_flags {
      name  = "google_ml_integration.enable_model_support"
      value = "on"
    }

    # Enable vector support if needed, though pgvector is standard in newer Postgres
  }

  depends_on = [google_project_service.apis]
  deletion_protection = false
}

resource "google_sql_database" "database" {
  name     = var.database_name
  instance = google_sql_database_instance.jobs_db.name
  project  = var.project_id
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "google_sql_user" "users" {
  name     = var.database_user
  instance = google_sql_database_instance.jobs_db.name
  password = random_password.password.result
  project  = var.project_id
}

# Grant the Cloud SQL Service Account the AI Platform User role
resource "google_project_iam_member" "sql_ai_platform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_sql_database_instance.jobs_db.service_account_email_address}"
}

output "db_instance_connection_name" {
  value = google_sql_database_instance.jobs_db.connection_name
}

output "db_password" {
  value     = random_password.password.result
  sensitive = true
}
