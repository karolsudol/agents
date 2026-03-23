# Service Account for the MCP Toolbox
resource "google_service_account" "toolbox_sa" {
  account_id   = "mcp-toolbox-sa"
  display_name = "MCP Toolbox Service Account"
  project      = var.project_id
}

# Service Account for the ADK Agent
resource "google_service_account" "agent_sa" {
  account_id   = "adk-agent-sa"
  display_name = "ADK Agent Service Account"
  project      = var.project_id
}

# Grant Agent SA Vertex AI User role
resource "google_project_iam_member" "agent_vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.agent_sa.email}"
}

# Grant Toolbox SA Cloud SQL Client role
resource "google_project_iam_member" "toolbox_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.toolbox_sa.email}"
}

# Grant Toolbox SA Cloud SQL Instance User (for IAM auth)
resource "google_project_iam_member" "toolbox_sql_instance_user" {
  project = var.project_id
  role    = "roles/cloudsql.instanceUser"
  member  = "serviceAccount:${google_service_account.toolbox_sa.email}"
}
