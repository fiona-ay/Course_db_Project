"""
实验室服务层
处理实验室相关的业务逻辑
"""
from app import db
from app.models.laboratory import Laboratory
from app.models.student import Student
from app.utils.exceptions import NotFoundError, ValidationError


def get_lab_list():
    """
    查询所有实验室
    
    Returns:
        list: 实验室对象列表
    """
    labs = Laboratory.query.all()
    return labs


def get_lab_by_id(lab_id):
    """
    根据 ID 查询实验室
    
    Args:
        lab_id: 实验室ID
    
    Returns:
        Laboratory: 实验室对象
    
    Raises:
        NotFoundError: 实验室不存在
    """
    lab = Laboratory.query.get(lab_id)
    if not lab:
        raise NotFoundError('实验室不存在')
    return lab


def create_lab(data):
    """
    创建新实验室
    
    Args:
        data: 实验室数据字典，包含 name 和 location
    
    Returns:
        Laboratory: 创建的实验室对象
    
    Raises:
        ValidationError: 数据验证失败
    """
    # 检查名称是否已存在
    existing_lab = Laboratory.query.filter_by(name=data.get('name')).first()
    if existing_lab:
        raise ValidationError('实验室名称已存在', payload={'field': 'name'})
    
    # 创建实验室
    lab = Laboratory(
        name=data.get('name'),
        location=data.get('location')
    )
    
    try:
        db.session.add(lab)
        db.session.commit()
        return lab
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'创建实验室失败: {str(e)}')


def update_lab(lab_id, data):
    """
    更新实验室信息
    关键逻辑：修改实验室名称后，需要更新 Student 表中的 lab_name 冗余字段
    
    Args:
        lab_id: 实验室ID
        data: 更新数据字典
    
    Returns:
        Laboratory: 更新后的实验室对象
    
    Raises:
        NotFoundError: 实验室不存在
        ValidationError: 数据验证失败
    """
    lab = get_lab_by_id(lab_id)
    
    # 检查名称是否与其他实验室冲突
    if 'name' in data and data['name'] != lab.name:
        existing_lab = Laboratory.query.filter(
            Laboratory.name == data['name'],
            Laboratory.id != lab_id
        ).first()
        if existing_lab:
            raise ValidationError('实验室名称已存在', payload={'field': 'name'})
        
        old_name = lab.name
        new_name = data['name']
        
        # 更新实验室名称
        lab.name = new_name
        
        # 关键逻辑：更新 Student 表中的冗余字段 lab_name
        # 使用 SQLAlchemy 的 update 语句进行批量更新
        Student.query.filter_by(lab_id=lab_id).update(
            {'lab_name': new_name},
            synchronize_session=False
        )
    else:
        # 只更新其他字段
        if 'location' in data:
            lab.location = data['location']
    
    try:
        db.session.commit()
        return lab
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'更新实验室失败: {str(e)}')


def delete_lab(lab_id):
    """
    删除实验室
    
    Args:
        lab_id: 实验室ID
    
    Returns:
        bool: 删除成功返回 True
    
    Raises:
        NotFoundError: 实验室不存在
        ValidationError: 删除失败（如存在关联数据）
    """
    lab = get_lab_by_id(lab_id)
    
    # 检查是否存在关联数据（可选：根据业务需求决定是否允许删除）
    # 这里仅做示例，实际应根据业务需求决定
    student_count = Student.query.filter_by(lab_id=lab_id).count()
    if student_count > 0:
        raise ValidationError(f'无法删除实验室，存在 {student_count} 个关联的学生', payload={'students': student_count})
    
    try:
        db.session.delete(lab)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'删除实验室失败: {str(e)}')

