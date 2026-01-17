"""
预约服务层
处理预约相关的业务逻辑
"""
from datetime import datetime
from app import db
from app.models.reservation import Reservation
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.equipment import Equipment
from app.utils.exceptions import NotFoundError, ValidationError
from app.utils.redis_client import redis_client


def create_reservation(data, current_user):
    """
    创建预约（学生/教师）
    
    Args:
        data: 预约数据字典
        current_user: 当前用户信息
    
    Returns:
        Reservation: 创建的预约对象
    
    Raises:
        ValidationError: 数据验证失败
    """
    # 验证设备是否存在
    equipment = Equipment.query.get(data.get('equip_id'))
    if not equipment:
        raise ValidationError('设备不存在', payload={'field': 'equip_id'})
    
    # 根据用户类型设置用户ID
    user_id = current_user['user_id']
    user_type = current_user['user_type']
    
    # 填充冗余字段
    user_name = None
    if user_type == 'student':
        student = Student.query.get(user_id)
        if not student:
            raise ValidationError('学生不存在')
        user_name = student.name
        data['student_id'] = user_id
        data['teacher_id'] = None
    elif user_type == 'teacher':
        teacher = Teacher.query.get(user_id)
        if not teacher:
            raise ValidationError('教师不存在')
        user_name = teacher.name
        data['student_id'] = None
        data['teacher_id'] = user_id
    else:
        raise ValidationError('用户类型不支持预约')
    
    # 创建预约
    reservation = Reservation(
        equip_id=data['equip_id'],
        student_id=data.get('student_id'),
        teacher_id=data.get('teacher_id'),
        status=0,  # 待审
        apply_time=datetime.utcnow(),
        user_name=user_name,
        equip_name=equipment.name,
        price=data.get('price'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time')
    )
    
    try:
        db.session.add(reservation)
        db.session.commit()
        
        # 清除相关缓存
        _clear_reservation_cache()
        
        return reservation
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'创建预约失败: {str(e)}')


def get_reservation_list(user_id=None, equip_id=None, status=None, user_type=None):
    """
    获取预约列表（支持筛选）
    
    Args:
        user_id: 用户ID筛选
        equip_id: 设备ID筛选
        status: 状态筛选
        user_type: 用户类型（student/teacher）
    
    Returns:
        list: 预约列表
    """
    query = Reservation.query
    
    # 按用户ID筛选
    if user_id and user_type:
        if user_type == 'student':
            query = query.filter(Reservation.student_id == user_id)
        elif user_type == 'teacher':
            query = query.filter(Reservation.teacher_id == user_id)
    
    # 按设备ID筛选
    if equip_id is not None:
        query = query.filter(Reservation.equip_id == equip_id)
    
    # 按状态筛选
    if status is not None:
        query = query.filter(Reservation.status == status)
    
    # 按申请时间倒序排列
    query = query.order_by(Reservation.apply_time.desc())
    
    return query.all()


def get_reservation_by_id(reservation_id):
    """
    根据 ID 查询预约详情
    
    Args:
        reservation_id: 预约ID
    
    Returns:
        Reservation: 预约对象
    
    Raises:
        NotFoundError: 预约不存在
    """
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        raise NotFoundError('预约不存在')
    return reservation


def update_reservation_status(reservation_id, status, approver_id=None):
    """
    更新预约状态（审批）
    
    Args:
        reservation_id: 预约ID
        status: 新状态
        approver_id: 审批人ID
    
    Returns:
        Reservation: 更新后的预约对象
    
    Raises:
        NotFoundError: 预约不存在
        ValidationError: 状态更新失败
    """
    reservation = get_reservation_by_id(reservation_id)
    
    # 验证状态流转
    valid_transitions = {
        0: [1, 2, 3],  # 待审 → 通过/拒绝/取消
        1: [3],        # 通过 → 取消
        2: [],         # 拒绝 → 无
        3: []          # 取消 → 无
    }
    
    if status not in valid_transitions.get(reservation.status, []):
        raise ValidationError(f'无效的状态流转: {reservation.status} -> {status}')
    
    # 更新状态
    reservation.status = status
    if status in [1, 2]:  # 审批通过或拒绝
        reservation.approver_id = approver_id
        reservation.approve_time = datetime.utcnow()
    
    try:
        db.session.commit()
        
        # 清除相关缓存
        _clear_reservation_cache(reservation_id=reservation_id)
        
        return reservation
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'更新预约状态失败: {str(e)}')


def delete_reservation(reservation_id):
    """
    删除预约
    
    Args:
        reservation_id: 预约ID
    
    Returns:
        bool: 删除成功返回 True
    
    Raises:
        NotFoundError: 预约不存在
        ValidationError: 删除失败
    """
    reservation = get_reservation_by_id(reservation_id)
    
    try:
        db.session.delete(reservation)
        db.session.commit()
        
        # 清除相关缓存
        _clear_reservation_cache(reservation_id=reservation_id)
        
        return True
    except Exception as e:
        db.session.rollback()
        raise ValidationError(f'删除预约失败: {str(e)}')


def _clear_reservation_cache(reservation_id=None):
    """
    清除预约相关缓存
    
    Args:
        reservation_id: 预约ID，如果提供则清除该预约的详情缓存
    """
    # 清除详情缓存
    if reservation_id:
        redis_client.delete(f'api:reservation:detail:{reservation_id}')
    
    # 清除列表缓存（使用通配符删除所有相关缓存）
    keys = redis_client.keys('api:reservation:list:*')
    for key in keys:
        redis_client.delete(key)