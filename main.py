from fastapi import FastAPI
import uvicorn

app=FastAPI()
@app.get("/")
def healthCheck():
    return{"status":"tutot-rag-is running"}
# def main():
#     print("Hello from tutor-rag!")

# if __name__ == "__main__":
#     main()