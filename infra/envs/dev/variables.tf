variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "bq_location" {
  type    = string
  default = "us-central1"
}

variable "raw_bucket" {
  type = string
}