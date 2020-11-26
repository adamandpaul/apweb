import Vue from 'vue'
import Draggable from 'vuedraggable'
import Swatches from 'vue-swatches'
import 'vue-swatches/dist/vue-swatches.min.css'
import XVJsonschemaForm from './XVJsonschemaForm.vue'
import '@koumoul/vjsf/dist/main.css'
import { Sketch } from 'vue-color'

Vue.component('swatches', Swatches)
Vue.component('draggable', Draggable)
Vue.component('color-picker', Sketch)
Vue.component('v-jsonschema-form', XVJsonschemaForm)
