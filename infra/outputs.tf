output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "db_instance_name" {
  value = google_sql_database_instance.jobs_db.name
}

output "db_user" {
  value = google_sql_user.users.name
}
