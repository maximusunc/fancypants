<template>
    <div id="app">
        <decode-player
            @player="displayPlayer"
            @player_id="setPlayerId"
        />
        <div v-if="player.length">
            <vue-json-editor
                id="json_view"
                v-model="player"
                :show-btns="true"
                @json-save="encode"
            ></vue-json-editor>
        </div>
    </div>
</template>

<script>
    import vueJsonEditor from 'vue-json-editor';
    import axios from 'axios';
    import DecodePlayer from './components/DecodePlayer.vue';

    export default {
        name: 'App',
        data() {
            return {
                player: [],
                player_id: null,
            }
        },
        components: {
            DecodePlayer,
            vueJsonEditor,
        },
        methods: {
            displayPlayer(player) {
                console.log('player', player);
                this.player = player;
            },
            setPlayerId(id) {
                this.player_id = id;
            },
            encode() {
                axios.post(`http://0.0.0.0:5748/encode/${this.player_id}`, this.player)
                    .then(() => {
                        console.log('Success');
                    })
            }
        }
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
    #json_view {
        margin-top: 20px;
    }
</style>
