from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """ Configuration settings for the Flask application"""
    
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'
    CACHE_TYPE = 'SimpleCache',
    SECRET_KEY = os.getenv('SECRET_KEY') 
    API_VERSION = os.getenv('API_VERSION')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False