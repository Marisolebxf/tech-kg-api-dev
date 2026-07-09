<script setup lang="ts">
import { computed, ref, watch } from 'vue'

import iconClose from '../../../assets/icons/icon-close.svg'
import iconInfo from '../../../assets/icons/icon-info.svg'
import iconModalSetting from '../../../assets/icons/icon-modal-setting.svg'
import iconSelectArrow from '../../../assets/icons/icon-select-arrow.svg'
import { getServiceGraphPreset } from '../../../data/graph-presets'
import type { GraphNodeData } from '../../../data/graph-presets'
import type { ServiceModule } from '../service-modules'

const props = defineProps<{
  moduleInfo: ServiceModule
  responseJson: string
}>()

const resultMode = ref<'structured' | 'api'>('structured')
const running = ref(false)
const showConfigModal = ref(false)
const lastTestTime = ref('2026-07-23 11:00:00')
const parameterValues = ref<Record<string, string>>({})
const graphPreset = computed(() => getServiceGraphPreset(props.moduleInfo.key))
const graphNodes = computed(() => graphPreset.value.nodes.slice(0, 7).map((node, index) => normalizeNode(node, index)))
const graphEdges = computed(() => graphPreset.value.edges.filter((edge) => (
  graphNodes.value.some((node) => node.id === edge.from) &&
  graphNodes.value.some((node) => node.id === edge.to)
)))
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
    ...props.moduleInfo.evidence.slice(0, 3).map((line, index) => [`证据${index + 1}`, line] as const),
  ]
})
const apiResultJson = computed(() => JSON.stringify({
  ...JSON.parse(props.responseJson),
  request_params: parameterValues.value,
}, null, 2))

watch(
  () => props.moduleInfo.key,
  () => {
    resultMode.value = 'structured'
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

function normalizeNode(node: GraphNodeData, index: number) {
  const toneMap: Record<string, string> = {
    main: 'blue',
    expert: 'green',
    org: 'purple',
    company: 'orange',
    paper: 'orange',
    topic: 'purple',
    project: 'gold',
  }
  const slots = [
    { x: 74, y: 224, width: 188, height: 70 },
    { x: 458, y: 36, width: 176, height: 62 },
    { x: 458, y: 156, width: 176, height: 62 },
    { x: 458, y: 276, width: 176, height: 62 },
    { x: 458, y: 396, width: 176, height: 62 },
    { x: 262, y: 126, width: 170, height: 62 },
    { x: 262, y: 326, width: 170, height: 62 },
  ]
  const slot = slots[index] ?? slots[slots.length - 1]
  return {
    ...node,
    boxX: slot.x,
    boxY: slot.y,
    width: slot.width,
    height: slot.height,
    tone: toneMap[node.nodeType] ?? 'blue',
    shortLabel: truncateText(node.label, 12),
    shortType: truncateText(node.entityType, 12),
  }
}

function truncateText(value: string, maxLength: number) {
  return value.length > maxLength ? `${value.slice(0, maxLength - 1)}…` : value
}

function nodeCenter(id: string) {
  const node = graphNodes.value.find((item) => item.id === id)
  if (!node) return { x: 0, y: 0 }
  return { x: node.boxX + node.width / 2, y: node.boxY + node.height / 2 }
}

function edgePath(from: string, to: string) {
  const start = nodeCenter(from)
  const end = nodeCenter(to)
  const midX = (start.x + end.x) / 2
  return `M ${start.x} ${start.y} C ${midX} ${start.y}, ${midX} ${end.y}, ${end.x} ${end.y}`
}

function edgeLabelPosition(from: string, to: string, index: number) {
  const start = nodeCenter(from)
  const end = nodeCenter(to)
  const offsets = [-18, 18, -30, 30, -42, 42]
  return { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 + (offsets[index % offsets.length] ?? -18) }
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

function handleSaveAndRun() {
  showConfigModal.value = false
  handleRun()
}
</script>

<template>
  <section class="search-panel-inline">
    <label class="search-panel-inline__field">
      <span>子功能名称：</span>
      <select class="select-with-icon" :value="moduleInfo.key" disabled>
        <option :value="moduleInfo.key">{{ moduleInfo.title }}查询接口</option>
      </select>
      <img class="select-icon" :src="iconSelectArrow" alt="" aria-hidden="true" />
      <img class="field-info-icon" :src="iconInfo" alt="" aria-hidden="true" />
    </label>
    <div class="search-panel-inline__actions">
      <button class="kg-button kg-button--secondary" type="button" @click="showConfigModal = true">参数设置</button>
      <button class="kg-button" type="button" @click="handleRun">{{ running ? '测试中...' : '执行测试' }}</button>
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
      <div class="graph-panel__canvas kg-graph-canvas">
        <svg class="service-box-graph" viewBox="0 0 760 520" role="img" aria-label="测试结果图谱">
          <defs>
            <marker id="service-arrow-blue" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4">
              <path d="M0,0 L8,4 L0,8 Z" fill="#4080ff" />
            </marker>
          </defs>
          <g class="graph-edges">
            <template v-for="(edge, index) in graphEdges" :key="edge.id">
              <path class="edge" :d="edgePath(edge.from, edge.to)" marker-end="url(#service-arrow-blue)" />
              <text class="edge-label" :x="edgeLabelPosition(edge.from, edge.to, index).x" :y="edgeLabelPosition(edge.from, edge.to, index).y">{{ truncateText(edge.label, 8) }}</text>
            </template>
          </g>
          <g class="graph-nodes">
            <g v-for="node in graphNodes" :key="node.id" class="box" :class="`box--${node.tone}`" :transform="`translate(${node.boxX} ${node.boxY})`">
              <rect :width="node.width" :height="node.height" rx="6" />
              <text :x="node.width / 2" :y="node.height / 2 - 4">{{ node.shortLabel }}</text>
              <text class="node-type" :x="node.width / 2" :y="node.height / 2 + 18">{{ node.shortType }}</text>
            </g>
          </g>
        </svg>
      </div>
    </section>

    <aside class="business-service__side">
      <section class="kg-panel result-panel">
        <div class="kg-panel__header">
          <h2 class="kg-panel__title">结果详情</h2>
          <div class="result-panel__tabs">
            <button :class="{ 'is-active': resultMode === 'structured' }" type="button" @click="resultMode = 'structured'">结构化结果</button>
            <button :class="{ 'is-active': resultMode === 'api' }" type="button" @click="resultMode = 'api'">API结果示例</button>
          </div>
        </div>
        <dl v-if="resultMode === 'structured'" class="result-panel__table">
          <div v-for="([label, value], index) in detailRows" :key="`${label}-${index}`">
            <dt>{{ label }}</dt>
            <dd>{{ value }}</dd>
          </div>
        </dl>
        <pre v-else class="result-panel__code">{{ apiResultJson }}</pre>
      </section>
    </aside>
  </div>

  <div v-if="showConfigModal" class="modal-mask" @click.self="showConfigModal = false">
    <section class="modal modal--config" role="dialog" aria-modal="true">
      <header class="modal__header">
        <h2><img :src="iconModalSetting" alt="" aria-hidden="true" />测试参数设置</h2>
        <button type="button" @click="showConfigModal = false">
          <img :src="iconClose" alt="" aria-hidden="true" />
        </button>
      </header>
      <div class="modal__body config-form">
        <label v-for="field in moduleInfo.requestFields" :key="field.name">
          <span><i>{{ field.required === '是' ? '*' : '' }}</i>{{ field.name }}</span>
          <input
            :value="parameterValues[field.name] ?? ''"
            :placeholder="field.description"
            @input="handleParameterInput(field.name, $event)"
          />
          <small>{{ field.description }}</small>
        </label>
      </div>
      <footer class="modal__footer">
        <button class="kg-button kg-button--secondary" type="button" @click="showConfigModal = false">取消</button>
        <button class="kg-button" type="button" @click="handleSaveAndRun">保存并执行</button>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.search-panel-inline {
  display: grid;
  grid-template-columns: 520px minmax(220px, 1fr);
  gap: 10px;
  align-items: end;
  min-height: 40px;
  padding: 0 14px 2px;
  font-size: 14px;
}

.search-panel-inline__field {
  position: relative;
  display: grid;
  grid-template-columns: max-content minmax(0, 1fr) 14px;
  align-items: center;
  gap: var(--space-8);
}

.search-panel-inline__field select {
  width: 100%;
  height: 32px;
  padding: 0 34px 0 var(--space-12);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text-primary);
}

.search-panel-inline__field select:disabled {
  opacity: 1;
  cursor: default;
}

.select-with-icon {
  appearance: none;
  -webkit-appearance: none;
  background-image: none;
  cursor: pointer;
}

.select-icon {
  position: absolute;
  top: 50%;
  right: 28px;
  width: 14px;
  height: 14px;
  transform: translateY(-50%);
  pointer-events: none;
}

.field-info-icon {
  width: 14px;
  height: 14px;
}

.search-panel-inline__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-16);
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
  display: grid;
  place-items: center;
  height: calc(100% - 44px);
  min-height: 0;
  padding: var(--space-16);
  overflow: hidden;
}

.service-box-graph {
  display: block;
  width: min(100%, 980px);
  height: auto;
  max-height: min(100%, 720px);
  aspect-ratio: 760 / 520;
}

.edge {
  fill: none;
  stroke: var(--graph-blue);
  stroke-width: 2;
}

.edge-label {
  paint-order: stroke;
  stroke: #fff;
  stroke-width: 8px;
  stroke-linejoin: round;
  fill: var(--primary);
  font-size: 12px;
  text-anchor: middle;
}

.box rect {
  fill: #ffffff;
  stroke-width: 1.6;
  filter: drop-shadow(0 8px 14px rgba(64, 128, 255, 0.12));
}

.box text {
  fill: var(--text-primary);
  text-anchor: middle;
  font-size: 12px;
  font-weight: 600;
}

.box .node-type {
  fill: var(--text-secondary);
  font-size: 12px;
  font-weight: 400;
}

.box--blue rect { stroke: var(--graph-blue); fill: #f7fbff; }
.box--green rect { stroke: var(--graph-green); fill: #f3fff6; }
.box--purple rect { stroke: var(--graph-purple); fill: #fbf7ff; }
.box--orange rect { stroke: var(--graph-orange); fill: #fff9f0; }
.box--gold rect { stroke: var(--graph-gold); fill: #fffbe8; }

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
  padding: 9px 12px;
  font-size: 14px;
  line-height: 22px;
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

.modal-mask {
  position: fixed;
  inset: 0;
  z-index: 30;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(16, 38, 76, 0.28);
}

.modal {
  width: min(720px, 100%);
  max-height: min(760px, calc(100vh - 48px));
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid rgba(167, 201, 250, 0.96);
  border-radius: var(--radius-md);
  background: var(--surface);
  box-shadow: 0 18px 46px rgba(48, 105, 194, 0.24);
}

.modal__header,
.modal__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 48px;
  padding: 0 16px;
  border-bottom: 1px solid var(--border);
}

.modal__footer {
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border);
  border-bottom: 0;
}

.modal__header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.modal__header img {
  width: 16px;
  height: 16px;
}

.modal__header button {
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: var(--radius-sm);
  background: transparent;
  cursor: pointer;
}

.modal__body {
  min-height: 0;
  overflow: auto;
  padding: 16px;
}

.config-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px 16px;
}

.config-form label {
  display: grid;
  gap: 6px;
  min-width: 0;
}

.config-form span {
  color: var(--text-secondary);
  font-size: 13px;
}

.config-form i {
  margin-right: 4px;
  color: var(--danger);
  font-style: normal;
}

.config-form input {
  width: 100%;
  height: 32px;
  padding: 0 10px;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text-primary);
}

.config-form small {
  color: var(--text-tertiary);
  font-size: 12px;
  line-height: 18px;
}

@media (max-width: 1280px) {
  .search-panel-inline,
  .business-service__main {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 720px) {
  .config-form {
    grid-template-columns: minmax(0, 1fr);
  }
}
</style>
