<script setup lang="ts">
import { computed, ref, watch } from 'vue'

type PlatformTab = 'overview' | 'processing' | 'construction' | 'query' | 'service'
type ServiceField = {
  name: string
  type: string
  required?: boolean
  description: string
}
type ServiceModule = {
  key: string
  title: string
  endpoint: string
  method: 'POST'
  requestFields: ServiceField[]
  responseFields: ServiceField[]
  requestExample: Record<string, string | number | boolean | string[]>
  responseExample: { data: Record<string, unknown> }
  resultRows: Array<{ label: string; value: string }>
  evidence: string[]
}

const commonResponseFields: ServiceField[] = [
  { name: 'code', type: 'number', description: '服务状态码' },
  { name: 'message', type: 'string', description: '服务返回信息' },
  { name: 'data', type: 'object', description: '结构化业务结果、图谱节点关系和证据链' },
  { name: 'confidence', type: 'number', description: '综合置信度' },
  { name: 'evidence', type: 'array', description: '支撑本次结果的数据来源和证据' },
]

const modules: ServiceModule[] = [
  {
    key: 'expert-direct',
    title: '科技专家/人才直接关系',
    endpoint: '/api/v1/kg-service/expert-direct-relation',
    method: 'POST',
    requestFields: [
      { name: 'source_expert_id', type: 'string', required: true, description: '第一个专家唯一标识' },
      { name: 'target_expert_id', type: 'string', required: false, description: '第二个专家唯一标识' },
      { name: 'relation_scene', type: 'string', required: false, description: '交互场景筛选条件' },
      { name: 'start_time', type: 'string', required: false, description: '关系起始时间' },
    ],
    responseFields: commonResponseFields,
    requestExample: { source_expert_id: 'E10001', target_expert_id: 'E10002', relation_scene: '科研合作', start_time: '2020-01' },
    responseExample: { data: { relation_type: '论文合作', relation_count: 12, scenario: '科研合作', confidence: 0.94 } },
    resultRows: [{ label: '直接关系', value: '12' }, { label: '关系类型', value: '4' }, { label: '关联成果', value: '18' }, { label: '最高置信度', value: '0.94' }],
    evidence: ['共同发表论文 4 篇，作者列表和单位信息一致。', '共同参与项目 3 项，项目角色存在协作链路。', '关系发生时间、场景和成果均已结构化记录。'],
  },
  {
    key: 'node-indirect',
    title: '科技单节点间接关系',
    endpoint: '/api/v1/kg-service/node-indirect-relation',
    method: 'POST',
    requestFields: [
      { name: 'core_node_id', type: 'string', required: true, description: '核心专家或人才节点 ID' },
      { name: 'relation_types', type: 'array', required: false, description: '间接关系类型' },
      { name: 'path_depth', type: 'number', required: false, description: '路径分析深度' },
      { name: 'min_strength', type: 'number', required: false, description: '最小关联强度阈值' },
    ],
    responseFields: commonResponseFields,
    requestExample: { core_node_id: 'E10001', relation_types: ['学术关联', '机构关联'], path_depth: 2, min_strength: 0.65 },
    responseExample: { data: { indirect_nodes: 36, paths: 58, average_strength: 0.76 } },
    resultRows: [{ label: '间接节点', value: '36' }, { label: '路径数量', value: '58' }, { label: '关系类型', value: '4' }, { label: '平均强度', value: '0.76' }],
    evidence: ['路径：张明远 -> 李佳宁 -> 专家C。', '路径深度为 2，命中学术关联和机构关联。', '每条间接关系均返回传递路径和强度。'],
  },
  {
    key: 'two-point-achievement',
    title: '科技两点合作成果',
    endpoint: '/api/v1/kg-service/two-point-achievements',
    method: 'POST',
    requestFields: [
      { name: 'source_expert_id', type: 'string', required: true, description: '第一个专家唯一标识' },
      { name: 'target_expert_id', type: 'string', required: true, description: '第二个专家唯一标识' },
      { name: 'achievement_type', type: 'string', required: false, description: '成果类型' },
      { name: 'time_range', type: 'string', required: false, description: '成果时间范围' },
    ],
    responseFields: commonResponseFields,
    requestExample: { source_expert_id: 'E10001', target_expert_id: 'E10002', achievement_type: '论文/专利/项目', time_range: '2020-2026' },
    responseExample: { data: { papers: 8, patents: 3, projects: 2, contribution: '共同算法模型' } },
    resultRows: [{ label: '合作论文', value: '8' }, { label: '合作专利', value: '3' }, { label: '共同项目', value: '2' }, { label: '价值评分', value: '91' }],
    evidence: ['按论文、专利、项目分类统计合作成果。', '标注完成时间、所属领域和奖项评价。', '输出核心贡献和合作模式。'],
  },
  {
    key: 'expert-colleague',
    title: '科技专家同事关系',
    endpoint: '/api/v1/kg-service/expert-colleague-relation',
    method: 'POST',
    requestFields: [
      { name: 'expert_id', type: 'string', required: true, description: '专家唯一标识' },
      { name: 'organization', type: 'string', required: false, description: '任职机构筛选' },
      { name: 'department', type: 'string', required: false, description: '部门或团队筛选' },
      { name: 'overlap_period', type: 'string', required: false, description: '任职重叠时间' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', organization: '中国科学院自动化研究所', department: '智能系统实验室', overlap_period: '2018-2022' },
    responseExample: { data: { colleagues: 18, teams: 4, overlap_years: 4, achievements: 6 } },
    resultRows: [{ label: '同事关系', value: '18' }, { label: '共同团队', value: '4' }, { label: '重叠年限', value: '4' }, { label: '期间成果', value: '6' }],
    evidence: ['任职时间存在重叠，机构层级匹配到同一实验室。', '标注共同工作内容和协作场景。', '关联同事期间产生的合作成果。'],
  },
  {
    key: 'expert-alumni',
    title: '科技专家校友关系',
    endpoint: '/api/v1/kg-service/expert-alumni-relation',
    method: 'POST',
    requestFields: [
      { name: 'expert_id', type: 'string', required: true, description: '专家唯一标识' },
      { name: 'school', type: 'string', required: false, description: '院校筛选条件' },
      { name: 'education_stage', type: 'string', required: false, description: '教育阶段筛选' },
      { name: 'major', type: 'string', required: false, description: '专业或院系筛选' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', school: '北京大学', education_stage: '博士', major: '计算机科学' },
    responseExample: { data: { alumni: 26, dimensions: ['同校', '同院系', '同导师'], interactions: 9 } },
    resultRows: [{ label: '校友数量', value: '26' }, { label: '关系维度', value: '3' }, { label: '学术互动', value: '9' }, { label: '最高置信度', value: '0.89' }],
    evidence: ['基于教育经历匹配校友关系。', '细分同校、同院系、同导师等关联维度。', '关联后续学术交流与合作互动。'],
  },
  {
    key: 'paper-cooperation',
    title: '科技专家论文合作关系',
    endpoint: '/api/v1/kg-service/paper-cooperation-relation',
    method: 'POST',
    requestFields: [
      { name: 'expert_id', type: 'string', required: true, description: '专家唯一标识' },
      { name: 'coauthor_id', type: 'string', required: false, description: '合作者唯一标识' },
      { name: 'topic', type: 'string', required: false, description: '论文主题筛选' },
      { name: 'venue_level', type: 'string', required: false, description: '期刊或会议级别' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', coauthor_id: 'E10002', topic: '人工智能', venue_level: 'A类会议' },
    responseExample: { data: { papers: 14, citations: 1260, stable_team: true, topics: ['人工智能', '先进计算'] } },
    resultRows: [{ label: '合作论文', value: '14' }, { label: '总被引', value: '1260' }, { label: '研究方向', value: '5' }, { label: '核心人员', value: '7' }],
    evidence: ['提取作者列表、作者单位、发表时间和论文主题。', '统计期刊会议级别和被引情况。', '识别长期稳定合作团队和核心合作人员。'],
  },
  {
    key: 'enterprise-relation',
    title: '重点关注科技企业关系',
    endpoint: '/api/v1/kg-service/key-enterprise-relation',
    method: 'POST',
    requestFields: [
      { name: 'expert_id', type: 'string', required: true, description: '专家唯一标识' },
      { name: 'enterprise_name', type: 'string', required: false, description: '企业名称筛选' },
      { name: 'role_type', type: 'string', required: false, description: '专家企业角色' },
      { name: 'industry', type: 'string', required: false, description: '企业行业方向' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', enterprise_name: '华南智能芯片', role_type: '顾问/股东/合作方', industry: '集成电路' },
    responseExample: { data: { enterprises: 9, roles: 4, cooperation_fields: ['芯片设计', '智能制造'] } },
    resultRows: [{ label: '关联企业', value: '9' }, { label: '角色类型', value: '4' }, { label: '合作领域', value: '6' }, { label: '经营风险', value: '2' }],
    evidence: ['标注专家在企业中的角色、合作领域、合作时间和模式。', '关联企业行业地位、技术方向与经营状况。', '支持产业界资源对接分析。'],
  },
  {
    key: 'industry-chain-event',
    title: '科技产业链点TOP-N事件关系',
    endpoint: '/api/v1/kg-service/industry-node-top-events',
    method: 'POST',
    requestFields: [
      { name: 'chain_node_id', type: 'string', required: true, description: '产业链节点标识' },
      { name: 'top_n', type: 'number', required: false, description: '返回事件数量' },
      { name: 'event_type', type: 'string', required: false, description: '事件类型筛选' },
      { name: 'time_range', type: 'string', required: false, description: '事件时间范围' },
    ],
    responseFields: commonResponseFields,
    requestExample: { chain_node_id: 'IC-CHIP-DESIGN', top_n: 10, event_type: '投融资/政策/风险', time_range: '2025-2026' },
    responseExample: { data: { events: 10, experts: 18, enterprises: 24, risk_level: '中' } },
    resultRows: [{ label: 'TOP事件', value: '10' }, { label: '关联专家', value: '18' }, { label: '关联企业', value: '24' }, { label: '风险等级', value: '中' }],
    evidence: ['按影响力评估筛选产业链节点 TOP-N 事件。', '构建事件与专家、企业、人才的关联关系。', '分析产业链影响和后续发展趋势。'],
  },
  {
    key: 'industry-chain-panorama',
    title: '科技产业链全景图',
    endpoint: '/api/v1/kg-service/industry-chain-panorama',
    method: 'POST',
    requestFields: [
      { name: 'chain_id', type: 'string', required: true, description: '产业链标识' },
      { name: 'layer_depth', type: 'number', required: false, description: '层级展开深度' },
      { name: 'relation_filter', type: 'array', required: false, description: '关系筛选条件' },
      { name: 'include_events', type: 'boolean', required: false, description: '是否包含事件' },
    ],
    responseFields: commonResponseFields,
    requestExample: { chain_id: 'AI-COMPUTING', layer_depth: 3, relation_filter: ['技术', '企业', '专家'], include_events: true },
    responseExample: { data: { nodes: 186, relations: 420, key_technologies: 22, key_enterprises: 48 } },
    resultRows: [{ label: '产业节点', value: '186' }, { label: '链路关系', value: '420' }, { label: '关键技术', value: '22' }, { label: '重点企业', value: '48' }],
    evidence: ['整合产业链实体、关系、事件数据。', '展示核心节点、关联关系和数据流向。', '支持层级展开、关系筛选和动态更新。'],
  },
]

const props = defineProps<{
  initialTab?: PlatformTab
}>()

const activeTab = ref<PlatformTab>(props.initialTab ?? 'overview')
const activeServiceKey = ref(modules[0]?.key ?? '')
const activeBuildTab = ref<'entity' | 'relation' | 'property' | 'rule'>('entity')
const activeServiceMode = ref<'test' | 'api'>('test')
const selectedQueryType = ref('科技专家')

const activeService = computed(() => modules.find((item) => item.key === activeServiceKey.value) ?? modules[0])
const activeRequestJson = computed(() => JSON.stringify(activeService.value.requestExample, null, 2))
const activeResponseJson = computed(() => JSON.stringify({
  code: 0,
  message: 'success',
  data: activeService.value.responseExample.data ?? activeService.value.responseExample,
}, null, 2))

watch(
  () => props.initialTab,
  (tab) => {
    if (tab) {
      activeTab.value = tab
    }
  },
)

const metrics = [
  { label: '实体总量', value: '1.28 亿', trend: '+18,426 今日新增', tone: 'blue' },
  { label: '关系总量', value: '6.42 亿', trend: '+92,318 今日新增', tone: 'green' },
  { label: '接入数据源', value: '42', trend: '论文/项目/企业/机构/事件', tone: 'purple' },
  { label: '待人工审核', value: '326', trend: '低置信度与冲突数据', tone: 'orange' },
]

const serviceTrend = [
  { label: '直接关系', value: 72 },
  { label: '间接关系', value: 48 },
  { label: '合作成果', value: 64 },
  { label: '同事校友', value: 56 },
  { label: '企业关联', value: 82 },
  { label: '产业事件', value: 68 },
]

const sourceHealth = [
  { name: '论文库', status: '正常', sync: '2 分钟前', rate: '99.2%' },
  { name: '专家人才库', status: '正常', sync: '8 分钟前', rate: '98.7%' },
  { name: '企业工商库', status: '告警', sync: '18 分钟前', rate: '91.4%' },
  { name: '产业事件库', status: '正常', sync: '5 分钟前', rate: '96.8%' },
]

const qualityRows = [
  { label: '实体消歧通过率', value: '92.6%', width: 92 },
  { label: '关系验证通过率', value: '88.4%', width: 88 },
  { label: '属性更新一致率', value: '94.1%', width: 94 },
  { label: '规则命中覆盖率', value: '86.9%', width: 87 },
]

const qualityGates = [
  { label: '自动入库', value: '7,604', desc: '置信度 >= 0.85' },
  { label: '人工审核', value: '326', desc: '低置信度或冲突数据' },
  { label: '规则回写', value: '42', desc: '审核结果沉淀为规则样本' },
]

const pipeline = [
  { name: '数据接入', desc: '读取论文、项目、成果、企业、机构、事件等多源数据', count: '12,438 条', status: '完成' },
  { name: '清洗标准化', desc: '字段格式统一、缺失校验、别名规范和时间归一', count: '11,982 条', status: '完成' },
  { name: '实体关系抽取', desc: '规则、算法和大模型辅助抽取实体、关系、属性', count: '8,942 条', status: '运行中' },
  { name: '比对消歧', desc: '与存量图谱比对，判断新增、合并、更新或冲突', count: '1,203 条', status: '运行中' },
  { name: '置信度审核', desc: '高置信度自动入库，低置信度进入人工审核', count: '326 条', status: '待审核' },
  { name: '入库服务调用', desc: '写入图数据库并支撑统一查询和业务服务调用', count: '7,604 条', status: '排队' },
]

const taskRows = [
  { batch: 'KG-INC-20260706-01', source: '论文库增量', stage: '关系抽取', status: '运行中', entities: '3,261', relations: '8,942', conflicts: '41' },
  { batch: 'KG-INC-20260706-02', source: '企业工商库', stage: '属性更新', status: '待审核', entities: '486', relations: '1,280', conflicts: '86' },
  { batch: 'KG-FULL-20260705-08', source: '专家人才库', stage: '图谱入库', status: '完成', entities: '18,420', relations: '62,117', conflicts: '0' },
]

const discoveryRows = [
  { type: '新增实体', count: '3,261', sample: '华南智能芯片有限公司、先进计算实验室', strategy: '无高相似候选时创建新实体，进入实体审核或自动入库' },
  { type: '新增关系', count: '8,942', sample: '论文合作、企业关联、产业事件参与', strategy: '基于规则和证据链校验，低置信度进入人工审核' },
  { type: '新增属性', count: '1,203', sample: '被引次数、论文数量、企业经营状态', strategy: '识别动态属性变化，判断补充、更新、冲突或回滚' },
  { type: '潜在隐藏关系', count: '286', sample: '共同项目间接路径、同导师链路、产业链事件共现', strategy: '路径分析和关系传递推理后进入候选关系池' },
  { type: '冲突数据', count: '326', sample: '实体别名冲突、关系证据不足、属性来源不一致', strategy: '进入人工审核队列，审核结果回写图谱和规则样本' },
]

const entityRows = [
  { name: '张明远', type: '科技专家', match: '张明远 / Zhang Mingyuan', score: '0.92', action: '建议合并' },
  { name: '先进计算实验室', type: '机构团队', match: '先进计算与智能系统实验室', score: '0.87', action: '待人工确认' },
  { name: '华南智能芯片有限公司', type: '科技企业', match: '无高相似候选', score: '0.31', action: '创建新实体' },
]

const relationRows = [
  { source: '张明远', target: '李佳宁', relation: '论文合作', evidence: '共同发表论文 4 篇', confidence: '0.94', status: '自动入库' },
  { source: '张明远', target: '王青', relation: '校友关系', evidence: '同校同院系，时间重叠 2 年', confidence: '0.78', status: '待审核' },
  { source: '李佳宁', target: '湾区智能制造联盟', relation: '产业事件参与', evidence: 'TOP-N 事件报道与项目名单', confidence: '0.71', status: '待审核' },
]

const propertyRows = [
  { object: '张明远', property: '论文数量', oldValue: '128', newValue: '132', rule: '动态属性自动更新' },
  { object: '李佳宁', property: '被引次数', oldValue: '3,421', newValue: '3,568', rule: '超过阈值自动入库' },
  { object: '某科技企业', property: '经营状态', oldValue: '存续', newValue: '注销风险', rule: '冲突数据进入审核' },
]

const ruleRows = [
  { name: '专家姓名别名消歧规则', type: '实体消歧', method: '字段映射 + 相似度算法', threshold: '0.86', status: '启用' },
  { name: '论文作者合作关系抽取', type: '关系抽取', method: '作者列表位置 + 单位校验', threshold: '0.90', status: '启用' },
  { name: '企业关联角色识别', type: '属性/关系识别', method: '正则 + 页面字段定位 + 人工确认', threshold: '0.80', status: '调试中' },
]

const queryTypes = ['科技专家', '科技企业', '论文成果', '机构团队', '产业链节点']
const relationFilters = ['直接关系', '间接关系', '同事', '校友', '论文合作', '企业关联', '产业事件']

const pageMeta = computed(() => {
  const map: Record<PlatformTab, { eyebrow: string; title: string; desc: string; statLabel: string; statValue: string; statHint: string }> = {
    overview: {
      eyebrow: '平台运行总览',
      title: '亿级科技知识图谱平台',
      desc: '统一呈现数据接入、图谱构建、质量治理、增量更新和业务服务运行状态。',
      statLabel: '今日增量任务',
      statValue: '18',
      statHint: '高置信度自动入库率 87.6%',
    },
    processing: {
      eyebrow: '数据处理中心',
      title: '数据接入与处理任务',
      desc: '配置数据源、处理规则和入库阈值，跟踪清洗、抽取、消歧、审核和入库执行过程。',
      statLabel: '待处理批次',
      statValue: '7',
      statHint: '326 条数据进入人工审核',
    },
    construction: {
      eyebrow: '图谱构建中心',
      title: '实体、关系、属性与规则管理',
      desc: '支持实体关系抽取、人工新增编辑、冲突处理、规则维护和图数据库增量写入。',
      statLabel: '本次入库影响',
      statValue: '13,406',
      statHint: '实体、关系和属性更新合计',
    },
    query: {
      eyebrow: '图谱查询中心',
      title: '核心子图查询与证据追溯',
      desc: '先输入查询条件，再返回核心实体网络、关键关系、结构化结果和证据链。',
      statLabel: '当前命中关系',
      statValue: '9',
      statHint: '最高置信度 0.94',
    },
    service: {
      eyebrow: '业务服务中心',
      title: '9 大业务服务统一调用',
      desc: '通过统一参数配置和服务出口调用底层图谱能力，输出图谱结果、结构化结果和证据链。',
      statLabel: '服务模块',
      statValue: '9',
      statHint: '统一窗口调用',
    },
  }
  return map[activeTab.value]
})

</script>

<template>
  <div class="platform-page">
    <header v-if="activeTab === 'overview'" class="platform-hero">
      <div>
        <p>{{ pageMeta.eyebrow }}</p>
        <h1>{{ pageMeta.title }}</h1>
        <span>{{ pageMeta.desc }}</span>
      </div>
      <div class="platform-hero__actions">
        <button type="button">新建任务</button>
        <button type="button">导出报告</button>
      </div>
      <div class="platform-hero__status">
        <strong>{{ pageMeta.statLabel }}</strong>
        <b>{{ pageMeta.statValue }}</b>
        <span>{{ pageMeta.statHint }}</span>
      </div>
    </header>

    <header v-else class="platform-page-head">
      <div>
        <p>{{ pageMeta.eyebrow }}</p>
        <h1>{{ pageMeta.title }}</h1>
      </div>
      <span>{{ pageMeta.desc }}</span>
    </header>

    <main v-if="activeTab === 'overview'" class="platform-content platform-overview">
      <section class="platform-metrics" aria-label="平台指标">
        <article v-for="item in metrics" :key="item.label" :class="['platform-metric', `is-${item.tone}`]">
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
          <em>{{ item.trend }}</em>
        </article>
      </section>

      <section class="kg-panel platform-pipeline-panel">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">数据到图谱处理闭环</h2>
          <span>建图 / 管图 / 更新图 / 查图 / 用图</span>
        </div>
        <div class="platform-pipeline">
          <article v-for="item in pipeline" :key="item.name" class="platform-pipeline__step">
            <div>
              <strong>{{ item.name }}</strong>
              <span>{{ item.status }}</span>
            </div>
            <p>{{ item.desc }}</p>
            <em>{{ item.count }}</em>
          </article>
        </div>
      </section>

      <section class="kg-panel">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">最近任务执行状态</h2>
          <button class="kg-button kg-button--secondary" type="button">查看任务</button>
        </div>
        <table class="platform-table">
          <thead>
            <tr>
              <th>任务批次</th>
              <th>数据源</th>
              <th>当前阶段</th>
              <th>状态</th>
              <th>实体</th>
              <th>关系</th>
              <th>冲突</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in taskRows" :key="row.batch">
              <td>{{ row.batch }}</td>
              <td>{{ row.source }}</td>
              <td>{{ row.stage }}</td>
              <td><span class="platform-status">{{ row.status }}</span></td>
              <td>{{ row.entities }}</td>
              <td>{{ row.relations }}</td>
              <td>{{ row.conflicts }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="platform-overview-grid">
        <div class="kg-panel platform-trend">
          <div class="kg-panel__header">
            <h2 class="kg-panel__title">业务服务调用趋势</h2>
            <span>近 24 小时</span>
          </div>
          <div class="platform-trend__bars">
            <div v-for="item in serviceTrend" :key="item.label">
              <span>{{ item.label }}</span>
              <i><b :style="{ height: `${item.value}%` }"></b></i>
              <em>{{ item.value }}%</em>
            </div>
          </div>
        </div>

        <div class="kg-panel platform-health">
          <div class="kg-panel__header">
            <h2 class="kg-panel__title">数据源健康状态</h2>
            <span>实时同步</span>
          </div>
          <div class="platform-health__list">
            <article v-for="item in sourceHealth" :key="item.name" :class="{ 'is-warning': item.status === '告警' }">
              <strong>{{ item.name }}</strong>
              <span>{{ item.status }}</span>
              <em>{{ item.sync }}</em>
              <b>{{ item.rate }}</b>
            </article>
          </div>
        </div>

        <div class="kg-panel platform-quality">
          <div class="kg-panel__header">
            <h2 class="kg-panel__title">图谱质量治理</h2>
            <span>质量闸口</span>
          </div>
          <div class="platform-quality__list">
            <article v-for="row in qualityRows" :key="row.label">
              <div><span>{{ row.label }}</span><strong>{{ row.value }}</strong></div>
              <i><b :style="{ width: `${row.width}%` }"></b></i>
            </article>
          </div>
        </div>
      </section>
    </main>

    <main v-else-if="activeTab === 'processing'" class="platform-content platform-processing">
      <section class="kg-panel platform-config">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">处理任务配置</h2>
          <button class="kg-button" type="button">启动任务</button>
        </div>
        <div class="platform-form-grid">
          <label>
            <span>数据源</span>
            <select>
              <option>论文库增量数据</option>
              <option>专家人才库</option>
              <option>科技企业库</option>
              <option>产业链事件库</option>
            </select>
          </label>
          <label>
            <span>处理方式</span>
            <select>
              <option>增量处理</option>
              <option>全量重建</option>
            </select>
          </label>
          <label>
            <span>抽取对象</span>
            <select>
              <option>实体 + 关系 + 属性</option>
              <option>仅实体</option>
              <option>仅关系</option>
            </select>
          </label>
          <label>
            <span>自动入库阈值</span>
            <input value="0.85" />
          </label>
        </div>
      </section>

      <section class="kg-panel platform-discovery">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">增量发现结果</h2>
          <span>新增实体 / 新增关系 / 新增属性 / 潜在隐藏关系 / 冲突数据</span>
        </div>
        <div class="platform-discovery__grid">
          <article v-for="row in discoveryRows" :key="row.type">
            <div>
              <span>{{ row.type }}</span>
              <strong>{{ row.count }}</strong>
            </div>
            <p>{{ row.sample }}</p>
            <em>{{ row.strategy }}</em>
          </article>
        </div>
      </section>

      <section class="kg-panel platform-gates">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">质量闸口与流转策略</h2>
          <span>自动处理与人工协同</span>
        </div>
        <div class="platform-gates__grid">
          <article v-for="gate in qualityGates" :key="gate.label">
            <span>{{ gate.label }}</span>
            <strong>{{ gate.value }}</strong>
            <p>{{ gate.desc }}</p>
          </article>
        </div>
      </section>

      <section class="kg-panel platform-processing-flow">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">执行过程追踪</h2>
          <span>机器初筛 + 人工审核 + 规则沉淀</span>
        </div>
        <div class="platform-timeline">
          <article v-for="item in pipeline" :key="item.name">
            <i></i>
            <div>
              <strong>{{ item.name }}</strong>
              <p>{{ item.desc }}</p>
            </div>
            <span>{{ item.count }}</span>
          </article>
        </div>
      </section>

      <aside class="kg-panel platform-review">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">人工审核队列</h2>
          <span>326 条</span>
        </div>
        <div class="platform-review__body">
          <article>
            <strong>实体重复疑似冲突</strong>
            <p>“张明远”与“Zhang Mingyuan”匹配度 0.82，低于自动合并阈值。</p>
            <div><button>确认合并</button><button>保留新实体</button></div>
          </article>
          <article>
            <strong>关系证据不足</strong>
            <p>企业合作关系仅来自单一网页，需要人工确认角色和时间。</p>
            <div><button>通过</button><button>退回规则</button></div>
          </article>
        </div>
      </aside>
    </main>

    <main v-else-if="activeTab === 'construction'" class="platform-content platform-construction">
      <section class="kg-panel platform-build">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">图谱构建与治理</h2>
          <div class="platform-segmented">
            <button type="button" :class="{ 'is-active': activeBuildTab === 'entity' }" @click="activeBuildTab = 'entity'">实体</button>
            <button type="button" :class="{ 'is-active': activeBuildTab === 'relation' }" @click="activeBuildTab = 'relation'">关系</button>
            <button type="button" :class="{ 'is-active': activeBuildTab === 'property' }" @click="activeBuildTab = 'property'">属性</button>
            <button type="button" :class="{ 'is-active': activeBuildTab === 'rule' }" @click="activeBuildTab = 'rule'">规则</button>
          </div>
        </div>

        <div class="platform-manual-toolbar">
          <button type="button">新增实体</button>
          <button type="button">新增关系</button>
          <button type="button">新增属性</button>
          <button type="button">批量审核</button>
          <button type="button">导入规则</button>
          <span>支持查询、新增、编辑、删除、合并、驳回、回滚，并将人工结果回写图谱。</span>
        </div>

        <div class="platform-manage-filter">
          <label>
            <span>对象检索</span>
            <input value="张明远 / 华南智能芯片" />
          </label>
          <label>
            <span>数据状态</span>
            <select>
              <option>全部状态</option>
              <option>待审核</option>
              <option>自动入库</option>
              <option>冲突数据</option>
            </select>
          </label>
          <label>
            <span>来源批次</span>
            <select>
              <option>KG-INC-20260706-01</option>
              <option>KG-INC-20260706-02</option>
            </select>
          </label>
          <button type="button">查询</button>
        </div>

        <table v-if="activeBuildTab === 'entity'" class="platform-table">
          <thead><tr><th>新识别实体</th><th>类型</th><th>候选匹配</th><th>相似度</th><th>建议操作</th><th>人工操作</th></tr></thead>
          <tbody>
            <tr v-for="row in entityRows" :key="row.name">
              <td>{{ row.name }}</td><td>{{ row.type }}</td><td>{{ row.match }}</td><td>{{ row.score }}</td><td>{{ row.action }}</td>
              <td>
                <div class="platform-row-actions">
                  <button>查看</button><button>编辑</button><button>合并</button><button>删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="activeBuildTab === 'relation'" class="platform-table">
          <thead><tr><th>源实体</th><th>目标实体</th><th>关系类型</th><th>证据</th><th>置信度</th><th>状态</th><th>人工操作</th></tr></thead>
          <tbody>
            <tr v-for="row in relationRows" :key="`${row.source}-${row.target}-${row.relation}`">
              <td>{{ row.source }}</td><td>{{ row.target }}</td><td>{{ row.relation }}</td><td>{{ row.evidence }}</td><td>{{ row.confidence }}</td><td>{{ row.status }}</td>
              <td>
                <div class="platform-row-actions">
                  <button>查看</button><button>编辑</button><button>审核</button><button>删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else-if="activeBuildTab === 'property'" class="platform-table">
          <thead><tr><th>对象</th><th>动态属性</th><th>原值</th><th>新值</th><th>处理规则</th><th>人工操作</th></tr></thead>
          <tbody>
            <tr v-for="row in propertyRows" :key="`${row.object}-${row.property}`">
              <td>{{ row.object }}</td><td>{{ row.property }}</td><td>{{ row.oldValue }}</td><td>{{ row.newValue }}</td><td>{{ row.rule }}</td>
              <td>
                <div class="platform-row-actions">
                  <button>查看</button><button>编辑</button><button>回滚</button><button>删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <table v-else class="platform-table">
          <thead><tr><th>规则名称</th><th>规则类型</th><th>配置方式</th><th>阈值</th><th>状态</th><th>操作</th></tr></thead>
          <tbody>
            <tr v-for="row in ruleRows" :key="row.name">
              <td>{{ row.name }}</td><td>{{ row.type }}</td><td>{{ row.method }}</td><td>{{ row.threshold }}</td><td>{{ row.status }}</td>
              <td>
                <div class="platform-row-actions">
                  <button>查看</button><button>编辑</button><button>停用</button><button>删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="platform-build-footer">
          <span>当前视图共 3 条记录</span>
          <span>最近同步：2026-07-06 10:30</span>
          <span>审核策略：自动入库 + 人工确认</span>
        </div>
      </section>

      <aside class="kg-panel platform-graph-summary">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">本次入库影响</h2>
        </div>
        <div class="platform-impact">
          <div><span>新增实体</span><strong>3,261</strong></div>
          <div><span>新增关系</span><strong>8,942</strong></div>
          <div><span>属性更新</span><strong>1,203</strong></div>
          <div><span>冲突待审</span><strong>326</strong></div>
        </div>
        <div class="platform-rule-note">
          <strong>规则沉淀</strong>
          <p>人工审核结果会回写为消歧样本、关系验证样本和阈值调整依据，支撑后续增量处理。</p>
        </div>
        <div class="platform-rule-note platform-rule-note--manual">
          <strong>人工维护策略</strong>
          <p>管理员可手动新增实体、关系和属性；对错误抽取结果执行删除、驳回或回滚；对冲突数据进行合并、拆分和来源标注。</p>
        </div>
        <div class="platform-governance-flow">
          <strong>治理流转</strong>
          <ol>
            <li><span>01</span><p>机器抽取候选实体、关系和属性</p></li>
            <li><span>02</span><p>图谱比对完成消歧、合并和冲突识别</p></li>
            <li><span>03</span><p>高置信度自动入库，异常数据进入审核</p></li>
            <li><span>04</span><p>审核结果回写图谱并沉淀为规则样本</p></li>
          </ol>
        </div>
      </aside>
    </main>

    <main v-else-if="activeTab === 'query'" class="platform-content platform-query">
      <section class="kg-panel platform-query-form">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">统一图查询入口</h2>
          <button class="kg-button" type="button">查询</button>
        </div>
        <div class="platform-form-grid">
          <label>
            <span>查询对象</span>
            <select v-model="selectedQueryType">
              <option v-for="item in queryTypes" :key="item">{{ item }}</option>
            </select>
          </label>
          <label>
            <span>关键词</span>
            <input value="张明远" />
          </label>
          <label>
            <span>关系类型</span>
            <select>
              <option v-for="item in relationFilters" :key="item">{{ item }}</option>
            </select>
          </label>
          <label>
            <span>置信度</span>
            <input value=">= 0.75" />
          </label>
        </div>
      </section>

      <section class="kg-panel platform-query-graph">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">核心子图展示</h2>
          <span>{{ selectedQueryType }} / 关键关系优先</span>
        </div>
        <svg class="kg-graph-canvas platform-svg" viewBox="0 0 760 430" role="img" aria-label="图谱查询结果">
          <defs>
            <marker id="platform-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
              <path d="M0,0 L7,3.5 L0,7 Z" fill="#aab4c3" />
            </marker>
          </defs>
          <g class="platform-network-lines">
            <line x1="382" y1="214" x2="188" y2="112" />
            <line x1="382" y1="214" x2="570" y2="102" />
            <line x1="382" y1="214" x2="182" y2="318" />
            <line x1="382" y1="214" x2="592" y2="316" />
            <line x1="188" y1="112" x2="116" y2="192" />
            <line x1="188" y1="112" x2="284" y2="92" />
            <line x1="570" y1="102" x2="650" y2="178" />
            <line x1="570" y1="102" x2="458" y2="74" />
            <line x1="182" y1="318" x2="104" y2="258" />
            <line x1="182" y1="318" x2="302" y2="344" />
            <line x1="592" y1="316" x2="686" y2="254" />
            <line x1="592" y1="316" x2="498" y2="360" />
            <line x1="302" y1="344" x2="498" y2="360" />
            <line x1="284" y1="92" x2="458" y2="74" />
          </g>
          <line class="platform-network-line is-primary" x1="382" y1="214" x2="188" y2="112" />
          <line class="platform-network-line is-green" x1="382" y1="214" x2="570" y2="102" />
          <line class="platform-network-line is-orange" x1="382" y1="214" x2="182" y2="318" />
          <line class="platform-network-line is-purple" x1="382" y1="214" x2="592" y2="316" />
          <text class="platform-edge-label" x="278" y="150">论文合作</text>
          <text class="platform-edge-label" x="484" y="152">同事关系</text>
          <text class="platform-edge-label" x="276" y="280">企业关联</text>
          <text class="platform-edge-label" x="500" y="282">成果证据</text>
          <g class="platform-node platform-node--main" transform="translate(382 214)">
            <circle r="34" /><text>张明远</text>
          </g>
          <g class="platform-node is-expert" transform="translate(188 112)"><circle r="28" /><text>李佳宁</text></g>
          <g class="platform-node is-org" transform="translate(570 102)"><circle r="28" /><text>清华大学</text></g>
          <g class="platform-node is-company" transform="translate(182 318)"><circle r="30" /><text>华南智能芯片</text></g>
          <g class="platform-node is-paper" transform="translate(592 316)"><circle r="30" /><text>先进计算论文</text></g>
          <g class="platform-node is-topic" transform="translate(116 192)"><circle r="20" /><text>生物医药</text></g>
          <g class="platform-node is-project" transform="translate(284 92)"><circle r="18" /><text>项目18</text></g>
          <g class="platform-node is-topic" transform="translate(650 178)"><circle r="20" /><text>人工智能</text></g>
          <g class="platform-node is-paper" transform="translate(458 74)"><circle r="18" /><text>论文006</text></g>
          <g class="platform-node is-project" transform="translate(104 258)"><circle r="18" /><text>技术31</text></g>
          <g class="platform-node is-company" transform="translate(302 344)"><circle r="20" /><text>腾讯</text></g>
          <g class="platform-node is-topic" transform="translate(686 254)"><circle r="18" /><text>新能源</text></g>
          <g class="platform-node is-project" transform="translate(498 360)"><circle r="18" /><text>项目03</text></g>
        </svg>
      </section>

      <aside class="kg-panel platform-detail">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">结构化结果与证据链</h2>
        </div>
        <div class="platform-detail__body">
          <dl>
            <div><dt>核心实体</dt><dd>张明远 / 科技专家</dd></div>
            <div><dt>命中关系</dt><dd>论文合作 4、同事 3、企业关联 2</dd></div>
            <div><dt>最高置信度</dt><dd>0.94</dd></div>
            <div><dt>最近更新</dt><dd>2026-07-06 10:30</dd></div>
          </dl>
          <ul>
            <li>共同发表论文 4 篇，作者列表和单位信息一致。</li>
            <li>任职时间存在重叠，机构层级匹配到同一实验室。</li>
            <li>企业合作关系来自项目公告和工商角色数据。</li>
          </ul>
        </div>
      </aside>
    </main>

    <main v-else :class="['platform-content', 'platform-service', { 'platform-service--api': activeServiceMode === 'api' }]">
      <section class="kg-panel platform-service-console">
        <div class="platform-service-console__top">
          <div class="platform-service-tabs">
            <button type="button" :class="{ 'is-active': activeServiceMode === 'test' }" @click="activeServiceMode = 'test'">
              服务调用
            </button>
            <button type="button" :class="{ 'is-active': activeServiceMode === 'api' }" @click="activeServiceMode = 'api'">
              接口文档
            </button>
          </div>
        </div>

        <div class="platform-service-console__body">
          <label>
            <span>业务服务</span>
            <select v-model="activeServiceKey">
              <option v-for="item in modules" :key="item.key" :value="item.key">{{ item.title }}</option>
            </select>
          </label>
          <template v-if="activeServiceMode === 'test'">
            <label v-for="field in activeService.requestFields.slice(0, 3)" :key="field.name">
              <span>{{ field.description }}</span>
              <input :value="activeService.requestExample[field.name] ?? ''" />
            </label>
          </template>
          <template v-else>
            <label>
            <span>接口路径</span>
            <input :value="activeService.endpoint" readonly />
            </label>
            <label>
            <span>请求方法</span>
            <input :value="activeService.method" readonly />
            </label>
          </template>
          <div class="platform-service-console__actions">
            <button v-if="activeServiceMode === 'test'" type="button">执行调用</button>
            <button v-else type="button">复制接口</button>
          </div>
        </div>
      </section>

      <template v-if="activeServiceMode === 'test'">
        <section class="kg-panel platform-service-graph">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">图谱结果</h2>
          <span>{{ activeService.title }}</span>
        </div>
        <svg class="kg-graph-canvas platform-svg" viewBox="0 0 760 430" role="img" aria-label="业务服务图谱">
          <defs>
            <marker id="service-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
              <path d="M0,0 L7,3.5 L0,7 Z" fill="#aab4c3" />
            </marker>
          </defs>
          <g class="platform-network-lines platform-network-lines--service">
            <line x1="382" y1="214" x2="180" y2="118" />
            <line x1="382" y1="214" x2="578" y2="118" />
            <line x1="382" y1="214" x2="194" y2="316" />
            <line x1="382" y1="214" x2="586" y2="316" />
            <line x1="180" y1="118" x2="96" y2="208" />
            <line x1="180" y1="118" x2="286" y2="84" />
            <line x1="578" y1="118" x2="674" y2="190" />
            <line x1="578" y1="118" x2="476" y2="76" />
            <line x1="194" y1="316" x2="312" y2="356" />
            <line x1="586" y1="316" x2="684" y2="270" />
            <line x1="312" y1="356" x2="506" y2="356" />
            <line x1="286" y1="84" x2="476" y2="76" />
          </g>
          <line class="platform-network-line is-primary" x1="382" y1="214" x2="180" y2="118" />
          <line class="platform-network-line is-green" x1="382" y1="214" x2="578" y2="118" />
          <line class="platform-network-line is-orange" x1="382" y1="214" x2="194" y2="316" />
          <line class="platform-network-line is-purple" x1="382" y1="214" x2="586" y2="316" />
          <text class="platform-edge-label" x="274" y="150">直接关系</text>
          <text class="platform-edge-label" x="490" y="152">机构关联</text>
          <text class="platform-edge-label" x="282" y="282">合作成果</text>
          <text class="platform-edge-label" x="500" y="282">事件关联</text>
          <g class="platform-node platform-node--main" transform="translate(382 214)"><circle r="34" /><text>张明远</text></g>
          <g class="platform-node is-expert" transform="translate(180 118)"><circle r="28" /><text>李佳宁</text></g>
          <g class="platform-node is-org" transform="translate(578 118)"><circle r="28" /><text>清华大学</text></g>
          <g class="platform-node is-paper" transform="translate(194 316)"><circle r="30" /><text>论文成果</text></g>
          <g class="platform-node is-topic" transform="translate(586 316)"><circle r="30" /><text>产业事件</text></g>
          <g class="platform-node is-company" transform="translate(96 208)"><circle r="20" /><text>科技企业</text></g>
          <g class="platform-node is-project" transform="translate(286 84)"><circle r="18" /><text>项目18</text></g>
          <g class="platform-node is-topic" transform="translate(674 190)"><circle r="20" /><text>人工智能</text></g>
          <g class="platform-node is-paper" transform="translate(476 76)"><circle r="18" /><text>论文006</text></g>
          <g class="platform-node is-company" transform="translate(312 356)"><circle r="20" /><text>腾讯</text></g>
          <g class="platform-node is-project" transform="translate(684 270)"><circle r="18" /><text>技术31</text></g>
          <g class="platform-node is-topic" transform="translate(506 356)"><circle r="18" /><text>新能源</text></g>
        </svg>
        </section>

        <aside class="kg-panel platform-service-result">
          <div class="kg-panel__header">
            <h2 class="kg-panel__title">结构化结果</h2>
          </div>
          <div class="platform-result-grid">
            <div v-for="row in activeService.resultRows" :key="row.label">
              <span>{{ row.label }}</span>
              <strong>{{ row.value }}</strong>
            </div>
          </div>
          <div class="platform-evidence">
            <strong>证据链</strong>
            <ul>
              <li v-for="item in activeService.evidence" :key="item">{{ item }}</li>
            </ul>
          </div>
          <div class="platform-service-info">
            <strong>返回具体信息</strong>
            <dl>
              <div><dt>核心对象</dt><dd>张明远 / 科技专家</dd></div>
              <div><dt>命中服务</dt><dd>{{ activeService.title }}</dd></div>
              <div><dt>置信度</dt><dd>0.94</dd></div>
              <div><dt>更新时间</dt><dd>2026-07-06 10:30</dd></div>
            </dl>
          </div>
        </aside>
      </template>

      <template v-else>
        <section class="kg-panel platform-api-doc">
          <div class="kg-panel__header">
            <h2 class="kg-panel__title">开发者接口文档</h2>
            <span>{{ activeService.method }} {{ activeService.endpoint }}</span>
          </div>
          <div class="platform-api-doc__grid">
            <article>
              <h3>请求参数</h3>
              <table class="platform-table">
                <thead><tr><th>字段名</th><th>类型</th><th>必填</th><th>说明</th></tr></thead>
                <tbody>
                  <tr v-for="field in activeService.requestFields.slice(0, 6)" :key="field.name">
                    <td>{{ field.name }}</td>
                    <td>{{ field.type }}</td>
                    <td>{{ field.required ?? '否' }}</td>
                    <td>{{ field.description }}</td>
                  </tr>
                </tbody>
              </table>
            </article>
            <article>
              <h3>返回字段</h3>
              <table class="platform-table">
                <thead><tr><th>字段名</th><th>类型</th><th>说明</th></tr></thead>
                <tbody>
                  <tr v-for="field in activeService.responseFields" :key="field.name">
                    <td>{{ field.name }}</td>
                    <td>{{ field.type }}</td>
                    <td>{{ field.description }}</td>
                  </tr>
                </tbody>
              </table>
            </article>
          </div>
          <div class="platform-api-examples">
            <article>
              <h3>请求示例</h3>
              <pre>{{ activeRequestJson }}</pre>
            </article>
            <article>
              <h3>响应示例</h3>
              <pre>{{ activeResponseJson }}</pre>
            </article>
          </div>
          <div class="platform-code-sample">
            <div>
              <strong>代码示例</strong>
              <span>Python</span>
              <span>Node.js</span>
              <span>cURL</span>
            </div>
            <pre>import requests

url = "https://api.example.com{{ activeService.endpoint }}"
payload = {{ activeRequestJson }}
response = requests.post(url, json=payload)
print(response.json())</pre>
          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<style scoped>
.platform-page {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  gap: 16px;
  height: 100%;
  min-width: 0;
  color: var(--text-primary);
}

.platform-hero {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  min-height: 98px;
  padding: 20px 24px;
  border: 1px solid rgba(132, 178, 246, 0.86);
  border-radius: 12px;
  background:
    linear-gradient(135deg, rgba(216, 235, 255, 0.98) 0%, rgba(237, 247, 255, 0.98) 48%, rgba(211, 242, 255, 0.94) 100%),
    #e5f1ff;
  box-shadow:
    0 16px 34px rgba(48, 105, 194, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.96);
}

.platform-hero::before {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(22, 93, 255, 0.075) 1px, transparent 1px),
    linear-gradient(rgba(22, 93, 255, 0.075) 1px, transparent 1px);
  background-size: 34px 34px;
  mask-image: linear-gradient(90deg, rgba(0, 0, 0, 0.62), transparent 72%);
  pointer-events: none;
  content: "";
}

.platform-hero > * {
  position: relative;
}

.platform-hero p,
.platform-hero h1,
.platform-hero span {
  margin: 0;
}

.platform-hero p {
  color: #165dff;
  font-size: 13px;
  font-weight: 600;
}

.platform-hero h1 {
  margin-top: 4px;
  color: #10264c;
  font-size: 28px;
  line-height: 38px;
  font-weight: 600;
}

.platform-hero span {
  display: block;
  margin-top: 4px;
  color: #526987;
  font-size: 13px;
  line-height: 20px;
}

.platform-hero__status {
  flex: 0 0 180px;
  display: grid;
  gap: 2px;
  padding: 10px 14px;
  border-left: 1px solid rgba(103, 160, 242, 0.62);
  border-radius: 0;
  background: transparent;
}

.platform-hero__actions {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.platform-hero__actions button {
  height: 32px;
  padding: 0 12px;
  border: 1px solid #bdd7ff;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.86);
  color: #165dff;
  font-size: 13px;
  cursor: pointer;
}

.platform-hero__actions button:first-child {
  border-color: transparent;
  background: linear-gradient(135deg, #165dff, #0ea5e9);
  color: #fff;
  box-shadow: 0 8px 18px rgba(22, 93, 255, 0.22);
}

.platform-hero__status strong,
.platform-hero__status span {
  color: #526987;
  font-size: 13px;
}

.platform-hero__status b {
  color: #165dff;
  font-size: 32px;
  line-height: 38px;
}

.platform-page-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 18px;
  min-height: 36px;
  padding: 0 2px 2px;
}

.platform-page-head p,
.platform-page-head h1,
.platform-page-head span {
  margin: 0;
}

.platform-page-head p {
  color: #165dff;
  font-size: 12px;
  line-height: 18px;
  font-weight: 600;
}

.platform-page-head h1 {
  color: #10264c;
  font-size: 20px;
  line-height: 28px;
  font-weight: 600;
}

.platform-page-head > span {
  max-width: 720px;
  overflow: hidden;
  color: #526987;
  font-size: 12px;
  line-height: 18px;
  text-align: right;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-content {
  min-height: 0;
  overflow: auto;
  padding-bottom: 2px;
}

.platform-overview {
  display: grid;
  grid-template-rows: auto auto auto minmax(0, 1fr);
  gap: 12px;
}

.platform-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.platform-metric {
  position: relative;
  overflow: hidden;
  display: grid;
  gap: 6px;
  min-height: 92px;
  padding: 14px;
  border: 1px solid #bed8ff;
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(239, 247, 255, 0.94)),
    #f3f8ff;
  box-shadow: 0 8px 18px rgba(48, 105, 194, 0.1);
}

.platform-metric::after {
  position: absolute;
  right: 12px;
  bottom: 10px;
  width: 52px;
  height: 3px;
  border-radius: 999px;
  background: currentColor;
  opacity: 0.18;
  content: "";
}

.platform-metric span,
.platform-metric em {
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  font-style: normal;
  line-height: 20px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-metric strong {
  font-size: 24px;
  line-height: 28px;
}

.platform-metric.is-blue strong { color: #165dff; }
.platform-metric.is-green strong { color: #00a870; }
.platform-metric.is-purple strong { color: #722ed1; }
.platform-metric.is-orange strong { color: #ff7d00; }

.platform-pipeline-panel .kg-panel__header span,
.platform-query-graph .kg-panel__header span,
.platform-service-graph .kg-panel__header span,
.platform-processing-flow .kg-panel__header span {
  color: var(--text-tertiary);
  font-size: 13px;
}

.platform-pipeline {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 10px;
  padding: 14px;
}

.platform-pipeline__step {
  position: relative;
  display: grid;
  align-content: start;
  gap: 8px;
  min-height: 128px;
  padding: 12px;
  border: 1px solid #e0ebfb;
  border-radius: 8px;
  background:
    linear-gradient(180deg, #ffffff, #f8fbff);
}

.platform-pipeline__step:not(:last-child)::after {
  position: absolute;
  top: 50%;
  right: -10px;
  width: 10px;
  height: 1px;
  background: #9bc2ff;
  content: "";
}

.platform-pipeline__step div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.platform-pipeline__step strong {
  font-size: 14px;
}

.platform-pipeline__step div span,
.platform-status {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  padding: 0 8px;
  border-radius: 999px;
  background: var(--primary-subtle);
  color: var(--primary);
  font-size: 12px;
  white-space: nowrap;
}

.platform-pipeline__step p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 18px;
}

.platform-pipeline__step em {
  align-self: end;
  color: var(--text-primary);
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
}

.platform-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.platform-table th,
.platform-table td {
  height: 38px;
  padding: 7px 12px;
  border-bottom: 1px solid var(--border);
  color: var(--text-primary);
  font-size: 13px;
  line-height: 20px;
  text-align: left;
  overflow-wrap: anywhere;
}

.platform-table th {
  background: linear-gradient(180deg, #eef5ff, #f8fbff);
  color: var(--text-secondary);
  font-weight: 600;
}

.platform-table td {
  background: rgba(255, 255, 255, 0.54);
}

.platform-table tbody tr {
  transition: background 0.16s ease;
}

.platform-table tbody tr:hover {
  background: #f8fbff;
}

.platform-build-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  padding: 12px 14px;
  border-top: 1px solid var(--border);
  background:
    linear-gradient(90deg, rgba(22, 93, 255, 0.06), rgba(20, 184, 166, 0.04)),
    #fbfdff;
  color: var(--text-tertiary);
  font-size: 12px;
  line-height: 18px;
}

.platform-processing {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  grid-template-rows: auto auto auto auto;
  gap: 12px;
  padding: 14px;
  border: 1px solid rgba(191, 215, 250, 0.96);
  border-radius: 12px;
  background:
    linear-gradient(180deg, rgba(245, 250, 255, 0.98), rgba(232, 242, 255, 0.86)),
    #eef5ff;
  box-shadow:
    0 14px 30px rgba(48, 105, 194, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.92);
  align-content: start;
}

.platform-processing-flow,
.platform-review {
  display: grid;
  grid-template-rows: auto 1fr;
  align-content: start;
}

.platform-config {
  grid-column: 1 / -1;
}

.platform-discovery {
  grid-column: 1 / -1;
}

.platform-gates {
  grid-column: 1 / -1;
}

.platform-form-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  padding: 12px 14px;
}

.platform-form-grid label {
  display: grid;
  gap: 6px;
  min-width: 0;
}

.platform-form-grid span {
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-form-grid input,
.platform-form-grid select {
  width: 100%;
  height: 32px;
  min-width: 0;
  padding: 0 10px;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: #fff;
  color: var(--text-primary);
}

.platform-timeline {
  display: grid;
  gap: 10px;
  padding: 14px;
  align-content: start;
}

.platform-timeline article {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 9px 12px;
  border: 1px solid #e2ebf8;
  border-radius: 8px;
  background: #fbfdff;
}

.platform-timeline i {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--primary);
  box-shadow: 0 0 0 5px rgba(22, 93, 255, 0.12);
}

.platform-timeline strong,
.platform-timeline p {
  margin: 0;
}

.platform-timeline strong {
  font-size: 14px;
}

.platform-timeline p {
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-timeline span {
  color: var(--primary);
  font-weight: 600;
}

.platform-review__body {
  display: grid;
  gap: 12px;
  padding: 14px;
  align-content: start;
}

.platform-review article {
  display: grid;
  gap: 8px;
  padding: 12px;
  border: 1px solid #e8edf6;
  border-radius: var(--radius-lg);
  background: #fbfdff;
}

.platform-review strong,
.platform-review p {
  margin: 0;
}

.platform-review p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 20px;
}

.platform-review div div {
  display: flex;
  gap: 8px;
}

.platform-review button {
  height: 28px;
  padding: 0 10px;
  border: 1px solid #bdd7ff;
  border-radius: var(--radius-sm);
  background: #fff;
  color: var(--primary);
  cursor: pointer;
}

.platform-discovery .kg-panel__header span {
  color: var(--text-tertiary);
  font-size: 13px;
}

.platform-discovery__grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
  padding: 14px;
}

.platform-discovery__grid article {
  display: grid;
  align-content: start;
  gap: 8px;
  min-height: 116px;
  padding: 10px 12px;
  border: 1px solid #e2ebf8;
  border-radius: 8px;
  background: #fbfdff;
}

.platform-discovery__grid article div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.platform-discovery__grid span {
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-discovery__grid strong {
  color: var(--primary);
  font-size: 20px;
  line-height: 24px;
}

.platform-discovery__grid p,
.platform-discovery__grid em {
  margin: 0;
  color: var(--text-primary);
  font-size: 12px;
  font-style: normal;
  line-height: 18px;
}

.platform-discovery__grid em {
  color: var(--text-secondary);
}

.platform-gates .kg-panel__header span,
.platform-trend .kg-panel__header span,
.platform-health .kg-panel__header span,
.platform-quality .kg-panel__header span {
  color: var(--text-tertiary);
  font-size: 13px;
}

.platform-gates__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  padding: 12px 14px;
}

.platform-gates__grid article {
  display: grid;
  gap: 6px;
  padding: 12px;
  border: 1px solid #dfeafe;
  border-radius: 8px;
  background: linear-gradient(135deg, #f8fbff, #fff);
}

.platform-gates__grid span,
.platform-gates__grid p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 20px;
}

.platform-gates__grid strong {
  color: var(--primary);
  font-size: 24px;
  line-height: 28px;
}

.platform-overview-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr) minmax(0, 1fr);
  gap: 12px;
}

.platform-trend__bars {
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  align-items: end;
  gap: 10px;
  min-height: 184px;
  padding: 14px;
}

.platform-trend__bars div {
  display: grid;
  justify-items: center;
  gap: 8px;
  min-width: 0;
}

.platform-trend__bars span,
.platform-trend__bars em {
  max-width: 100%;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 12px;
  font-style: normal;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-trend__bars i {
  position: relative;
  display: flex;
  align-items: end;
  width: 22px;
  height: 98px;
  overflow: hidden;
  border-radius: 999px;
  background: #e8f1ff;
}

.platform-trend__bars b {
  width: 100%;
  border-radius: inherit;
  background: linear-gradient(180deg, #14b8a6, #165dff);
}

.platform-health__list,
.platform-quality__list {
  display: grid;
  gap: 10px;
  padding: 14px;
}

.platform-health__list article {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 52px 76px 52px;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 7px 10px;
  border: 1px solid #e2ebf8;
  border-radius: 6px;
  background: #fbfdff;
}

.platform-health__list strong,
.platform-health__list span,
.platform-health__list em,
.platform-health__list b {
  min-width: 0;
  overflow: hidden;
  font-size: 12px;
  font-style: normal;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-health__list span {
  color: #00a870;
}

.platform-health__list article.is-warning span {
  color: #ff7d00;
}

.platform-health__list em {
  color: var(--text-tertiary);
}

.platform-health__list b {
  color: var(--text-primary);
  text-align: right;
}

.platform-quality__list article {
  display: grid;
  gap: 8px;
}

.platform-quality__list article div {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-quality__list article strong {
  color: var(--text-primary);
}

.platform-quality__list i {
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: #e8f1ff;
}

.platform-quality__list b {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #165dff, #14b8a6);
}

.platform-construction {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 16px;
  min-height: 100%;
  align-items: stretch;
}

.platform-build,
.platform-graph-summary {
  min-height: 0;
  height: 100%;
}

.platform-build {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.platform-graph-summary {
  display: grid;
  align-content: start;
  gap: 12px;
  padding-bottom: 14px;
}

.platform-build-footer {
  margin-top: auto;
}

.platform-segmented {
  display: inline-flex;
  gap: 4px;
  padding: 3px;
  border: 1px solid rgba(125, 211, 252, 0.42);
  border-radius: 999px;
  background: rgba(232, 241, 255, 0.92);
}

.platform-segmented button {
  height: 28px;
  padding: 0 14px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
}

.platform-segmented button.is-active {
  background: linear-gradient(135deg, #165dff, #22d3ee);
  color: #fff;
  box-shadow: 0 6px 16px rgba(22, 93, 255, 0.26);
}

.platform-manual-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(248,251,255,0.92), rgba(240,247,255,0.8));
}

.platform-manual-toolbar button {
  flex: 0 0 auto;
  height: 32px;
  padding: 0 14px;
  border: 1px solid #bdd7ff;
  border-radius: 999px;
  background: #fff;
  color: var(--primary);
  font-size: 13px;
  cursor: pointer;
}

.platform-manual-toolbar button:first-child {
  border-color: transparent;
  background: linear-gradient(135deg, #165dff, #0ea5e9);
  color: #fff;
  box-shadow: 0 8px 18px rgba(22, 93, 255, 0.22);
}

.platform-manual-toolbar span {
  min-width: 0;
  margin-left: 6px;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 20px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-manage-filter {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) 180px 220px auto;
  align-items: end;
  gap: 10px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--border);
  background: rgba(248, 251, 255, 0.72);
}

.platform-manage-filter label {
  display: grid;
  gap: 5px;
  min-width: 0;
}

.platform-manage-filter span {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 18px;
}

.platform-manage-filter input,
.platform-manage-filter select {
  width: 100%;
  height: 30px;
  min-width: 0;
  padding: 0 9px;
  border: 1px solid #bdd7ff;
  border-radius: 6px;
  background: #fff;
  color: var(--text-primary);
  font-size: 13px;
}

.platform-manage-filter button {
  height: 30px;
  padding: 0 16px;
  border: 0;
  border-radius: 6px;
  background: var(--primary);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
}

.platform-row-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.platform-row-actions button {
  height: 24px;
  padding: 0 8px;
  border: 1px solid #bdd7ff;
  border-radius: 5px;
  background: #fff;
  color: var(--primary);
  font-size: 12px;
  line-height: 22px;
  cursor: pointer;
}

.platform-row-actions button:last-child {
  border-color: #ffd6d6;
  color: #d92d20;
  background: #fffafa;
}

.platform-impact {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  padding: 14px;
  padding-bottom: 0;
}

.platform-impact div {
  position: relative;
  overflow: hidden;
  display: grid;
  gap: 6px;
  min-height: 74px;
  padding: 10px 12px;
  border: 1px solid rgba(191, 219, 254, 0.9);
  border-radius: 8px;
  background: linear-gradient(145deg, rgba(255,255,255,0.92), rgba(236,246,255,0.88));
}

.platform-impact div::after {
  position: absolute;
  right: -14px;
  bottom: -20px;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: rgba(22, 93, 255, 0.08);
  content: "";
}

.platform-impact span {
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-impact strong {
  font-size: 24px;
  color: var(--primary);
}

.platform-rule-note {
  margin: 0 14px;
  padding: 12px;
  border: 1px solid #ffe0b2;
  border-radius: 8px;
  background: linear-gradient(135deg, #fff8ed, #fffdf8);
}

.platform-rule-note p {
  margin: 8px 0 0;
  color: #7a4a00;
  font-size: 13px;
  line-height: 20px;
}

.platform-rule-note--manual {
  border-color: #cce5d8;
  background: linear-gradient(135deg, #edfff7, #f8fffb);
}

.platform-rule-note--manual p {
  color: #12643b;
}

.platform-governance-flow {
  margin: 0 14px;
  padding: 12px;
  border: 1px solid #dce9ff;
  border-radius: 8px;
  background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(247,251,255,0.88));
}

.platform-governance-flow > strong {
  display: block;
  margin-bottom: 10px;
  color: var(--text-primary);
  font-size: 14px;
}

.platform-governance-flow ol {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.platform-governance-flow li {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr);
  gap: 8px;
  align-items: start;
}

.platform-governance-flow li span {
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #e8f1ff;
  color: var(--primary);
  font-size: 11px;
  font-weight: 600;
}

.platform-governance-flow li p {
  margin: 2px 0 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 18px;
}

.platform-query,
.platform-service {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  grid-template-rows: auto auto minmax(0, 1fr);
  gap: 12px;
}

.platform-service {
  grid-template-columns: minmax(0, 1fr) 360px;
  grid-template-rows: auto minmax(0, 1fr);
  align-items: stretch;
}

.platform-service--api {
  grid-template-columns: minmax(0, 1fr);
}

.platform-query-form,
.platform-service-console {
  grid-column: 1 / -1;
}

.platform-query {
  grid-template-rows: auto minmax(0, 1fr);
}

.platform-query-graph,
.platform-service-graph,
.platform-detail,
.platform-service-result,
.platform-api-doc {
  min-height: 0;
}

.platform-service-console {
  overflow: hidden;
}

.platform-service-console__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 42px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(191, 215, 250, 0.96);
  background:
    linear-gradient(90deg, rgba(22, 93, 255, 0.08), transparent 48%),
    rgba(248, 252, 255, 0.9);
}

.platform-service-tabs {
  display: inline-flex;
  align-items: center;
  gap: 18px;
}

.platform-service-tabs button {
  position: relative;
  height: 42px;
  border: 0;
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
}

.platform-service-tabs button.is-active {
  color: var(--primary);
  font-weight: 600;
}

.platform-service-tabs button.is-active::after {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 2px;
  border-radius: 999px;
  background: var(--primary);
  content: "";
}

.platform-service-console__body {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) repeat(3, minmax(170px, 0.8fr)) auto;
  align-items: end;
  gap: 12px;
  padding: 12px 16px 14px;
}

.platform-service--api .platform-service-console__body {
  grid-template-columns: minmax(260px, 0.9fr) minmax(360px, 1.4fr) 140px auto;
}

.platform-service-console__body label {
  display: grid;
  gap: 6px;
  min-width: 0;
}

.platform-service-console__body label span {
  color: var(--text-secondary);
  font-size: 12px;
}

.platform-service-console__body input,
.platform-service-console__body select {
  width: 100%;
  height: 32px;
  min-width: 0;
  padding: 0 10px;
  border: 1px solid #bdd7ff;
  border-radius: 6px;
  background: #fff;
  color: var(--text-primary);
  font-size: 13px;
}

.platform-service-console__actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.platform-service-console__actions button {
  height: 32px;
  padding: 0 14px;
  border: 1px solid #bdd7ff;
  border-radius: 6px;
  background: #fff;
  color: var(--primary);
  font-size: 13px;
  cursor: pointer;
}

.platform-service-console__actions button:last-child {
  border-color: transparent;
  background: linear-gradient(135deg, #165dff, #0ea5e9);
  color: #fff;
  box-shadow: 0 8px 18px rgba(22, 93, 255, 0.2);
}

.platform-svg {
  width: 100%;
  height: calc(100% - 45px);
  min-height: 340px;
  display: block;
  background:
    linear-gradient(#e8f1ff 1px, transparent 1px),
    linear-gradient(90deg, #e8f1ff 1px, transparent 1px),
    linear-gradient(135deg, rgba(22, 93, 255, 0.06), rgba(20, 184, 166, 0.04)),
    #fbfdff;
  background-size: 28px 28px, 28px 28px, auto, auto;
}

.platform-service-result {
  overflow: auto;
}

.platform-node circle {
  fill: #21c1c3;
  stroke: #fff;
  stroke-width: 2;
  filter: drop-shadow(0 4px 8px rgba(53, 77, 112, 0.14));
}

.platform-node--main circle {
  fill: #1e8ff3;
  stroke: #fff;
}

.platform-node.is-expert circle { fill: #20bfc2; }
.platform-node.is-org circle { fill: #48c914; }
.platform-node.is-company circle { fill: #ffad17; }
.platform-node.is-paper circle { fill: #762bd7; }
.platform-node.is-topic circle { fill: #1f8ff1; }
.platform-node.is-project circle { fill: #eb2aa3; }

.platform-node text {
  fill: #343b48;
  font-size: 13px;
  text-anchor: middle;
  dominant-baseline: hanging;
  transform: translateY(18px);
}

.platform-node--main text {
  fill: #fff;
  font-weight: 600;
  dominant-baseline: middle;
  transform: none;
}

.platform-network-lines line,
.platform-network-line {
  stroke: #b8c1ce;
  stroke-width: 1.4;
  marker-end: url(#platform-arrow);
}

.platform-network-lines--service line {
  marker-end: url(#service-arrow);
}

.platform-network-line.is-primary { stroke: #4080ff; stroke-width: 2; }
.platform-network-line.is-green { stroke: #00b42a; stroke-width: 2; }
.platform-network-line.is-orange { stroke: #ff7d00; stroke-width: 2; }
.platform-network-line.is-purple { stroke: #722ed1; stroke-width: 2; }

.platform-edge-label {
  paint-order: stroke;
  stroke: #fff;
  stroke-width: 8px;
  stroke-linejoin: round;
  fill: #52657f;
  font-size: 12px;
  text-anchor: middle;
  dominant-baseline: middle;
  pointer-events: none;
}

.platform-detail__body {
  display: grid;
  gap: 14px;
  padding: 14px;
}

.platform-detail dl {
  display: grid;
  gap: 8px;
  margin: 0;
}

.platform-detail dl div {
  display: grid;
  grid-template-columns: 82px minmax(0, 1fr);
  gap: 10px;
  padding: 9px 10px;
  border-radius: 6px;
  background: #f7faff;
}

.platform-detail dt,
.platform-detail dd {
  margin: 0;
  font-size: 13px;
}

.platform-detail dt {
  color: var(--text-secondary);
}

.platform-detail ul,
.platform-evidence ul {
  display: grid;
  gap: 8px;
  margin: 0;
  padding-left: 18px;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 20px;
}

.platform-result-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  padding: 14px;
}

.platform-result-grid div {
  display: grid;
  gap: 6px;
  min-height: 68px;
  padding: 10px 12px;
  border: 1px solid #e2ebf8;
  border-radius: 8px;
  background: #fbfdff;
}

.platform-result-grid span {
  color: var(--text-secondary);
  font-size: 13px;
}

.platform-result-grid strong {
  color: var(--primary);
  font-size: 22px;
}

.platform-evidence {
  display: grid;
  gap: 10px;
  margin: 0 14px 14px;
  padding: 12px;
  border: 1px solid #e2ebf8;
  border-radius: 8px;
  background: #fff;
}

.platform-service-info {
  display: grid;
  gap: 8px;
  margin: 0 14px 14px;
  padding: 12px;
  border: 1px solid #dce9ff;
  border-radius: 8px;
  background: #f8fbff;
}

.platform-service-info strong {
  color: var(--text-primary);
  font-size: 13px;
}

.platform-service-info dl {
  display: grid;
  gap: 8px;
  margin: 0;
}

.platform-service-info dl div {
  display: grid;
  grid-template-columns: 108px minmax(0, 1fr);
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #e2ebf8;
}

.platform-service-info dl div:last-child {
  border-bottom: 0;
}

.platform-service-info dt,
.platform-service-info dd {
  margin: 0;
  min-width: 0;
  font-size: 12px;
  line-height: 18px;
  overflow-wrap: anywhere;
}

.platform-service-info dt {
  color: var(--primary);
  font-family: "SFMono-Regular", Consolas, monospace;
}

.platform-service-info dd {
  color: var(--text-secondary);
}

.platform-api-doc {
  overflow: hidden;
}

.platform-service--api .platform-api-doc {
  grid-column: 1 / -1;
  overflow: auto;
}

.platform-api-doc .kg-panel__header span {
  min-width: 0;
  overflow: hidden;
  color: var(--text-tertiary);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.platform-api-doc__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 14px;
}

.platform-api-doc__grid .platform-table {
  table-layout: auto;
}

.platform-api-doc__grid .platform-table th,
.platform-api-doc__grid .platform-table td {
  height: auto;
  min-height: 38px;
  vertical-align: top;
  white-space: normal;
}

.platform-api-doc__grid article {
  min-width: 0;
  overflow: hidden;
  border: 1px solid #dce9ff;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
}

.platform-api-doc__grid h3 {
  margin: 0;
  padding: 10px 12px;
  border-bottom: 1px solid #e2ebf8;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 20px;
}

.platform-code-sample {
  margin: 0 14px 14px;
  overflow: hidden;
  border: 1px solid #dce9ff;
  border-radius: 8px;
  background: #fbfdff;
}

.platform-api-examples {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 0 14px 14px;
}

.platform-api-examples article {
  min-width: 0;
  overflow: hidden;
  border: 1px solid #dce9ff;
  border-radius: 8px;
  background: #fbfdff;
}

.platform-api-examples h3 {
  margin: 0;
  padding: 10px 12px;
  border-bottom: 1px solid #e2ebf8;
  color: var(--text-primary);
  font-size: 14px;
}

.platform-api-examples pre {
  min-height: 180px;
  max-height: 260px;
  margin: 0;
  padding: 14px 16px;
  overflow: auto;
  color: #344054;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  line-height: 20px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.platform-code-sample div {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid #e2ebf8;
}

.platform-code-sample strong {
  margin-right: auto;
  color: var(--text-primary);
  font-size: 14px;
}

.platform-code-sample span {
  min-width: 56px;
  padding: 4px 8px;
  border-radius: 5px;
  background: #eef5ff;
  color: var(--text-secondary);
  font-size: 12px;
  text-align: center;
}

.platform-code-sample span:first-of-type {
  background: #fff;
  color: var(--primary);
  box-shadow: inset 0 0 0 1px #bdd7ff;
}

.platform-code-sample pre {
  min-height: 180px;
  max-height: 280px;
  margin: 0;
  padding: 16px 18px;
  overflow: auto;
  color: #344054;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  line-height: 20px;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

@media (max-width: 1500px) {
  .platform-pipeline {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .platform-pipeline__step:not(:last-child)::after {
    display: none;
  }
}
</style>
