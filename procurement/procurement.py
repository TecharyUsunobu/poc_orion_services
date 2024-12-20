from woocommerce import API
import os

wcapi = API(
    url="https://portalstage.techary.com/",
    consumer_key=os.getenv('WOO_CONSUMER_KEY'),
    consumer_secret=os.getenv('WOO_CONSUMER_SECRET'),
)
