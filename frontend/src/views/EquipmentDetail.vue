<template>
  <div class="equipment-detail-page">
    <el-button 
      type="primary" 
      :icon="ArrowLeft" 
      @click="router.back()"
      style="margin-bottom: 20px"
    >
      返回
    </el-button>

    <el-card v-if="loading" shadow="hover">
      <el-skeleton :rows="8" animated />
    </el-card>

    <el-card v-else-if="equipment" shadow="hover" class="detail-card">
      <template #header>
        <div class="detail-header">
          <h2>{{ equipment.name }}</h2>
          <el-tag :type="getStatusType(equipment.status)" size="large">
            {{ getStatusText(equipment.status) }}
          </el-tag>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="设备ID">{{ equipment.id }}</el-descriptions-item>
        <el-descriptions-item label="设备名称">{{ equipment.name }}</el-descriptions-item>
        <el-descriptions-item label="实验室">
          {{ equipment.lab_name || '未分配' }}
        </el-descriptions-item>
        <el-descriptions-item label="类别">
          {{ equipment.category === 1 ? '学院' : equipment.category === 2 ? '实验室' : '未分类' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(equipment.status)">
            {{ getStatusText(equipment.status) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="detail-actions" v-if="userStore.isAdmin">
        <el-button type="warning" @click="handleEdit">
          <el-icon><Edit /></el-icon>
          编辑设备
        </el-button>
        <el-button type="danger" @click="handleDelete">
          <el-icon><Delete /></el-icon>
          删除设备
        </el-button>
      </div>
    </el-card>

    <el-empty v-else description="设备不存在" />

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑设备"
      width="600px"
      @close="resetEditForm"
    >
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="100px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="editForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="实验室" prop="lab_id">
          <el-select v-model="editForm.lab_id" placeholder="请选择实验室" style="width: 100%">
            <el-option
              v-for="lab in labs"
              :key="lab.id"
              :label="lab.name"
              :value="lab.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-select v-model="editForm.category" placeholder="请选择类别" style="width: 100%">
            <el-option label="学院" :value="1" />
            <el-option label="实验室" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="editForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="可用" :value="1" />
            <el-option label="使用中" :value="2" />
            <el-option label="维护中" :value="3" />
            <el-option label="已停用" :value="0" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="editLoading" @click="handleUpdate">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Edit, Delete } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getEquipmentById, updateEquipment, deleteEquipment } from '@/api/equipment'
import { getLabList } from '@/api/laboratory'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const equipment = ref(null)
const labs = ref([])
const loading = ref(false)
const showEditDialog = ref(false)
const editLoading = ref(false)

const editForm = reactive({
  name: '',
  lab_id: null,
  category: 2,
  status: 1
})

const editRules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  lab_id: [{ required: true, message: '请选择实验室', trigger: 'change' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const editFormRef = ref(null)

// 获取设备详情
const fetchEquipmentDetail = async () => {
  const id = route.params.id
  if (!id) return

  loading.value = true
  try {
    const response = await getEquipmentById(id)
    if (response.code === 200) {
      equipment.value = response.data
    }
  } catch (error) {
    console.error('获取设备详情失败:', error)
    ElMessage.error('获取设备详情失败')
  } finally {
    loading.value = false
  }
}

// 获取实验室列表
const fetchLabs = async () => {
  try {
    const response = await getLabList()
    if (response.code === 200) {
      labs.value = response.data.items || response.data || []
    }
  } catch (error) {
    console.error('获取实验室列表失败:', error)
  }
}

// 编辑
const handleEdit = () => {
  if (!equipment.value) return
  
  editForm.name = equipment.value.name || ''
  editForm.lab_id = equipment.value.lab_id || null
  editForm.category = equipment.value.category || 2
  editForm.status = equipment.value.status !== undefined ? equipment.value.status : 1
  showEditDialog.value = true
}

// 更新
const handleUpdate = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      editLoading.value = true
      try {
        const id = route.params.id
        const { ...formData } = editForm
        // 确保数据类型正确
        const requestData = {
          name: formData.name,
          lab_id: formData.lab_id,
          category: Number(formData.category),
          status: Number(formData.status)
        }
        const response = await updateEquipment(id, requestData)
        if (response.code === 200) {
          ElMessage.success('更新成功')
          showEditDialog.value = false
          fetchEquipmentDetail()
        }
      } catch (error) {
        console.error('更新设备失败:', error)
      } finally {
        editLoading.value = false
      }
    }
  })
}

// 删除
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除该设备吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const id = route.params.id
    const response = await deleteEquipment(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      router.push('/equipment')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除设备失败:', error)
    }
  }
}

// 重置编辑表单
const resetEditForm = () => {
  Object.assign(editForm, {
    name: '',
    lab_id: null,
    category: 2,
    status: 1
  })
  editFormRef.value?.resetFields()
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    1: '可用',
    2: '使用中',
    3: '维护中',
    0: '已停用'
  }
  return statusMap[status] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    1: 'success',  // 可用
    2: 'warning',  // 使用中
    3: 'info',  // 维护中
    0: 'danger'  // 已停用
  }
  return statusMap[status] || ''
}

// 初始化
onMounted(() => {
  fetchLabs()
  fetchEquipmentDetail()
})
</script>

<style scoped lang="scss">
.equipment-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.detail-card {
  border-radius: 8px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.detail-actions {
  margin-top: 24px;
  display: flex;
  gap: 12px;
}
</style>

