<template>
  <div class="equipment-page">
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><Box /></el-icon>
        设备列表
      </h2>
      <el-button 
        v-if="userStore.isAdmin" 
        type="primary" 
        @click="showCreateDialog = true"
      >
        <el-icon><Plus /></el-icon>
        新增设备
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="filter-card" shadow="hover">
      <el-form :model="filterForm" inline>
        <el-form-item label="实验室">
          <el-select 
            v-model="filterForm.lab_id" 
            placeholder="请选择实验室" 
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="lab in labs"
              :key="lab.id"
              :label="lab.name"
              :value="lab.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="filterForm.keyword"
            placeholder="请输入设备名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="类别">
          <el-select 
            v-model="filterForm.category" 
            placeholder="请选择类别" 
            clearable
            style="width: 150px"
          >
            <el-option label="学院" :value="1" />
            <el-option label="实验室" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select 
            v-model="filterForm.status" 
            placeholder="请选择状态" 
            clearable
            style="width: 150px"
          >
            <el-option label="可用" :value="1" />
            <el-option label="使用中" :value="2" />
            <el-option label="维护中" :value="3" />
            <el-option label="已停用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 设备列表 -->
    <el-card class="list-card" shadow="hover">
      <el-empty v-if="!loading && equipmentList.length === 0" description="暂无设备数据" />
      <el-skeleton v-else-if="loading" :rows="5" animated />
      <div v-else class="equipment-grid">
        <el-card
          v-for="equipment in equipmentList"
          :key="equipment.id"
          class="equipment-card"
          shadow="hover"
          @click="handleViewDetail(equipment.id)"
        >
          <div class="equipment-header">
            <h3 class="equipment-name">{{ equipment.name }}</h3>
            <el-tag :type="getStatusType(equipment.status)">
              {{ getStatusText(equipment.status) }}
            </el-tag>
          </div>
          <div class="equipment-info">
            <div class="info-item">
              <el-icon><OfficeBuilding /></el-icon>
              <span>实验室：{{ equipment.lab_name || '未分配' }}</span>
            </div>
            <div class="info-item">
              <el-icon><Collection /></el-icon>
              <span>类别：{{ equipment.category === 1 ? '学院' : equipment.category === 2 ? '实验室' : '未分类' }}</span>
            </div>
          </div>
          <div class="equipment-actions">
            <el-button type="primary" size="small" @click.stop="handleViewDetail(equipment.id)">
              查看详情
            </el-button>
            <el-button
              v-if="userStore.isAdmin"
              type="warning"
              size="small"
              @click.stop="handleEdit(equipment)"
            >
              编辑
            </el-button>
            <el-button
              v-if="userStore.isAdmin"
              type="danger"
              size="small"
              @click.stop="handleDelete(equipment.id)"
            >
              删除
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 分页 -->
      <el-pagination
        v-if="total > 0"
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </el-card>

    <!-- 创建设备对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      title="新增设备"
      width="600px"
      @close="resetCreateForm"
    >
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="100px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="createForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="实验室" prop="lab_id">
          <el-select v-model="createForm.lab_id" placeholder="请选择实验室" style="width: 100%">
            <el-option
              v-for="lab in labs"
              :key="lab.id"
              :label="lab.name"
              :value="lab.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="类别" prop="category">
          <el-select v-model="createForm.category" placeholder="请选择类别" style="width: 100%">
            <el-option label="学院" :value="1" />
            <el-option label="实验室" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="createForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="可用" :value="1" />
            <el-option label="使用中" :value="2" />
            <el-option label="维护中" :value="3" />
            <el-option label="已停用" :value="0" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" :loading="createLoading" @click="handleCreate">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑设备对话框 -->
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Box,
  Plus,
  Search,
  Refresh,
  OfficeBuilding,
  Collection,
  InfoFilled
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { getEquipmentList, createEquipment, updateEquipment, deleteEquipment } from '@/api/equipment'
import { getLabList } from '@/api/laboratory'

const router = useRouter()
const userStore = useUserStore()

// 数据
const equipmentList = ref([])
const labs = ref([])
const loading = ref(false)
const total = ref(0)

// 筛选表单
const filterForm = reactive({
  lab_id: null,
  keyword: '',
  category: '',
  status: ''
})

// 分页
const pagination = reactive({
  page: 1,
  page_size: 10
})

// 对话框
const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const createLoading = ref(false)
const editLoading = ref(false)

// 创建表单
const createForm = reactive({
  name: '',
  lab_id: null,
  category: 2, // 默认为 2（实验室）
  status: 1 // 默认为 1（可用）
})

const createRules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  lab_id: [{ required: true, message: '请选择实验室', trigger: 'change' }],
  category: [{ required: true, message: '请选择类别', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const createFormRef = ref(null)

// 编辑表单
const editForm = reactive({
  id: null,
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

// 获取设备列表
const fetchEquipmentList = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...filterForm
    }
    // 移除空值
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) {
        delete params[key]
      }
    })
    
    const response = await getEquipmentList(params)
    if (response.code === 200) {
      equipmentList.value = response.data.items || response.data || []
      total.value = response.data.total || equipmentList.value.length
    }
  } catch (error) {
    console.error('获取设备列表失败:', error)
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

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchEquipmentList()
}

// 重置
const handleReset = () => {
  filterForm.lab_id = null
  filterForm.keyword = ''
  filterForm.category = ''
  filterForm.status = ''
  handleSearch()
}

// 查看详情
const handleViewDetail = (id) => {
  router.push(`/equipment/${id}`)
}

// 编辑
const handleEdit = (equipment) => {
  editForm.id = equipment.id
  editForm.name = equipment.name || ''
  editForm.lab_id = equipment.lab_id || null
  editForm.category = equipment.category || 2
  editForm.status = equipment.status !== undefined ? equipment.status : 1
  showEditDialog.value = true
}

// 创建
const handleCreate = async () => {
  if (!createFormRef.value) return
  
  await createFormRef.value.validate(async (valid) => {
    if (valid) {
      createLoading.value = true
      try {
        // 确保数据类型正确
        const requestData = {
          name: createForm.name,
          lab_id: createForm.lab_id,
          category: Number(createForm.category),
          status: Number(createForm.status)
        }
        
        const response = await createEquipment(requestData)
        if (response.code === 200) {
          ElMessage.success('创建成功')
          showCreateDialog.value = false
          fetchEquipmentList()
        }
      } catch (error) {
        console.error('创建设备失败:', error)
      } finally {
        createLoading.value = false
      }
    }
  })
}

// 更新
const handleUpdate = async () => {
  if (!editFormRef.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      editLoading.value = true
      try {
        const { id, ...formData } = editForm
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
          fetchEquipmentList()
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
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该设备吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    const response = await deleteEquipment(id)
    if (response.code === 200) {
      ElMessage.success('删除成功')
      fetchEquipmentList()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除设备失败:', error)
    }
  }
}

// 重置创建表单
const resetCreateForm = () => {
  Object.assign(createForm, {
    name: '',
    lab_id: null,
    category: 2,
    status: 1
  })
  createFormRef.value?.resetFields()
}

// 重置编辑表单
const resetEditForm = () => {
  Object.assign(editForm, {
    id: null,
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

// 分页变化
const handleSizeChange = () => {
  fetchEquipmentList()
}

const handlePageChange = () => {
  fetchEquipmentList()
}

// 初始化
onMounted(() => {
  fetchLabs()
  fetchEquipmentList()
})
</script>

<style scoped lang="scss">
.equipment-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

  .page-title {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.filter-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.list-card {
  border-radius: 8px;
}

.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
  margin-bottom: 20px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.equipment-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.equipment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .equipment-name {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
    flex: 1;
  }
}

.equipment-info {
  margin-bottom: 16px;

  .info-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 14px;
    color: #666;

    &:last-child {
      margin-bottom: 0;
    }

    .el-icon {
      color: #999;
    }
  }
}

.equipment-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination {
  margin-top: 20px;
  justify-content: center;
}
</style>
