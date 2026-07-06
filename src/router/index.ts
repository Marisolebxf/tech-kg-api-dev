import { createRouter, createWebHashHistory } from 'vue-router'

import PlatformWorkbenchView from '../views/platform/PlatformWorkbenchView.vue'

export const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/overview',
    },
    {
      path: '/overview',
      name: 'overview',
      component: PlatformWorkbenchView,
      props: { initialTab: 'overview' },
      meta: { title: '平台总览' },
    },
    {
      path: '/data-processing',
      name: 'data-processing',
      component: PlatformWorkbenchView,
      props: { initialTab: 'processing' },
      meta: { title: '数据处理' },
    },
    {
      path: '/graph-construction',
      name: 'graph-construction',
      component: PlatformWorkbenchView,
      props: { initialTab: 'construction' },
      meta: { title: '图谱构建' },
    },
    {
      path: '/graph-query',
      name: 'graph-query',
      component: PlatformWorkbenchView,
      props: { initialTab: 'query' },
      meta: { title: '图谱查询' },
    },
    {
      path: '/business-service',
      name: 'business-service',
      component: PlatformWorkbenchView,
      props: { initialTab: 'service' },
      meta: { title: '业务服务' },
    },
  ],
})
