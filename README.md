# mlops-course

## lesson 1. llama3-med42-8b for med consulting

```
curl -v -s http://127.0.0.11/api/users/signup -H "Content-Type: application/json" -X POST -d '{"email": "arjun@mail.in", "password": "123456"}' | jq
```
```
curl -s http://127.0.0.11/api/llm_queries/new -H "Content-Type: application/json" -X POST -d '{"user_id": 1, "dialogue_id": 2,  "query": "i see worse in the evening. why?"}' | jq
```
