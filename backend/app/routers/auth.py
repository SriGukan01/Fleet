import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.database import get_db
from backend.app.models.user import (
    UserCreate,
    UserResponse,
    TokenResponse,
    LoginRequest,
    DemoLoginRequest,
    UserRole
)
from backend.app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in or use Demo Access."
        )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token."
        )
    
    db = get_db()
    users_col = db.get_collection("users")
    user = await users_col.find_one({"_id": payload["sub"]})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    return UserResponse(
        id=user["_id"],
        email=user["email"],
        name=user["name"],
        role=UserRole(user.get("role", "applicant")),
        organization=user.get("organization"),
        is_active=user.get("is_active", True),
        is_demo=user.get("is_demo", False),
        created_at=user.get("created_at", "")
    )

@router.post("/register", response_model=TokenResponse)
async def register(req: UserCreate):
    db = get_db()
    users_col = db.get_collection("users")
    existing = await users_col.find_one({"email": req.email.lower().strip()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    user_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    doc = {
        "_id": user_id,
        "email": req.email.lower().strip(),
        "name": req.name.strip(),
        "role": req.role.value,
        "organization": req.organization,
        "hashed_password": hash_password(req.password),
        "is_active": True,
        "is_demo": False,
        "created_at": now
    }
    await users_col.insert_one(doc)

    token = create_access_token({"sub": user_id, "role": req.role.value, "email": doc["email"]})
    user_res = UserResponse(
        id=user_id,
        email=doc["email"],
        name=doc["name"],
        role=req.role,
        organization=doc["organization"],
        is_active=True,
        is_demo=False,
        created_at=now
    )
    return TokenResponse(access_token=token, user=user_res)

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    db = get_db()
    users_col = db.get_collection("users")
    user = await users_col.find_one({"email": req.email.lower().strip()})
    if not user or not verify_password(req.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")

    token = create_access_token({"sub": user["_id"], "role": user.get("role", "applicant"), "email": user["email"]})
    user_res = UserResponse(
        id=user["_id"],
        email=user["email"],
        name=user["name"],
        role=UserRole(user.get("role", "applicant")),
        organization=user.get("organization"),
        is_active=user.get("is_active", True),
        is_demo=user.get("is_demo", False),
        created_at=user.get("created_at", "")
    )
    return TokenResponse(access_token=token, user=user_res)

@router.post("/demo-login", response_model=TokenResponse)
async def demo_login(req: DemoLoginRequest):
    """
    Hackathon 1-click login for demonstration: switches seamlessly between
    Applicant, Verification Officer, and System Administrator.
    """
    db = get_db()
    users_col = db.get_collection("users")
    user = await users_col.find_one({"role": req.role.value, "is_demo": True})
    
    if not user:
        # Fallback to any user with that role
        user = await users_col.find_one({"role": req.role.value})
        
    if not user:
        raise HTTPException(status_code=404, detail=f"No demonstration account found for role '{req.role.value}'.")

    token = create_access_token({"sub": user["_id"], "role": user["role"], "email": user["email"]})
    user_res = UserResponse(
        id=user["_id"],
        email=user["email"],
        name=user["name"],
        role=UserRole(user["role"]),
        organization=user.get("organization"),
        is_active=True,
        is_demo=True,
        created_at=user.get("created_at", "")
    )
    return TokenResponse(access_token=token, user=user_res)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user
