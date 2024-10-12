class Config:
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey'
    JWT_SECRET = ""
    # Razorpay API credentials
    RAZORPAY_KEY_ID = 'your_razorpay_key_id'
    RAZORPAY_KEY_SECRET = 'your_razorpay_key_secret'
