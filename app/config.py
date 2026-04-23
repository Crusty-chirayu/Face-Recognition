from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    recognition_threshold: float = 0.4
    use_cnn_model: bool = False
    frame_interval_ms: int = 500
    max_frame_size_kb: int = 500
    duplicate_log_cooldown_seconds: int = 300
    anti_spoof_enabled: bool = True
    anti_spoof_threshold: float = 0.6
    unknown_alert_enabled: bool = True
    upload_dir: str = "./uploads"
    reports_dir: str = "./reports"
    max_upload_size_mb: int = 5
    max_photos_per_person: int = 5
    smtp_host: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    smtp_from: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    admin_email: str
    admin_name: str
    admin_password: str
    log_level: str = "DEBUG"
    log_format: str = "console"

    class Config:
        env_file = ".env"

settings = Settings()