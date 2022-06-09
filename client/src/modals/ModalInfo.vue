<template>
    <b-modal :title="titleText" v-model="showModal"
        :hide-header-close=true :no-close-on-esc=true :no-close-on-backdrop=true
        size="md"
        id="modalInfo"
    >
        <div>
            {{bodyText}}
        </div>
        <template v-slot:modal-footer="{}" >
            <div class="w-100">
                <b-btn variant="primary" class="float-right" @click="closeModal">
                    Ok
                </b-btn>
            </div>
        </template>

    </b-modal>
</template>

<script>
    
    export default {
        name: 'ModalInfo',
        props: {
            showModal: Boolean,
            bodyText: String,
            titleText: String
        },
        methods: {
            closeModal(){
                this.$emit("close")
            }
        }
    }

</script>

