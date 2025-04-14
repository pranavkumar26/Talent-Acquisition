from sentence_transformers import SentenceTransformer, util
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_resumes(json_path="data/sample_resumes.json"):
    with open(json_path, 'r') as file:
        return json.load(file)

def match_candidates(job_description, resumes, top_k=3):
    job_embedding = model.encode(job_description, convert_to_tensor=True)
    
    results = []
    for resume in resumes:
        resume_embedding = model.encode(resume["content"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(job_embedding, resume_embedding).item()
        results.append({
            "id": resume["id"],
            "name": resume["name"],
            "similarity": similarity
        })
    
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]

if __name__ == "__main__":
    resumes = load_resumes()
    job_desc = "Looking for a Python developer with experience in NLP, PyTorch, and REST APIs."
    matches = match_candidates(job_desc, resumes)

    print("Top Matches:")
    for match in matches:
        print(f"{match['name']} - Score: {match['similarity']:.2f}")