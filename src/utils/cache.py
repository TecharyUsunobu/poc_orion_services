from flask_caching import Cache

cache = Cache()

def init_cache(app):
    """Initializing the cache with the Flask app."""
    cache.init_app(app)
    
    
def cache_response(timeout=300):
    """Cache responses for a specific timeout"""
    def decorator(f):
        return cache.cached(timeout=timeout)(f)
    return decorator