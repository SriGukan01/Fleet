import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from backend.app.database import get_db
from backend.app.routers.auth import get_current_user
from backend.app.models.user import UserResponse
from backend.app.services.compliance_engine import DEFAULT_RULES

router = APIRouter(prefix="/api/compliance-rules", tags=["Compliance Rules"])

class CreateRuleRequest(BaseModel):
    rule_id: str
    name: str
    jurisdiction: str
    application_type: str = "all"
    policy_reference: Dict[str, Any]
    severity: str = "high"
    rule_type: str
    parameters: Dict[str, Any] = {}
    explanation: str
    remediation_instructions: str

class UpdateRuleRequest(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    severity: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@router.get("")
async def list_rules():
    db = get_db()
    rules_col = db.get_collection("compliance_rules")
    rules = await rules_col.find().to_list(100)
    if not rules:
        return DEFAULT_RULES
    return rules

@router.post("")
async def create_rule(
    req: CreateRuleRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can configure regulatory rules.")

    db = get_db()
    rules_col = db.get_collection("compliance_rules")

    existing = await rules_col.find_one({"rule_id": req.rule_id})
    if existing:
        raise HTTPException(status_code=400, detail=f"Rule with ID '{req.rule_id}' already exists.")

    new_rule = {
        "_id": str(uuid.uuid4()),
        "rule_id": req.rule_id,
        "name": req.name,
        "jurisdiction": req.jurisdiction,
        "application_type": req.application_type,
        "policy_reference": req.policy_reference,
        "version": "1.0",
        "severity": req.severity,
        "rule_type": req.rule_type,
        "parameters": req.parameters,
        "explanation": req.explanation,
        "remediation_instructions": req.remediation_instructions,
        "is_active": True
    }
    await rules_col.insert_one(new_rule)
    return new_rule

@router.patch("/{id}")
async def update_rule(
    id: str,
    req: UpdateRuleRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Only administrators can modify compliance rules.")

    db = get_db()
    rules_col = db.get_collection("compliance_rules")
    rule = await rules_col.find_one({"_id": id}) or await rules_col.find_one({"rule_id": id})
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found.")

    updates = {}
    if req.name is not None:
        updates["name"] = req.name
    if req.is_active is not None:
        updates["is_active"] = req.is_active
    if req.severity is not None:
        updates["severity"] = req.severity
    if req.parameters is not None:
        updates["parameters"] = req.parameters

    if updates:
        await rules_col.update_one({"_id": rule["_id"]}, {"$set": updates})
        rule.update(updates)

    return rule

@router.get("/sources")
async def list_regulatory_sources():
    """
    Returns source-backed regulatory knowledge excerpts grounded in official policies.
    """
    db = get_db()
    rules_col = db.get_collection("compliance_rules")
    rules = await rules_col.find().to_list(100)
    if not rules:
        rules = DEFAULT_RULES
    
    sources = []
    for r in rules:
        ref = r.get("policy_reference", {})
        if ref:
            sources.append({
                "rule_id": r.get("rule_id"),
                "rule_name": r.get("name"),
                "jurisdiction": r.get("jurisdiction"),
                "authority": ref.get("authority"),
                "clause": ref.get("section_or_clause"),
                "title": ref.get("title"),
                "source_url": ref.get("source_url"),
                "effective_date": ref.get("effective_date"),
                "excerpt": ref.get("excerpt")
            })
    return sources
