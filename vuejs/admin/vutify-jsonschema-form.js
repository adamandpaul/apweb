import Vue from 'vue'
import Draggable from 'vuedraggable'
import XVJsonschemaForm from './XVJsonschemaForm.vue'
import '@koumoul/vjsf/dist/main.css'

Vue.component('draggable', Draggable)
Vue.component('v-jsonschema-form', XVJsonschemaForm)
