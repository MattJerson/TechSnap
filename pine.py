import pinecone
#import torch
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# connect to pinecone environment
pinecone.init(
	api_key='d5be10cf-4dd1-49ad-aac7-789a7c3827e9',
	environment='gcp-starter'
)
index_name = "techsnap"
# connect to extractive-question-answering index we created
index = pinecone.Index(index_name)

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
# load the retriever model from huggingface model hub
retriever = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')
#model_name = 'deepset/roberta-base-squad2'
# load the reader model into a question-answering pipeline
#reader = pipeline(tokenizer=model_name, model=model_name, task='question-answering', device='cpu')

def get_context(question, top_k=3):
    # generate embeddings for the question
    xq = retriever.encode([question]).tolist()
    # search pinecone index for context passage with the answer
    xc = index.query(xq, top_k=top_k, include_metadata=True)
    # extract the context passage from pinecone search result
    c = [x["metadata"]['context'] for x in xc["matches"]]
    return c


from pprint import pprint



def getanswer(question):
  context = get_context(question, top_k = 3)
  #wadu = extract_answer(question,context)
  #return wadu[0]['answer'] + wadu[1]['answer'] + wadu[2]['answer']
  return context



question = 'get me an office computer'
print(getanswer(question))
