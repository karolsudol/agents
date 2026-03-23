# Resource: Cloud Run Service for the MCP Toolbox
resource "google_cloud_run_v2_service" "toolbox" {
  name     = "mcp-toolbox-service"
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.toolbox_sa.email
    containers {
      image = "gcr.io/${var.project_id}/mcp-toolbox"

      env {
        name  = "DB_PASSWORD"
        value = random_password.password.result
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "REGION"
        value = var.region
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Resource: Cloud Run Service for the ADK Agents
resource "google_cloud_run_v2_service" "agents" {
  name     = "adk-agents-service"
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.agent_sa.email
    containers {
      image = "gcr.io/${var.project_id}/adk-agents"

      env {
        name  = "TOOLBOX_URL"
        value = google_cloud_run_v2_service.toolbox.uri
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "REGION"
        value = var.region
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# Allow unauthenticated access for demo purposes
resource "google_cloud_run_v2_service_iam_member" "noauth_toolbox" {
  location = google_cloud_run_v2_service.toolbox.location
  project  = google_cloud_run_v2_service.toolbox.project
  name     = google_cloud_run_v2_service.toolbox.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service_iam_member" "noauth_agents" {
  location = google_cloud_run_v2_service.agents.location
  project  = google_cloud_run_v2_service.agents.project
  name     = google_cloud_run_v2_service.agents.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "toolbox_url" {
  value = google_cloud_run_v2_service.toolbox.uri
}

output "agents_url" {
  value = google_cloud_run_v2_service.agents.uri
}
