<template>
    <label class="text-reader">
        <input
            type='text'
            v-model="player_id"
            placeholder="Player Id"
        />
        <br />
        <button @click="decode">Decode</button>
    </label>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'DecodePlayer',
        data: () => ({
            player_id: '',
        }),
        methods: {
            decode() {
                axios.get(`http://0.0.0.0:5748/decode/${this.player_id}`)
                    .then((res) => {
                        this.$emit('player', res.data);
                        this.$emit('player_id', this.player_id);
                        this.player_id = '';
                    });
            }
        }
    };
</script>

<style scoped>
    input {
        display: block;
        margin: auto;
    }
    button {
        padding: 10px;
        border: 1px solid grey;
        border-radius: 10px;
    }
</style>