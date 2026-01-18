"""
API v1 Schemas 模块
包含所有 DTO/Schema 定义
"""
from app.api.v1.schemas.lab_schema import (
    LaboratorySchema, LaboratoryCreateSchema, LaboratoryUpdateSchema
)
from app.api.v1.schemas.equipment_schema import (
    EquipmentSchema, EquipmentCreateSchema, EquipmentUpdateSchema, EquipmentQuerySchema
)
from app.api.v1.schemas.timeslot_schema import (
    TimeSlotSchema, TimeSlotCreateSchema, TimeSlotUpdateSchema
)

__all__ = [
    'LaboratorySchema',
    'LaboratoryCreateSchema',
    'LaboratoryUpdateSchema',
    'EquipmentSchema',
    'EquipmentCreateSchema',
    'EquipmentUpdateSchema',
    'EquipmentQuerySchema',
    'TimeSlotSchema',
    'TimeSlotCreateSchema',
    'TimeSlotUpdateSchema',
]
