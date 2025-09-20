import requests

base_url = "http://localhost:8000"

# 회원가입
signup_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "full_name": "John Doe"
}
response = requests.post(f"{base_url}/auth/signup", json=signup_data)
print("회원가입 결과:", response.json())

# 로그인 (간단 검증)
login_data = {
    "username": "john_doe",
    "password": "securepass123"
}
auth_response = requests.post(f"{base_url}/auth/login", json=login_data)
print("로그인 결과:", auth_response.json())

# 도서 등록
book_data = {
    "title": "Python Programming",
    "author": "Jane Smith",
    "isbn": "978-0123456789",
    "category": "Programming",
    "total_copies": 5
}
book_response = requests.post(f"{base_url}/books", json=book_data)
print("도서 등록 결과:", book_response.json())

# 도서 전체 조회
search_response = requests.get(f"{base_url}/books")
print("도서 전체 조회 결과:", search_response.json())

# 도서 삭제
delete_isbn = "978-0123456789"
delete_response = requests.delete(f"{base_url}/books/{delete_isbn}")
print("도서 삭제 결과:", delete_response.json())