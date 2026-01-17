//Task 6
<template>
  <div class="help-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <el-icon><QuestionFilled /></el-icon>
              <span style="margin-left: 8px; font-weight: bold">设备预约系统 - 帮助中心</span>
            </div>
          </template>

          <div class="section">
            <h3><el-icon><Promotion /></el-icon> 预约流程</h3>
            <el-steps :active="activeStep" align-center finish-status="success" style="margin-top: 20px">
              <el-step title="选择设备" description="在设备列表挑选所需仪器" />
              <el-step title="选择时段" description="避开已预约或维修时段" />
              <el-step title="提交申请" description="填写实验用途并提交" />
              <el-step title="等待审批" description="管理员将在1个工作日内审核" />
            </el-steps>
          </div>

          <el-divider />

          <div class="section">
            <h3><el-icon><List /></el-icon> 常见问题 (FAQ)</h3>
            <el-collapse v-model="activeFaq" accordion>
              <el-collapse-item title="预约提交后可以取消吗？" name="1">
                <div>在管理员审批之前，您可以在“我的预约”页面点击“取消”。若已审批通过，需联系管理员手动撤销。</div>
              </el-collapse-item>
              <el-collapse-item title="为什么我无法选择某些时间段？" name="2">
                <div>可能是该时间段已被其他同学预约，或者该设备正处于“维护中”状态。</div>
              </el-collapse-item>
              <el-collapse-item title="账号权限说明" name="3">
                <div>学生账号仅限预约；教师账号可预约并查看所在实验室设备；管理员拥有审批和用户管理权限。</div>
              </el-collapse-item>
            </el-collapse>
          </div>

          <el-divider />

          <div class="section">
            <h3><el-icon><Service /></el-icon> 技术支持</h3>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="系统管理员">湖南大学计算机学院 - 数据库小组</el-descriptions-item>
              <el-descriptions-item label="联系邮箱">admin@hnu.edu.cn</el-descriptions-item>
              <el-descriptions-item label="办公地点">信息科学与工程学院大楼 XXX 室</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { QuestionFilled, Promotion, List, Service } from '@element-plus/icons-vue'

const activeStep = ref(1)
const activeFaq = ref(['1'])
</script>

<style scoped>
.help-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 80vh;
}
.section {
  margin: 20px 0;
}
h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #409eff;
}
</style>