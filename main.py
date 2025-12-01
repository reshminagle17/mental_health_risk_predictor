# import the ASGI server
import uvicorn

print("hello world")
# entry point for the application
if __name__ == "__main__":
    uvicorn.run("src.app:app",host="0.0.0.0",port=8000,reload=True)