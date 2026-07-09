export type ServiceField = {
  name: string
  type: string
  required?: string
  description: string
}

export type ServiceResultRow = {
  label: string
  value: string
  tone?: 'blue' | 'green' | 'orange' | 'purple'
}

export type ServiceModule = {
  key: string
  title: string
  subtitle: string
  endpoint: string
  method: 'POST'
  moduleRequirement: string
  requestFields: ServiceField[]
  responseFields: ServiceField[]
  requestExample: Record<string, string | number | boolean | string[]>
  responseExample: Record<string, unknown>
  resultRows: ServiceResultRow[]
  evidence: string[]
}

const commonResponseFields: ServiceField[] = [
  { name: 'code', type: 'number', description: '服务状态码' },
  { name: 'message', type: 'string', description: '服务返回信息' },
  { name: 'data', type: 'object', description: '结构化业务结果、图谱节点关系和证据链' },
  { name: 'confidence', type: 'number', description: '综合置信度' },
  { name: 'evidence', type: 'array', description: '支撑本次结果的数据来源和证据' },
]

export const serviceModules: ServiceModule[] = [
  {
    key: 'expert-direct',
    title: '科技专家/人才直接关系',
    subtitle: '识别专家之间的直接关联类型、时间、场景和成果。',
    endpoint: '/api/v1/kg-service/expert-direct-relation',
    method: 'POST',
    moduleRequirement: '通过专家直接交互数据和知识图谱实体属性，识别并构建专家之间的直接关联，记录关系类型、发生时间、场景和相关成果。',
    requestFields: [
      { name: 'source_expert_id', type: 'string', required: '是', description: '第一个专家唯一标识' },
      { name: 'target_expert_id', type: 'string', required: '否', description: '第二个专家唯一标识' },
      { name: 'relation_scene', type: 'string', required: '否', description: '交互场景筛选条件' },
      { name: 'start_time', type: 'string', required: '否', description: '关系起始时间' },
    ],
    responseFields: commonResponseFields,
    requestExample: { source_expert_id: 'E10001', target_expert_id: 'E10002', relation_scene: '科研合作', start_time: '2020-01' },
    responseExample: { code: 0, message: 'success', data: { relation_type: '论文合作', relation_count: 12, scenario: '科研合作', confidence: 0.94 } },
    resultRows: [
      { label: '直接关系', value: '12', tone: 'blue' },
      { label: '关系类型', value: '4', tone: 'green' },
      { label: '关联成果', value: '18', tone: 'orange' },
      { label: '最高置信度', value: '0.94', tone: 'purple' },
    ],
    evidence: ['共同发表论文 4 篇，作者列表和单位信息一致。', '共同参与项目 3 项，项目角色存在协作链路。', '关系发生时间、场景和成果均已结构化记录。'],
  },
  {
    key: 'node-indirect',
    title: '科技单节点间接关系',
    subtitle: '从直接关系和多跳路径中推理潜在关联。',
    endpoint: '/api/v1/kg-service/node-indirect-relation',
    method: 'POST',
    moduleRequirement: '以单个科技专家或人才作为核心节点，挖掘知识图谱中与该节点存在间接关联的其他节点，输出传递路径、关系类型和关联强度。',
    requestFields: [
      { name: 'core_node_id', type: 'string', required: '是', description: '核心专家或人才节点 ID' },
      { name: 'relation_types', type: 'array', required: '否', description: '间接关系类型' },
      { name: 'path_depth', type: 'number', required: '否', description: '路径分析深度' },
      { name: 'min_strength', type: 'number', required: '否', description: '最小关联强度阈值' },
    ],
    responseFields: commonResponseFields,
    requestExample: { core_node_id: 'E10001', relation_types: ['学术关联', '机构关联'], path_depth: 2, min_strength: 0.65 },
    responseExample: { code: 0, message: 'success', data: { indirect_nodes: 36, paths: 58, average_strength: 0.76 } },
    resultRows: [
      { label: '间接节点', value: '36', tone: 'blue' },
      { label: '路径数量', value: '58', tone: 'green' },
      { label: '关系类型', value: '4', tone: 'orange' },
      { label: '平均强度', value: '0.76', tone: 'purple' },
    ],
    evidence: ['路径：张明远 -> 李佳宁 -> 专家C。', '路径深度为 2，命中学术关联和机构关联。', '每条间接关系均返回传递路径和强度。'],
  },
  {
    key: 'two-point-achievement',
    title: '科技两点合作成果',
    subtitle: '汇总两个专家之间的论文、项目、专利和奖项成果。',
    endpoint: '/api/v1/kg-service/two-point-achievements',
    method: 'POST',
    moduleRequirement: '针对两个科技专家或人才节点，整合合作数据，提取并汇总两者的合作成果、时间、领域、评价和合作模式。',
    requestFields: [
      { name: 'source_expert_id', type: 'string', required: '是', description: '第一个专家 ID' },
      { name: 'target_expert_id', type: 'string', required: '是', description: '第二个专家 ID' },
      { name: 'achievement_type', type: 'string', required: '否', description: '成果类型' },
      { name: 'time_range', type: 'string', required: '否', description: '成果时间范围' },
    ],
    responseFields: commonResponseFields,
    requestExample: { source_expert_id: 'E10001', target_expert_id: 'E10002', achievement_type: '论文/专利/项目', time_range: '2020-2026' },
    responseExample: { code: 0, message: 'success', data: { papers: 8, patents: 3, projects: 2, contribution: '共同算法模型' } },
    resultRows: [
      { label: '合作论文', value: '8', tone: 'blue' },
      { label: '合作专利', value: '3', tone: 'green' },
      { label: '共同项目', value: '2', tone: 'orange' },
      { label: '价值评分', value: '91', tone: 'purple' },
    ],
    evidence: ['按论文、专利、项目分类统计合作成果。', '标注完成时间、所属领域和奖项评价。', '输出核心贡献和合作模式。'],
  },
  {
    key: 'expert-colleague',
    title: '科技专家同事关系',
    subtitle: '根据工作经历、机构架构和任职时间推理同事关系。',
    endpoint: '/api/v1/kg-service/expert-colleague-relation',
    method: 'POST',
    moduleRequirement: '提取专家在不同时期的工作单位、所属部门、参与团队等机构信息，结合机构架构与人员任职数据，推理专家之间的同事关系。',
    requestFields: [
      { name: 'expert_id', type: 'string', required: '是', description: '专家唯一标识' },
      { name: 'organization', type: 'string', required: '否', description: '任职机构筛选' },
      { name: 'department', type: 'string', required: '否', description: '部门或团队筛选' },
      { name: 'overlap_period', type: 'string', required: '否', description: '任职重叠时间' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', organization: '中国科学院自动化研究所', department: '智能系统实验室', overlap_period: '2018-2022' },
    responseExample: { code: 0, message: 'success', data: { colleagues: 18, teams: 4, overlap_years: 4, achievements: 6 } },
    resultRows: [
      { label: '同事关系', value: '18', tone: 'blue' },
      { label: '共同团队', value: '4', tone: 'green' },
      { label: '重叠年限', value: '4', tone: 'orange' },
      { label: '期间成果', value: '6', tone: 'purple' },
    ],
    evidence: ['任职时间存在重叠，机构层级匹配到同一实验室。', '标注共同工作内容和协作场景。', '关联同事期间产生的合作成果。'],
  },
  {
    key: 'expert-alumni',
    title: '科技专家校友关系',
    subtitle: '基于教育经历识别院校、院系、导师和同届关联。',
    endpoint: '/api/v1/kg-service/expert-alumni-relation',
    method: 'POST',
    moduleRequirement: '基于科技专家教育背景数据和院校信息，识别并构建专家之间的校友关系，记录关联维度和后续交流合作。',
    requestFields: [
      { name: 'expert_id', type: 'string', required: '是', description: '专家唯一标识' },
      { name: 'school', type: 'string', required: '否', description: '院校筛选条件' },
      { name: 'education_stage', type: 'string', required: '否', description: '教育阶段筛选' },
      { name: 'major', type: 'string', required: '否', description: '专业或院系筛选' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', school: '北京大学', education_stage: '博士', major: '计算机科学' },
    responseExample: { code: 0, message: 'success', data: { alumni: 26, dimensions: ['同校', '同院系', '同导师'], interactions: 9 } },
    resultRows: [
      { label: '校友数量', value: '26', tone: 'blue' },
      { label: '关系维度', value: '3', tone: 'green' },
      { label: '学术互动', value: '9', tone: 'orange' },
      { label: '最高置信度', value: '0.89', tone: 'purple' },
    ],
    evidence: ['基于教育经历匹配校友关系。', '细分同校、同院系、同导师等关联维度。', '关联后续学术交流与合作互动。'],
  },
  {
    key: 'paper-cooperation',
    title: '科技专家论文合作关系',
    subtitle: '围绕论文作者、主题和被引数据分析合作网络。',
    endpoint: '/api/v1/kg-service/paper-cooperation-relation',
    method: 'POST',
    moduleRequirement: '提取作者列表、作者单位、发表时间和论文主题，识别长期稳定合作团队和核心合作人员。',
    requestFields: [
      { name: 'expert_id', type: 'string', required: '是', description: '专家唯一标识' },
      { name: 'coauthor_id', type: 'string', required: '否', description: '合作者唯一标识' },
      { name: 'topic', type: 'string', required: '否', description: '论文主题筛选' },
      { name: 'venue_level', type: 'string', required: '否', description: '期刊或会议级别' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', coauthor_id: 'E10002', topic: '人工智能', venue_level: 'A类会议' },
    responseExample: { code: 0, message: 'success', data: { papers: 14, citations: 1260, stable_team: true, topics: ['人工智能', '先进计算'] } },
    resultRows: [
      { label: '合作论文', value: '14', tone: 'blue' },
      { label: '总被引', value: '1260', tone: 'green' },
      { label: '研究方向', value: '5', tone: 'orange' },
      { label: '核心人员', value: '7', tone: 'purple' },
    ],
    evidence: ['提取作者列表、作者单位、发表时间和论文主题。', '统计期刊会议级别和被引情况。', '识别长期稳定合作团队和核心合作人员。'],
  },
  {
    key: 'enterprise-relation',
    title: '重点关注科技企业关系',
    subtitle: '连接专家、企业角色、合作领域与经营状态。',
    endpoint: '/api/v1/kg-service/key-enterprise-relation',
    method: 'POST',
    moduleRequirement: '标注专家在企业中的角色、合作领域、合作时间和模式，支持产业界资源对接分析。',
    requestFields: [
      { name: 'expert_id', type: 'string', required: '是', description: '专家唯一标识' },
      { name: 'enterprise_name', type: 'string', required: '否', description: '企业名称筛选' },
      { name: 'role_type', type: 'string', required: '否', description: '专家企业角色' },
      { name: 'industry', type: 'string', required: '否', description: '企业行业方向' },
    ],
    responseFields: commonResponseFields,
    requestExample: { expert_id: 'E10001', enterprise_name: '华南智能芯片', role_type: '顾问/股东/合作方', industry: '集成电路' },
    responseExample: { code: 0, message: 'success', data: { enterprises: 9, roles: 4, cooperation_fields: ['芯片设计', '智能制造'] } },
    resultRows: [
      { label: '关联企业', value: '9', tone: 'blue' },
      { label: '角色类型', value: '4', tone: 'green' },
      { label: '合作领域', value: '6', tone: 'orange' },
      { label: '经营风险', value: '2', tone: 'purple' },
    ],
    evidence: ['标注专家在企业中的角色、合作领域、合作时间和模式。', '关联企业行业地位、技术方向与经营状况。', '支持产业界资源对接分析。'],
  },
  {
    key: 'industry-chain-event',
    title: '科技产业链点TOP-N事件关系',
    subtitle: '围绕产业节点筛选事件并关联专家、企业和影响。',
    endpoint: '/api/v1/kg-service/industry-node-top-events',
    method: 'POST',
    moduleRequirement: '按影响力评估筛选产业链节点 TOP-N 事件，构建事件与专家、企业、人才的关联关系。',
    requestFields: [
      { name: 'chain_node_id', type: 'string', required: '是', description: '产业链节点标识' },
      { name: 'top_n', type: 'number', required: '否', description: '返回事件数量' },
      { name: 'event_type', type: 'string', required: '否', description: '事件类型筛选' },
      { name: 'time_range', type: 'string', required: '否', description: '事件时间范围' },
    ],
    responseFields: commonResponseFields,
    requestExample: { chain_node_id: 'IC-CHIP-DESIGN', top_n: 10, event_type: '投融资/政策/风险', time_range: '2025-2026' },
    responseExample: { code: 0, message: 'success', data: { events: 10, experts: 18, enterprises: 24, risk_level: '中' } },
    resultRows: [
      { label: 'TOP事件', value: '10', tone: 'blue' },
      { label: '关联专家', value: '18', tone: 'green' },
      { label: '关联企业', value: '24', tone: 'orange' },
      { label: '风险等级', value: '中', tone: 'purple' },
    ],
    evidence: ['按影响力评估筛选产业链节点 TOP-N 事件。', '构建事件与专家、企业、人才的关联关系。', '分析产业链影响和后续发展趋势。'],
  },
  {
    key: 'industry-chain-panorama',
    title: '科技产业链全景图',
    subtitle: '整合产业节点、关键技术、企业和事件形成链路全景。',
    endpoint: '/api/v1/kg-service/industry-chain-panorama',
    method: 'POST',
    moduleRequirement: '整合产业链实体、关系、事件数据，展示核心节点、关联关系和数据流向，支持层级展开和动态更新。',
    requestFields: [
      { name: 'chain_id', type: 'string', required: '是', description: '产业链标识' },
      { name: 'layer_depth', type: 'number', required: '否', description: '层级展开深度' },
      { name: 'relation_filter', type: 'array', required: '否', description: '关系筛选条件' },
      { name: 'include_events', type: 'boolean', required: '否', description: '是否包含事件' },
    ],
    responseFields: commonResponseFields,
    requestExample: { chain_id: 'AI-COMPUTING', layer_depth: 3, relation_filter: ['技术', '企业', '专家'], include_events: true },
    responseExample: { code: 0, message: 'success', data: { nodes: 186, relations: 420, key_technologies: 22, key_enterprises: 48 } },
    resultRows: [
      { label: '产业节点', value: '186', tone: 'blue' },
      { label: '链路关系', value: '420', tone: 'green' },
      { label: '关键技术', value: '22', tone: 'orange' },
      { label: '重点企业', value: '48', tone: 'purple' },
    ],
    evidence: ['整合产业链实体、关系、事件数据。', '展示核心节点、关联关系和数据流向。', '支持层级展开、关系筛选和动态更新。'],
  },
]

export function getServiceModule(key: string): ServiceModule {
  return serviceModules.find((item) => item.key === key) ?? serviceModules[0]
}
