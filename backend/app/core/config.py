from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI : str
    REDIS_URL : str
    AWS_S3_BUCKET : str
    
    
    # Add these new fields to match your .env file
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_S3_ENDPOINT: str
    
    class Config:
        env_file =".env"
        
        
        
settings = Settings()