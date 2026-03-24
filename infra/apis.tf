resource "google_project_service" "apis" {
  for_each = toset([
    "sqladmin.googleapis.com",
    "aiplatform.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
    "compute.googleapis.com",
    "cloudbuild.googleapis.com",
    "spanner.googleapis.com"
  ])

  project = var.project_id
  service = each.key

  disable_on_destroy = false
}
