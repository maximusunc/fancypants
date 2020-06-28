<template>
  <div v-if="player.length">
    <vue-json-editor
        id="json_view"
        v-model="player_json"
        :show-btns="true"
        @json-save="encode"
    ></vue-json-editor>
  </div>
</template>
 
<script>
    import vueJsonEditor from 'vue-json-editor';
    import axios from 'axios';
    import _ from 'lodash';
 
    export default {
        props: {
            player: Array,
            player_id: String,
        },
        computed: {
            player_json: {
                get: function() { return _.cloneDeep(this.player); },
                set: function(value) { this.player_json = value; }
            }
        },
        components: {
            vueJsonEditor
        },
        methods: {
            encode() {
                axios.post(`http://0.0.0.0:5748/encode/${this.player_id}`, this.player_copy)
                    .then(() => {
                        console.log('Success');
                    })
            }
        }
    }
</script>

<style>
    #json_view {
        margin-top: 20px;
    }
</style>
