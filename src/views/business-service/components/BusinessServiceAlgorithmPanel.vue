<script setup lang="ts">
import { computed, ref, watch } from 'vue'

import iconInfo from '../../../assets/icons/icon-info.svg'
import KgGraphCanvas from '../../../components/kg-graph-canvas.vue'
import { getServiceGraphPreset } from '../../../data/graph-presets'
import type { GraphEdgeData, GraphNodeData } from '../../../data/graph-presets'
import type { ServiceModule } from '../service-modules'

const props = defineProps<{
  moduleInfo: ServiceModule
  responseJson: string
}>()

const resultMode = ref<'summary' | 'entity' | 'relation' | 'rule' | 'api'>('summary')
const running = ref(false)
const lastTestTime = ref('2026-07-23 11:00:00')
const parameterValues = ref<Record<string, string>>({})
const selectedGraphNodeId = ref<string | null>('core')
const selectedGraphEdgeId = ref<string | null>(null)
const graphPreset = computed(() => getServiceGraphPreset(props.moduleInfo.key))
const graphNodes = computed(() => graphPreset.value.nodes)
const graphEdges = computed(() => graphPreset.value.edges.filter((edge) => (
  graphNodes.value.some((node) => node.id === edge.from) &&
  graphNodes.value.some((node) => node.id === edge.to)
)))
const selectedNode = computed(() => (
  graphNodes.value.find((node) => node.id === selectedGraphNodeId.value) ?? graphNodes.value[0]
))
const selectedEdge = computed(() => (
  graphEdges.value.find((edge) => edge.id === selectedGraphEdgeId.value) ?? graphEdges.value[0]
))
const selectedEdgeNodes = computed(() => {
  const edge = selectedEdge.value
  return {
    from: graphNodes.value.find((node) => node.id === edge?.from),
    to: graphNodes.value.find((node) => node.id === edge?.to),
  }
})
const relationDetailRows = computed(() => {
  const edge = selectedEdge.value
  const from = selectedEdgeNodes.value.from
  const to = selectedEdgeNodes.value.to
  if (!edge || !from || !to) return []
  return [
    ['源实体', `${from.label} / ${from.entityType}`] as const,
    ['目标实体', `${to.label} / ${to.entityType}`] as const,
    ['关系类型', edge.label] as const,
    ['关系分类', edge.category] as const,
    ['置信度', `${Math.min(from.confidence, to.confidence).toFixed(2)}`] as const,
    ['命中规则', props.moduleInfo.rules[0]?.name ?? '已命中关系识别规则'] as const,
  ]
})
const detailRows = computed(() => {
  const requestEntries = props.moduleInfo.requestFields.slice(0, 4).map((field) => [
    field.description,
    parameterValues.value[field.name] ?? formatValue(props.moduleInfo.requestExample[field.name]),
  ] as const)
  const resultEntries = props.moduleInfo.resultRows.map((row) => [row.label, row.value] as const)
  return [
    ['子功能名称', props.moduleInfo.title] as const,
    ['最近测试时间', lastTestTime.value] as const,
    ...resultEntries,
    ...requestEntries,
    ...props.moduleInfo.rules.slice(0, 3).map((rule, index) => [`规则${index + 1}`, rule.name] as const),
  ]
})
const apiResultJson = computed(() => JSON.stringify({
  ...JSON.parse(props.responseJson),
  request_params: parameterValues.value,
}, null, 2))

watch(
  () => props.moduleInfo.key,
  () => {
    resultMode.value = 'summary'
    selectedGraphNodeId.value = 'core'
    selectedGraphEdgeId.value = null
    resetParameters()
  },
  { immediate: true },
)

function formatValue(value: unknown) {
  if (Array.isArray(value)) return value.join('、')
  if (typeof value === 'boolean') return value ? '是' : '否'
  return String(value ?? '-')
}

function resetParameters() {
  parameterValues.value = Object.fromEntries(
    props.moduleInfo.requestFields.map((field) => [
      field.name,
      formatValue(props.moduleInfo.requestExample[field.name]),
    ]),
  )
}

function handleRun() {
  running.value = true
  window.setTimeout(() => {
    lastTestTime.value = '2026-07-23 11:00:00'
    running.value = false
  }, 360)
}

function handleParameterInput(fieldName: string, event: Event) {
  parameterValues.value = {
    ...parameterValues.value,
    [fieldName]: (event.target as HTMLInputElement).value,
  }
}

function handleSelectGraphNode(node: GraphNodeData) {
  selectedGraphNodeId.value = node.id
  selectedGraphEdgeId.value = null
  resultMode.value = 'entity'
}

function handleSelectGraphEdge(edge: GraphEdgeData) {
  selectedGraphEdgeId.value = edge.id
  selectedGraphNodeId.value = null
  resultMode.value = 'relation'
}
</script>

<template>
  <section class="kg-panel service-console">
    <div class="service-console__head">
      <div>
        <h2>{{ moduleInfo.title }}</h2>
        <p>{{ moduleInfo.subtitle }}</p>
      </div>
      <img class="field-info-icon" :src="iconInfo" alt="" aria-hidden="true" />
    </div>
    <div class="service-console__params">
      <label v-for="field in moduleInfo.requestFields" :key="field.name">
        <span><i v-if="field.required === '是'">*</i>{{ field.name }}</span>
        <input
          :value="parameterValues[field.name] ?? ''"
          :placeholder="field.description"
          @input="handleParameterInput(field.name, $event)"
        />
      </label>
    </div>
    <div class="service-console__actions">
      <button class="kg-button" type="button" @click="handleRun">{{ running ? '测试中...' : '执行测试' }}</button>
      <button class="kg-button kg-button--secondary" type="button" @click="resetParameters">重置参数</button>
    </div>
  </section>

  <div class="business-service__main">
    <section class="kg-panel graph-panel">
      <div class="kg-panel__header">
        <h2 class="kg-panel__title">测试结果预览</h2>
        <div class="graph-panel__time">
          <span>最近测试时间：</span>
          <strong>{{ lastTestTime }}</strong>
        </div>
      </div>
      <div class="graph-panel__canvas">
        <KgGraphCanvas
          :nodes="graphNodes"
          :edges="graphEdges"
          :selected-node-id="selectedGraphNodeId"
          :selected-edge-id="selectedGraphEdgeId"
          aria-label="测试结果图谱"
          @select-node="handleSelectGraphNode"
          @select-edge="handleSelectGraphEdge"
        />
      </div>
    </section>

    <aside class="business-service__side">
      <section class="kg-panel result-panel">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">结果详情</h2>
          <div class="result-panel__tabs">
            <button :class="{ 'is-active': resultMode === 'summary' }" type="button" @click="resultMode = 'summary'">摘要</button>
            <button :class="{ 'is-active': resultMode === 'entity' }" type="button" @click="resultMode = 'entity'">实体</button>
            <button :class="{ 'is-active': resultMode === 'relation' }" type="button" @click="resultMode = 'relation'">关系</button>
            <button :class="{ 'is-active': resultMode === 'rule' }" type="button" @click="resultMode = 'rule'">规则</button>
            <button :class="{ 'is-active': resultMode === 'api' }" type="button" @click="resultMode = 'api'">API</button>
          </div>
        </div>
        <dl v-if="resultMode === 'summary'" class="result-panel__table">
          <div v-for="([label, value], index) in detailRows" :key="`${label}-${index}`">
            <dt>{{ label }}</dt>
            <dd>{{ value }}</dd>
          </div>
        </dl>
        <dl v-else-if="resultMode === 'entity'" class="result-panel__table">
          <div><dt>实体名称</dt><dd>{{ selectedNode.label }}</dd></div>
          <div><dt>实体类型</dt><dd>{{ selectedNode.entityType }}</dd></div>
          <div><dt>命中关系</dt><dd>{{ selectedNode.relations }}</dd></div>
          <div><dt>置信度</dt><dd>{{ selectedNode.confidence.toFixed(2) }}</dd></div>
          <div><dt>数据来源</dt><dd>专家库 / 论文库 / 项目库 / 工商库</dd></div>
        </dl>
        <dl v-else-if="resultMode === 'relation'" class="result-panel__table">
          <div v-for="([label, value], index) in relationDetailRows" :key="`${label}-${index}`">
            <dt>{{ label }}</dt>
            <dd>{{ value }}</dd>
          </div>
        </dl>
        <div v-else-if="resultMode === 'rule'" class="result-panel__rules">
          <article v-for="(rule, index) in moduleInfo.rules" :key="rule.name">
            <header>
              <strong>规则 {{ index + 1 }}：{{ rule.name }}</strong>
              <span>{{ rule.type }}</span>
            </header>
            <dl>
              <div><dt>适用对象</dt><dd>{{ rule.target }}</dd></div>
              <div><dt>触发条件</dt><dd>{{ rule.trigger }}</dd></div>
              <div><dt>处理逻辑</dt><dd>{{ rule.logic }}</dd></div>
              <div><dt>输出结果</dt><dd>{{ rule.output }}</dd></div>
              <div><dt>置信度阈值</dt><dd>{{ rule.threshold }}</dd></div>
              <div><dt>审核策略</dt><dd>{{ rule.audit }}</dd></div>
            </dl>
          </article>
        </div>
        <pre v-else class="result-panel__code">{{ apiResultJson }}</pre>
      </section>
    </aside>
  </div>
</template>

<style scoped>
.service-console {
  display: grid;
  grid-template-columns: minmax(240px, 0.8fr) minmax(0, 1.8fr) auto;
  align-items: end;
  gap: 14px;
  min-height: 92px;
  padding: 14px 16px;
  overflow: hidden;
}

.service-console__head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 16px;
  align-items: start;
  gap: 10px;
  min-width: 0;
}

.service-console__head h2 {
  margin: 0;
  color: #10264c;
  font-size: 18px;
  line-height: 26px;
  font-weight: 700;
}

.service-console__head p {
  margin: 4px 0 0;
  color: var(--text-tertiary);
  font-size: 14px;
  line-height: 22px;
  overflow-wrap: anywhere;
}

.service-console__params {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  min-width: 0;
}

.service-console__params label {
  display: grid;
  gap: 6px;
  min-width: 0;
}

.service-console__params span {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 20px;
}

.service-console__params i {
  margin-right: 4px;
  color: var(--danger);
  font-style: normal;
}

.service-console__params input {
  width: 100%;
  height: 36px;
  min-width: 0;
  padding: 0 10px;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: #fff;
  color: var(--text-primary);
  font-size: 15px;
}

.field-info-icon {
  width: 14px;
  height: 14px;
}

.service-console__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
  min-width: 236px;
}

.business-service__main {
  display: grid;
  grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr);
  gap: var(--space-16);
  flex: 1;
  min-height: 0;
  padding: var(--space-16);
  border-radius: var(--radius-md);
  background: var(--surface-subtle);
  overflow: hidden;
}

.business-service__side,
.graph-panel,
.result-panel {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

.business-service__side,
.graph-panel,
.result-panel {
  height: 100%;
}

.graph-panel__time {
  display: flex;
  gap: var(--space-12);
  color: var(--text-tertiary);
}

.graph-panel__time strong {
  font-weight: 400;
}

.graph-panel__canvas {
  height: calc(100% - 50px);
  min-height: 0;
  overflow: hidden;
}

:deep(.kg-graph-viewport) {
  height: 100%;
  min-height: 0;
}

.result-panel__tabs {
  display: inline-flex;
  gap: 0;
  padding: 2px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface-subtle);
}

.result-panel__tabs button {
  height: 28px;
  padding: 0 12px;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
}

.result-panel__tabs button.is-active {
  background: var(--surface);
  color: var(--primary);
  font-weight: 600;
}

.result-panel__table {
  flex: 1;
  min-height: 0;
  margin: 0;
  overflow: auto;
}

.result-panel__table div {
  display: grid;
  grid-template-columns: 190px minmax(0, 1fr);
  min-height: 44px;
  border-bottom: 1px solid var(--border);
}

.result-panel__table dt,
.result-panel__table dd {
  margin: 0;
  padding: 10px 14px;
  font-size: 15px;
  line-height: 24px;
}

.result-panel__table dt {
  color: var(--text-tertiary);
  text-align: right;
  border-right: 1px solid var(--border);
  font-weight: 600;
}

.result-panel__table dd {
  color: var(--text-primary);
  overflow-wrap: anywhere;
}

.result-panel__code {
  flex: 1;
  min-height: 0;
  margin: 0;
  padding: 14px 16px;
  overflow: auto;
  color: #2f3442;
  background: #f7f9fc;
  font-family: Consolas, Monaco, monospace;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre-wrap;
}

.result-panel__rules {
  flex: 1;
  min-height: 0;
  display: grid;
  gap: 10px;
  align-content: start;
  padding: 14px;
  overflow: auto;
}

.result-panel__rules article {
  display: grid;
  gap: 10px;
  padding: 12px;
  border: 1px solid #e2ebf8;
  border-radius: 8px;
  background: #fbfdff;
}

.result-panel__rules header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-width: 0;
}

.result-panel__rules strong {
  color: var(--primary);
  font-size: 15px;
}

.result-panel__rules header span {
  flex: 0 0 auto;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--primary-subtle);
  color: var(--primary);
  font-size: 12px;
  line-height: 18px;
}

.result-panel__rules dl {
  display: grid;
  gap: 6px;
  margin: 0;
}

.result-panel__rules dl div {
  display: grid;
  grid-template-columns: 84px minmax(0, 1fr);
  gap: 8px;
  align-items: start;
}

.result-panel__rules dt,
.result-panel__rules dd {
  margin: 0;
  font-size: 14px;
  line-height: 22px;
}

.result-panel__rules dt {
  color: var(--text-tertiary);
  font-weight: 600;
  text-align: right;
}

.result-panel__rules dd {
  color: var(--text-secondary);
  overflow-wrap: anywhere;
}

@media (max-width: 1280px) {
  .service-console,
  .business-service__main,
  .service-console__params {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
