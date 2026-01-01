"""
设备服务层
处理设备相关的业务逻辑
"""
from app import db
from app.models.equipment import Equipment
from app.models.laboratory import Laboratory
from app.utils.exceptions import NotFoundError, ValidationError


def get_equipment_list(lab_id=None, keyword=None, category=None, status=None):
    """
    查询设备列表（支持筛选）
    
    Args:
        lab_id: 实验室ID筛选
        keyword: 关键词搜索（设备名称）
        category: 设备类别筛选
        status: 设备状态筛选
    
    Returns:
        list: 设备列表
    """
    query = Equipment.query
    
    # 按实验室ID筛选
    if lab_id is not None:
        query = query.filter(Equipment.lab_id == lab_id)
    
    # 关键词搜索（设备名称）
    if keyword:
        # 使用 LIKE 查询（MySQL 会自动使用索引）
        query = query.filter(Equipment.name.like(f'%{keyword}%'))
    
    # 按类别筛选
    if category is not None:
        query = query.filter(Equipment.category == category)
    
    # 按状态筛选
    if status is not None:
        query = query.filter(Equipment.status == status)
    
    # 按ID排序
    query = query.order_by(Equipment.id)
    
    return query.all()


def get_equipment_by_id(equip_id):
    """
    根据 ID 查询设备
    
    Args:
        equip_id: 设备ID
    
    Returns:
        Equipment: 设备对象
    
    Raises:
        NotFoundError: 设备不存在
    """
    equipment = Equipment.query.get(equip_id)
    if not equipment:
        raise NotFoundError('设备不存在')
    return equipment


def create_equipment(data):
    """
    创建新设备
    
    Args:
        data: 设备数据字典
    
    Returns:
        Equipment: 创建的设备对象
    
    Raises:
        ValidationError: 数据验证失败
    """
    # 如果指定了实验室ID，验证实验室是否存在
    if data.get('lab_id'):
        lab = Laboratory.query.get(data['lab_id'])
        if not lab:
            raise ValidationError('指定的实验室不存在', payload={'field': 'lab_id'})
    
    # 创建设备
    equipment = Equipment(
        name=data.get('name'),
        lab_id=data.get('lab_id'),
        category=data.get('category'),
        status=data.get('status', 1)
    )
    
    try:
        db.session.add(equipment)
        db.session.commit()
        return equipment
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'创建设备失败: {str(e)}')


def update_equipment(equip_id, data):
    """
    更新设备信息
    
    Args:
        equip_id: 设备ID
        data: 更新数据字典
    
    Returns:
        Equipment: 更新后的设备对象
    
    Raises:
        NotFoundError: 设备不存在
        ValidationError: 数据验证失败
    """
    equipment = get_equipment_by_id(equip_id)
    
    # 如果指定了实验室ID，验证实验室是否存在
    if 'lab_id' in data and data['lab_id']:
        lab = Laboratory.query.get(data['lab_id'])
        if not lab:
            raise ValidationError('指定的实验室不存在', payload={'field': 'lab_id'})
    
    # 更新字段
    if 'name' in data:
        equipment.name = data['name']
    if 'lab_id' in data:
        equipment.lab_id = data['lab_id']
    if 'category' in data:
        equipment.category = data['category']
    if 'status' in data:
        equipment.status = data['status']
    if 'next_avail_time' in data:
        equipment.next_avail_time = data['next_avail_time']
    
    try:
        db.session.commit()
        return equipment
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'更新设备失败: {str(e)}')


def delete_equipment(equip_id):
    """
    删除设备
    
    Args:
        equip_id: 设备ID
    
    Returns:
        bool: 删除成功返回 True
    
    Raises:
        NotFoundError: 设备不存在
        ValidationError: 删除失败（如存在关联数据）
    """
    equipment = get_equipment_by_id(equip_id)
    
    # 检查是否存在关联数据（预约记录）
    reservation_count = equipment.reservations.count()
    if reservation_count > 0:
        raise ValidationError(f'无法删除设备，存在 {reservation_count} 条关联的预约记录', payload={'reservations': reservation_count})
    
    try:
        db.session.delete(equipment)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'删除设备失败: {str(e)}')

