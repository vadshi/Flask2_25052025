import os, sys
sys.path.append(os.path.pardir)
from my_app import create_app
from my_app.config import ProductionConfig

app = create_app()


if __name__ == '__main__':
    app.run(
        port=ProductionConfig.PORT, 
        host=ProductionConfig.SERVER_NAME, 
        debug=ProductionConfig.DEBUG
    )