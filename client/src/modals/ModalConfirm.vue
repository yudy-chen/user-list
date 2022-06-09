<template>
    <b-modal :title="titleText" v-model="showModal"
        :hide-header-close=true :no-close-on-esc=true :no-close-on-backdrop=true
        size="md"
        id="modalConfirm"
    >
        <div>
            {{bodyText}}
        </div>
        <template v-slot:modal-footer="{}" >
            <div class="w-100">
                <b-btn variant="secondary" @click="cancelModal">
                    Cancel
                </b-btn>
                <b-btn variant="primary" class="float-right" @click="okModal">
                    Ok
                </b-btn>
            </div>
        </template>

    </b-modal>
</template>

<script>
    
    export default {
        name: 'ModalConfirm',
        props: {
            showModal: Boolean,
            bodyText: String,
            titleText: String,
            confirmedTopic: String
        },
        methods: {
            cancelModal(){
                this.$emit("cancel")
            },
            okModal(){
                this.$emit("ok", this.confirmedTopic)
            }
        }
    }

</script>

