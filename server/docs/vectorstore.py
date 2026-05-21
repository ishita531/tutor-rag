import os
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.db import chunk_collection

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV=os.getenv("PINECONE_ENV","us-east-1")
PINECONE_INDEX_NAME=os.getenv("PINECONE_INDEX_NAME","tutor-rags")

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
#means store this variable into system enviornment

UPLOAD_DIR="./upload_docs"
#Create/use a folder named upload_docs inside current project.
#upload_docs is the folder where the file uploaded will get saved

#function to make folder/directories
os.makedirs(UPLOAD_DIR,exist_ok=True)


pc=None
index=None

def get_pinecone_index():
    global pc,index
    if index is None:
        #creates pinecone client
        #basically connecitng to pineconde server
        #now your app can talk to pinecone
        pc=Pinecone(api_key=PINECONE_API_KEY)
        #index represeents your vector database
        index=pc.Index(PINECONE_INDEX_NAME)
    return index


#this function processes uplaoded pdfs
async def load_vectorstore(uploaded_files,role:str,doc_id:str,grade:int):
    #initialise embedding model
    embed_model=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    #get pinecone index
    pinecone_index=get_pinecone_index()
    #loop through uploaded files
    for file in uploaded_files:
        # 1 save rae file
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        # 2. loaad pdf text
        #creates a pdf loader
        loader=PyPDFLoader(str(save_path))
        #loads the pdf text
        documents=loader.load()
        # 3. chunk text
    #     Suppose PDF has 10,000 characters.
    # e split into chunks:
    # Chunk 1 → chars 0–500
    # Chunk 2 → chars 450–950
    # Chunk 3 → chars 900–1400
        splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        # 4. guard chunks
        if not chunks:
            print(f"No text extracted from {file.filename}, skipping...")
            continue        # 5.dual storing
        # store full text in mongodb
        chunk_docs=[]
        for i,chunk in enumerate(chunks):
            chunk_docs.append({
                "chunk_id":f"{doc_id}-{i}",
                "doc_id":doc_id,
                "text":chunk.page_content,
                "page":int(chunk.metadata.get("page",0)),
                "source":file.filename,
                "grade":grade,
                "role":role,
            })
        if chunk_docs:
            chunk_collection.insert_many(chunk_docs)
         # Creating embeddiings
        texts=[chunk.page_content for chunk in chunks]
        embeddings = await asyncio.to_thread(embed_model.embed_documents,texts)
        ids=[f"{doc_id}{-i}" for i in range(len(embeddings))]

        metadatas=[
            {
            "doc_id":doc_id,
               
             "page":int(chunks[i].metadata.get("page",0)),
             "source":file.filename,
              "grade":grade,
             "role":role,

                }
              for i in range(len(embeddings))
        ]
        pinecone_index.upsert(vectors=zip(ids,embeddings,metadatas))
    print(f"Successfully indexed{file.filename}")

def delete_document(doc_id: str):
    pinecone_index = get_pinecone_index()

    pinecone_index.delete(
        filter={
            "doc_id": doc_id
        }
    )

    chunk_collection.delete_many({
        "doc_id": doc_id
    })

    print("Document deleted")