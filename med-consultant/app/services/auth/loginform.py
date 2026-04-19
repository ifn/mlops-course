from typing import List, Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors: List[str] = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self) -> bool:
        if not self.username or "@" not in self.username:
            self.errors.append("Valid email is required")
        if not self.password:
            self.errors.append("Password is required")
        return not self.errors
