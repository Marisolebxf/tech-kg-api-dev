<script setup lang="ts">
import { computed, onErrorCaptured, ref } from 'vue'
import { RouterView, useRoute } from 'vue-router'

import iconMenuCollapse from '../assets/icons/icon-menu-collapse.svg'
import iconMessage from '../assets/icons/icon-message.svg'
import iconSidebarArrow from '../assets/icons/icon-sidebar-arrow.svg'
import navFlow from '../assets/icons/nav-flow.svg'
import navGraph from '../assets/icons/nav-graph.svg'
import navReasoning from '../assets/icons/nav-reasoning.svg'
import { useAppStore } from '../stores/app'
import avatarBen from '../assets/images/avatar-ben.png'
import logoKg from '../assets/images/logo-kg.png'

const route = useRoute()
const appStore = useAppStore()
const pageTitle = computed(() => String(route.meta.title ?? '亿级知识图谱'))
const routeError = ref('')
const serviceNavCollapsed = ref(false)
const serviceNavItems = [
  { to: '/expert-direct', label: '专家直接关系', fullLabel: '科技专家直接关系' },
  { to: '/node-indirect', label: '单节点间接关系', fullLabel: '科技单节点间接关系' },
  { to: '/two-point-achievement', label: '两点合作成果', fullLabel: '科技两点合作成果' },
  { to: '/expert-colleague', label: '专家同事关系', fullLabel: '科技专家同事关系' },
  { to: '/expert-alumni', label: '专家校友关系', fullLabel: '科技专家校友关系' },
  { to: '/paper-cooperation', label: '论文合作关系', fullLabel: '专家论文合作关系' },
  { to: '/enterprise-relation', label: '重点企业关系', fullLabel: '重点科技企业关系' },
  { to: '/industry-chain-event', label: '产业链事件关系', fullLabel: '产业链点事件关系' },
  { to: '/industry-chain-panorama', label: '产业链全景图', fullLabel: '科技产业链全景图' },
]
const showServiceNavItems = computed(() => (
  !appStore.collapsed && !serviceNavCollapsed.value
))

onErrorCaptured((error) => {
  routeError.value = error instanceof Error ? error.message : String(error)
  return false
})
</script>

<template>
  <div class="app-viewport">
    <div class="app-shell" :class="{ 'is-collapsed': appStore.collapsed }">
        <aside class="app-sidebar">
          <div class="app-brand">
            <img class="app-brand__logo" :src="logoKg" alt="知识图谱平台" />
            <div v-if="!appStore.collapsed" class="app-brand__name">知识图谱平台</div>
            <button
              class="app-brand__menu"
              type="button"
              :aria-label="appStore.collapsed ? '展开导航' : '收起导航'"
              @click="appStore.toggleCollapsed()"
            >
              <img :src="iconMenuCollapse" alt="" aria-hidden="true" />
            </button>
          </div>

          <nav class="app-nav">
            <div v-if="!appStore.collapsed" class="app-nav__group">平台能力</div>
            <RouterLink class="app-nav__item app-nav__item--top" active-class="app-nav__item--active" to="/overview" :title="appStore.collapsed ? '平台总览' : undefined">
              <img class="app-nav__icon" :src="navFlow" alt="" aria-hidden="true" />
              <span v-if="!appStore.collapsed">平台总览</span>
              <img v-if="!appStore.collapsed" class="app-nav__arrow" :src="iconSidebarArrow" alt="" aria-hidden="true" />
            </RouterLink>
            <RouterLink class="app-nav__item app-nav__item--top" active-class="app-nav__item--active" to="/data-processing" :title="appStore.collapsed ? '数据处理' : undefined">
              <img class="app-nav__icon" :src="navGraph" alt="" aria-hidden="true" />
              <span v-if="!appStore.collapsed">数据处理</span>
              <img v-if="!appStore.collapsed" class="app-nav__arrow" :src="iconSidebarArrow" alt="" aria-hidden="true" />
            </RouterLink>
            <div v-if="!appStore.collapsed" class="app-nav__group">图谱治理</div>
            <RouterLink class="app-nav__item app-nav__item--top" active-class="app-nav__item--active" to="/graph-construction" :title="appStore.collapsed ? '图谱构建' : undefined">
              <img class="app-nav__icon" :src="navReasoning" alt="" aria-hidden="true" />
              <span v-if="!appStore.collapsed">图谱构建</span>
              <img v-if="!appStore.collapsed" class="app-nav__arrow" :src="iconSidebarArrow" alt="" aria-hidden="true" />
            </RouterLink>
            <RouterLink class="app-nav__item app-nav__item--top" active-class="app-nav__item--active" to="/graph-query" :title="appStore.collapsed ? '图谱查询' : undefined">
              <img class="app-nav__icon" :src="navGraph" alt="" aria-hidden="true" />
              <span v-if="!appStore.collapsed">图谱查询</span>
              <img v-if="!appStore.collapsed" class="app-nav__arrow" :src="iconSidebarArrow" alt="" aria-hidden="true" />
            </RouterLink>
            <div v-if="!appStore.collapsed" class="app-nav__group">服务调用</div>
            <button
              class="app-nav__item app-nav__item--top app-nav__item--button"
              :class="{ 'app-nav__item--open': !serviceNavCollapsed }"
              type="button"
              :title="appStore.collapsed ? '业务服务' : undefined"
              :aria-expanded="!serviceNavCollapsed"
              @click="serviceNavCollapsed = !serviceNavCollapsed"
            >
              <img class="app-nav__icon" :src="navReasoning" alt="" aria-hidden="true" />
              <span v-if="!appStore.collapsed">业务服务</span>
              <img v-if="!appStore.collapsed" class="app-nav__arrow" :src="iconSidebarArrow" alt="" aria-hidden="true" />
            </button>
            <RouterLink
              v-for="(item, index) in serviceNavItems"
              :key="item.to"
              v-if="showServiceNavItems"
              class="app-nav__item app-nav__item--sub"
              active-class="app-nav__item--active"
              :to="item.to"
              :title="item.fullLabel"
            >
              <em>{{ String(index + 1).padStart(2, '0') }}</em>
              <span>{{ item.label }}</span>
            </RouterLink>
          </nav>

          <div class="app-user">
            <img class="app-user__avatar" :src="avatarBen" alt="" aria-hidden="true" />
            <span v-if="!appStore.collapsed">系统管理员</span>
            <img v-if="!appStore.collapsed" class="app-user__message" :src="iconMessage" alt="" aria-hidden="true" />
          </div>
        </aside>

        <main class="app-main">
          <section class="app-workspace" :aria-label="pageTitle">
            <div v-if="routeError" class="route-error">
              <strong>页面渲染异常</strong>
              <span>{{ routeError }}</span>
            </div>
            <RouterView v-else />
          </section>
        </main>
      </div>
  </div>
</template>

<style scoped>
.app-viewport {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  background: #dcecff;
}

.app-shell {
  display: grid;
  grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
  width: 100%;
  height: 100%;
  background:
    linear-gradient(135deg, #dbeaff 0%, #eef6ff 45%, #e0f1ff 100%);
  transition: grid-template-columns 0.2s ease;
}

.app-shell.is-collapsed {
  grid-template-columns: var(--sidebar-width-collapsed) minmax(0, 1fr);
}

.app-sidebar {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
  padding: 20px 16px 16px;
  overflow: hidden;
  color: var(--text-primary);
  border-right: 1px solid rgba(132, 178, 246, 0.82);
  background:
    linear-gradient(180deg, rgba(232, 243, 255, 0.98) 0%, rgba(213, 232, 255, 0.98) 58%, rgba(199, 224, 255, 0.98) 100%),
    #dcecff;
  box-shadow: 16px 0 36px rgba(48, 105, 194, 0.18);
}

.app-sidebar::before {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(22, 93, 255, 0.075) 1px, transparent 1px),
    linear-gradient(rgba(22, 93, 255, 0.075) 1px, transparent 1px);
  background-size: 26px 26px;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.62), transparent 78%);
  pointer-events: none;
  content: "";
}

.app-sidebar > * {
  position: relative;
}

.app-brand {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 12px;
  height: 48px;
  padding-bottom: 18px;
  border-bottom: 1px solid rgba(84, 139, 220, 0.22);
}

.app-brand__logo {
  width: 38px;
  height: 38px;
  object-fit: contain;
}

.app-brand__name {
  flex: 0 0 auto;
  font-size: 22px;
  line-height: 30px;
  font-weight: 700;
  color: #10264c;
  white-space: nowrap;
}

.app-brand__menu {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  margin-left: auto;
  padding: 0;
  border: 0;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
}

.app-brand__menu img {
  width: 18px;
  height: 18px;
  object-fit: contain;
  opacity: 0.72;
}

.app-brand__menu:hover {
  background: rgba(255, 255, 255, 0.72);
}

.app-shell.is-collapsed .app-brand {
  justify-content: center;
}

.app-shell.is-collapsed .app-brand__menu {
  margin-left: 0;
}

.app-shell.is-collapsed .app-nav__item {
  grid-template-columns: 22px;
  justify-content: center;
  padding-inline: 0;
}

.app-shell.is-collapsed .app-nav__item--active {
  width: calc(100% - 12px);
  margin-left: 6px;
}

.app-nav {
  position: relative;
  flex: 1 1 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 18px;
  padding-bottom: 14px;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: none;
}

.app-nav::-webkit-scrollbar {
  display: none;
}

.app-nav::after {
  display: none;
}

.app-nav__item {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr) 14px;
  align-items: center;
  gap: 14px;
  min-height: 54px;
  padding: 0 16px;
  border: 1px solid transparent;
  border-radius: 6px;
  color: #243b63;
  font-size: 20px;
  line-height: 28px;
  white-space: nowrap;
  transition:
    background 0.16s ease,
    border-color 0.16s ease,
    color 0.16s ease;
}

.app-nav__item--button {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  border-color: transparent;
  background: transparent;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}

.app-nav__item--button:focus {
  outline: none;
}

.app-nav__item--button:focus-visible {
  border-color: rgba(86, 149, 239, 0.52);
  background: rgba(255, 255, 255, 0.62);
}

.app-nav__item:hover {
  color: #165dff;
  border-color: rgba(86, 149, 239, 0.52);
  background: rgba(255, 255, 255, 0.86);
}

.app-nav__group {
  margin: 18px 8px 10px;
  color: #567198;
  font-size: 17px;
  line-height: 25px;
  font-weight: 500;
  letter-spacing: 0;
}

.app-nav__icon {
  width: 21px;
  height: 21px;
  align-self: center;
  justify-self: center;
  object-fit: contain;
  opacity: 0.82;
}

.app-nav__arrow {
  width: 14px;
  height: 14px;
  justify-self: end;
  object-fit: contain;
  opacity: 0.52;
  transition: transform 0.16s ease;
}

.app-nav__item--open {
  margin-top: 8px;
}

.app-nav__item--open .app-nav__arrow {
  transform: rotate(90deg);
}

.app-nav__item--active {
  position: relative;
  z-index: 1;
  grid-template-columns: 1fr;
  width: min(246px, calc(100% - 28px));
  margin-left: 28px;
  color: #165dff;
  border-color: rgba(87, 150, 242, 0.76);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(218, 235, 255, 0.96)),
    #f7fbff;
  box-shadow:
    inset 3px 0 0 #165dff,
    0 10px 24px rgba(22, 93, 255, 0.18);
}

.app-nav__item--active .app-nav__icon,
.app-nav__item--active .app-nav__arrow {
  opacity: 1;
}

.app-nav__item--top.app-nav__item--active {
  grid-template-columns: 22px minmax(0, 1fr) 14px;
  width: 100%;
  margin-left: 0;
}

.app-nav__item--sub {
  position: relative;
  z-index: 1;
  grid-template-columns: 36px minmax(0, 1fr);
  width: min(250px, calc(100% - 34px));
  min-height: 56px;
  margin: 4px 0 4px 34px;
  padding: 0 14px;
  border-color: rgba(179, 209, 255, 0.42);
  background: rgba(255, 255, 255, 0.42);
  color: #2e4770;
  font-size: 18px;
  line-height: 27px;
}

.app-nav__item--sub em {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 24px;
  border-radius: 999px;
  background: rgba(22, 93, 255, 0.08);
  color: #4c74b4;
  font-size: 13px;
  font-style: normal;
  font-weight: 700;
}

.app-nav__item--sub span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-nav__item--sub.app-nav__item--active {
  color: var(--primary);
  border: 1px solid rgba(87, 150, 242, 0.72);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(226, 239, 255, 0.96)),
    #eef5ff;
  box-shadow: inset 3px 0 0 #165dff, 0 8px 18px rgba(22, 93, 255, 0.12);
}

.app-nav__item--sub.app-nav__item--active em {
  background: var(--primary);
  color: #fff;
}

.app-user {
  position: static;
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  gap: var(--space-8);
  width: 100%;
  min-width: 0;
  margin-top: 10px;
  font-size: 20px;
  line-height: 28px;
  color: #243b63;
}

.app-user__avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.app-user__message {
  width: 22px;
  height: 22px;
  margin-left: auto;
  object-fit: contain;
  opacity: 0.72;
}

.app-main {
  min-width: 0;
  height: 100%;
  padding: 20px 22px;
  overflow: hidden;
}

.app-workspace {
  height: 100%;
  padding: 0;
  border: 0;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  overflow: hidden;
}

.route-error {
  display: grid;
  align-content: center;
  gap: 10px;
  height: 100%;
  padding: 32px;
  color: #b42318;
  background: #fff7f6;
  border: 1px solid #fecdca;
  border-radius: var(--radius-md);
}

.route-error strong {
  font-size: 18px;
}

.route-error span {
  color: #912018;
  overflow-wrap: anywhere;
}

@media (max-height: 820px), (max-width: 1500px) {
  .app-nav::after {
    top: 126px;
  }

  .app-nav__item {
    min-height: 48px;
  }

  .app-nav__item--sub,
  .app-nav__item--active {
    width: min(238px, calc(100% - 34px));
  }
}

@media (max-height: 720px) {
  .app-sidebar {
    padding-bottom: 12px;
  }

  .app-nav {
    padding-bottom: 10px;
  }

  .app-nav__item {
    min-height: 42px;
    font-size: 18px;
    line-height: 25px;
  }

  .app-nav__item--sub,
  .app-nav__item--active {
    width: min(238px, calc(100% - 34px));
  }
}
</style>
