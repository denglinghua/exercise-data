<template>
  <q-page>
    <div class="fullscreen q-pa-xs flex flex-center">
      <q-input v-model="id" label="悦跑圈ID" type="number" @keyup.enter="goDataPage" style="width:200px" autofocus
        bottom-slots>
        <template v-slot:append>
          <q-icon name="arrow_forward" size="md" color="primary" @click="goDataPage" />
        </template>
        <template v-slot:hint>
          <q-icon class="q-mr-md" color="grey-6" size="1.2em" name="help_outline">
            <q-tooltip>
              悦跑圈APP“我”页面可以查看复制ID
            </q-tooltip>
          </q-icon>
        </template>
      </q-input>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const $router = useRouter()

const defaultId = process.env.DEV ? '86288420' : ''
const id = ref(defaultId)

function goDataPage() {
  if (!id.value) return
  $router.push({ name: 'data', params: { id: id.value } })
}
</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
</style>
