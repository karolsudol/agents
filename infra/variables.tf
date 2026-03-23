variable "project_id" {
  description = "The ID of the GCP project"
  type        = string
  default     = "skillful-signer-491109-r0"
}

variable "region" {
  description = "The region to deploy resources in"
  type        = string
  default     = "europe-west1"
}

variable "db_instance_name" {
  description = "The name of the Cloud SQL instance"
  type        = string
  default     = "jobs-db-instance"
}

variable "database_name" {
  description = "The name of the database"
  type        = string
  default     = "jobs_db"
}

variable "database_user" {
  description = "The name of the database user"
  type        = string
  default     = "jobs_user"
}
