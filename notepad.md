pip install -r requirements.txt
# Terminal 1:
    cd backend 
    uvicorn main:app --reload --port 8000

# Terminal 2:
    streamlit run frontend/app.py

# To run with docker : 
    docker-compose up --build
    # Frontend: http://localhost:8501
    # API docs: http://localhost:8000/docs