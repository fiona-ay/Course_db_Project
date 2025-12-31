<template>
  <div class="laboratory-list">
    <!-- 页面标题卡片 -->
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-icon float">
        <el-icon :size="48"><OfficeBuilding /></el-icon>
      </div>
      <div>
        <h2 class="page-title gradient-text">实验室管理</h2>
        <p class="page-subtitle">管理和查看所有实验室信息</p>
      </div>
    </div>

    <!-- 主要内容卡片 -->
    <el-card class="main-card glass-card animate__animated animate__fadeInUp" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="card-title">
            <el-icon><List /></el-icon>
            实验室列表
          </span>
          <el-button 
            type="primary" 
            @click="handleAdd"
            class="cute-button"
            :icon="Plus"
          >
            新增实验室
          </el-button>
        </div>
      </template>

      <!-- 表格容器 -->
      <div class="table-container">
        <el-table
          v-loading="loading"
          :data="labList"
          stripe
          style="width: 100%"
          class="cute-table"
          :row-class-name="tableRowClassName"
        >
          <el-table-column prop="id" label="ID" width="80" align="center">
            <template #default="{ row }">
              <el-tag type="info" effect="plain" round>{{ row.id }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="name" label="实验室名称">
            <template #default="{ row }">
              <div class="name-cell">
                <el-icon class="name-icon"><OfficeBuilding /></el-icon>
                <span class="name-text">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="location" label="实验室位置">
            <template #default="{ row }">
              <div class="location-cell">
                <el-icon><Location /></el-icon>
                <span>{{ row.location || '未设置' }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="220" fixed="right" align="center">
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                @click="handleEdit(row)"
                :icon="Edit"
                class="cute-button"
                round
              >
                编辑
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(row)"
                :icon="Delete"
                class="cute-button"
                round
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 空状态 -->
        <el-empty 
          v-if="!loading && labList.length === 0" 
          description="暂无实验室数据"
          :image-size="120"
        >
          <el-button type="primary" @click="handleAdd" class="cute-button">
            创建第一个实验室
          </el-button>
        </el-empty>
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="520px"
      @close="resetForm"
      class="cute-dialog"
      :close-on-click-modal="false"
    >
      <div class="dialog-icon-container">
        <div class="dialog-icon float" :class="editingId ? 'edit-icon' : 'add-icon'">
          <el-icon :size="40">
            <component :is="editingId ? Edit : Plus" />
          </el-icon>
        </div>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        label-position="left"
        class="cute-form"
      >
        <el-form-item label="实验室名称" prop="name">
          <el-input 
            v-model="form.name" 
            placeholder="请输入实验室名称"
            :prefix-icon="OfficeBuilding"
            clearable
            size="large"
          />
        </el-form-item>
        <el-form-item label="实验室位置" prop="location">
          <el-input 
            v-model="form.location" 
            placeholder="请输入实验室位置"
            :prefix-icon="Location"
            clearable
            size="large"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false" size="large" round>
            取消
          </el-button>
          <el-button 
            type="primary" 
            @click="handleSubmit" 
            :loading="submitting"
            size="large"
            class="cute-button"
            round
          >
            {{ submitting ? '提交中...' : '确定' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Plus, Edit, Delete, OfficeBuilding, Location, List 
} from '@element-plus/icons-vue'
import { getLabList, createLab, updateLab, deleteLab } from '@/api/laboratory'

const loading = ref(false)
const labList = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('新增实验室')
const submitting = ref(false)
const formRef = ref(null)
const editingId = ref(null)

const form = reactive({
  name: '',
  location: ''
})

const rules = {
  name: [
    { required: true, message: '请输入实验室名称', trigger: 'blur' },
    { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  location: [
    { max: 100, message: '长度不能超过 100 个字符', trigger: 'blur' }
  ]
}

// 表格行类名（用于动画）
const tableRowClassName = ({ rowIndex }) => {
  return `table-row-${rowIndex}`
}

// 获取列表
const fetchList = async () => {
  loading.value = true
  try {
    const res = await getLabList()
    labList.value = res.data || []
  } catch (error) {
    console.error('获取实验室列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 新增
const handleAdd = () => {
  dialogTitle.value = '新增实验室'
  editingId.value = null
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row) => {
  dialogTitle.value = '编辑实验室'
  editingId.value = row.id
  form.name = row.name
  form.location = row.location || ''
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除实验室"${row.name}"吗？`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        customClass: 'cute-message-box'
      }
    )
    
    await deleteLab(row.id)
    ElMessage.success({
      message: '删除成功！',
      type: 'success',
      duration: 2000,
      showClose: true
    })
    fetchList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    if (editingId.value) {
      // 更新
      await updateLab(editingId.value, {
        name: form.name,
        location: form.location
      })
      ElMessage.success({
        message: '更新成功！',
        type: 'success',
        duration: 2000
      })
    } else {
      // 新增
      await createLab({
        name: form.name,
        location: form.location
      })
      ElMessage.success({
        message: '创建成功！',
        type: 'success',
        duration: 2000
      })
    }
    
    dialogVisible.value = false
    fetchList()
  } catch (error) {
    if (error !== false) {
      console.error('提交失败:', error)
    }
  } finally {
    submitting.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.name = ''
  form.location = ''
  editingId.value = null
  formRef.value?.resetFields()
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped lang="scss">
.laboratory-list {
  max-width: 1400px;
  margin: 0 auto;
  animation: slideInUp 0.6s ease-out;
}

/* 页面标题 */
.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding: 24px 32px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);

  .header-icon {
    width: 80px;
    height: 80px;
    border-radius: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  }

  .page-title {
    margin: 0 0 8px 0;
    font-size: 28px;
    font-weight: 700;
  }

  .page-subtitle {
    margin: 0;
    color: #666;
    font-size: 14px;
  }
}

.main-card {
  border: none;
  
  :deep(.el-card__header) {
    border-bottom: 2px solid rgba(102, 126, 234, 0.1);
    padding: 20px 24px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  }

  :deep(.el-card__body) {
    padding: 24px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .card-title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

/* 表格样式 */
.table-container {
  margin-top: 16px;
}

.cute-table {
  :deep(.el-table__header) {
    th {
      background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      color: #333;
      font-weight: 600;
      border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
  }

  :deep(.el-table__body) {
    tr {
      transition: all 0.3s ease;

      &:hover {
        background: rgba(102, 126, 234, 0.05) !important;
        transform: scale(1.01);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
      }
    }

    td {
      border-bottom: 1px solid rgba(102, 126, 234, 0.1);
    }
  }

  :deep(.el-table--striped) {
    .el-table__body {
      tr.el-table__row--striped {
        background: rgba(102, 126, 234, 0.02);
      }
    }
  }
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;

  .name-icon {
    color: #667eea;
    font-size: 18px;
  }

  .name-text {
    color: #333;
  }
}

.location-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;

  .el-icon {
    color: #999;
  }
}

/* 对话框样式 */
.cute-dialog {
  :deep(.el-dialog) {
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
  }

  :deep(.el-dialog__header) {
    padding: 24px 24px 0;
    border-bottom: none;
    text-align: center;
  }

  :deep(.el-dialog__title) {
    font-size: 22px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  :deep(.el-dialog__body) {
    padding: 24px;
  }
}

.dialog-icon-container {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.dialog-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);

  &.add-icon {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  }

  &.edit-icon {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  }
}

.cute-form {
  :deep(.el-form-item__label) {
    font-weight: 500;
    color: #333;
  }

  :deep(.el-input__wrapper) {
    border-radius: 10px;
    transition: all 0.3s ease;

    &:hover {
      box-shadow: 0 0 0 1px #667eea inset;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
}

/* 按钮样式增强 */
.cute-button {
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

/* 空状态 */
:deep(.el-empty) {
  padding: 60px 0;
  
  .el-empty__description {
    color: #999;
    font-size: 14px;
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    text-align: center;
  }

  .card-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>
