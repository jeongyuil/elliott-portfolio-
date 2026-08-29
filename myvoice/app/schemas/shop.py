from datetime import datetime
from pydantic import BaseModel
from app.schemas.base import CamelModel

class ShopItemResponse(CamelModel):
    id: str
    name: str
    description: str
    emoji: str
    price: int
    item_type: str

class InventoryResponse(CamelModel):
    stars: int
    owned_skins: list[str] = []
    active_popo_skin: str | None = None
    active_luna_skin: str | None = None

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # Convert comma-separated string to list for ORM objects
        if hasattr(obj, 'owned_skins') and isinstance(obj.owned_skins, str):
            data = {
                'stars': obj.stars,
                'owned_skins': [s for s in obj.owned_skins.split(',') if s],
                'active_popo_skin': obj.active_popo_skin,
                'active_luna_skin': obj.active_luna_skin,
            }
            return super().model_validate(data, **kwargs)
        return super().model_validate(obj, **kwargs)

class StarRegenInfo(CamelModel):
    rate_per_hour: int
    max_balance: int
    last_regen_at: datetime | None = None

class PurchaseRequest(BaseModel):
    item_id: str

class PurchaseResponse(CamelModel):
    success: bool
    new_stars: int
    inventory: InventoryResponse
