"""Add equipment name index - 添加设备名称索引

Revision ID: add_equip_name_idx
Revises: add_indexes_001
Create Date: 2025-01-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_equip_name_idx'
down_revision = 'add_indexes_001'
branch_labels = None
depends_on = None


def upgrade():
    # ### 为 equipment 表添加设备名称索引 ###
    # 用于关键词搜索优化
    op.create_index('idx_equipment_name', 'equipment', ['name'], 
                     unique=False)
    
    # 注意：如果需要全文索引（FULLTEXT），MySQL 需要特殊语法
    # 全文索引示例（如果数据库支持）：
    # op.execute("CREATE FULLTEXT INDEX idx_fulltext_name ON equipment(name)")
    # 但 MySQL 全文索引有最小词长度限制，且需要 InnoDB 5.6+ 或 MyISAM 引擎


def downgrade():
    # ### 删除设备名称索引 ###
    op.drop_index('idx_equipment_name', table_name='equipment')
    # 如果创建了全文索引，也需要删除：
    # op.execute("DROP INDEX idx_fulltext_name ON equipment")

