from fastapi import APIRouter,UploadFile,File,Form,HTTPException
from .vectorstore import load_vectorstore,delete_document
import uuid
import traceback

router=APIRouter()

@router.post("/upload_docs")
async def upload_docs(file:UploadFile=File(...),grade:int=Form(...),):
    """
        Upload a pdf document and index it into:
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only Pdf files are supported")
    doc_id=str(uuid.uuid4())
    ACCESS_ROLE="Public"

    # call vectorstore function
    try:
        await load_vectorstore(uploaded_files=[file],role=ACCESS_ROLE,doc_id=doc_id,grade=grade)
    # except Exception as e:
    #     print("Error during document upload")
    #     raise HTTPException(status_code=500,detail="Failed to process and index the document")
    except Exception as e:
   

        traceback.print_exc()

        raise HTTPException(
        status_code=500,
        detail=str(e)
        )
    return{
        "messaage":f"{file.filename} uploaded and indexeed successfully",
        "doc_id":doc_id,
        "grade":grade,
        "access":ACCESS_ROLE
    }
@router.delete("/delete_doc/{doc_id}")
def delete_doc(doc_id: str):

    delete_document(doc_id)

    return {
        "message": "Document deleted successfully"
    }