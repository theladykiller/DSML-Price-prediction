from app import app
import callbacks.plot  # Register the callbacks
import callbacks.knn   # Register KNN callbacks

if __name__ == '__main__':
    app.run(debug=True)  # dev_tools_props_check=True