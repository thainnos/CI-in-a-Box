terraform {
  required_providers {
    proxmox = {
      source = "Telmate/proxmox"
      version = "2.9.11"
    }
    null = {
        version = "~> 3.0.0"
    }
  }
}

provider "proxmox" {
    pm_api_url = "https://${var.proxmox_host}:8006/api2/json"
    pm_tls_insecure = true
    
    /* Die folgenden zwei Felder werden benötigt.    */
    pm_api_token_secret = var.proxmox_user.token_secret
    pm_api_token_id = var.proxmox_user.token_id
      
    # Uncomment the below for debugging.
    # pm_log_enable = true
    # pm_log_file = "terraform-plugin-proxmox.log"
    pm_debug = true
    # pm_log_levels = {
    # _default = "debug"
    # _capturelog = ""
    # }
}