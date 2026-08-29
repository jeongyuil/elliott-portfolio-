from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.core.security import get_current_child_id
from app.models import ShopItem, ChildInventory
from app.schemas.shop import ShopItemResponse, InventoryResponse, PurchaseRequest, PurchaseResponse, StarRegenInfo
from app.routers.kid_home import apply_star_regen, STAR_REGEN_PER_HOUR, STAR_MAX_BALANCE

router = APIRouter()

@router.get("", response_model=dict)
async def get_shop(
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # Get Items
    stmt = select(ShopItem)
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    # Get Inventory
    inv_stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
    inv_result = await db.execute(inv_stmt)
    inventory = inv_result.scalar_one_or_none()
    
    if not inventory:
        inventory = ChildInventory(child_id=child_id)
        db.add(inventory)
        await db.commit()

    # Apply passive star regeneration
    regen = apply_star_regen(inventory)
    if regen > 0:
        await db.commit()

    return {
        "items": [ShopItemResponse.model_validate(i) for i in items],
        "inventory": InventoryResponse.model_validate(inventory),
        "starRegen": StarRegenInfo(
            rate_per_hour=STAR_REGEN_PER_HOUR,
            max_balance=STAR_MAX_BALANCE,
            last_regen_at=inventory.last_star_regen_at,
        ).model_dump(by_alias=True),
    }

@router.post("/purchase", response_model=PurchaseResponse)
async def purchase_item(
    req: PurchaseRequest,
    child_id: UUID = Depends(get_current_child_id),
    db: AsyncSession = Depends(get_db)
):
    # Get Item
    stmt = select(ShopItem).where(ShopItem.id == req.item_id)
    result = await db.execute(stmt)
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    # Get Inventory
    inv_stmt = select(ChildInventory).where(ChildInventory.child_id == child_id)
    inv_result = await db.execute(inv_stmt)
    inventory = inv_result.scalar_one_or_none()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
        
    # Only skins can be purchased now
    if item.item_type != "skin":
        raise HTTPException(status_code=400, detail="This item type is not available for purchase")

    # Check stars
    if inventory.stars < item.price:
        raise HTTPException(status_code=400, detail="Not enough stars")

    # Check if already owned
    owned = [s for s in inventory.owned_skins.split(",") if s] if inventory.owned_skins else []
    if item.id in owned:
        raise HTTPException(status_code=400, detail="Already owned")

    inventory.stars -= item.price
    owned.append(item.id)
    inventory.owned_skins = ",".join(owned)

    await db.commit()
    await db.refresh(inventory)

    return PurchaseResponse(
        success=True,
        new_stars=inventory.stars,
        inventory=InventoryResponse.model_validate(inventory)
    )
