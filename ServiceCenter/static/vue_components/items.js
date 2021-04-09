const fwitems = {
    data() {
        return {
            count: 0,
            cars:[
                {"brand": "Volkswagen", "year": 2012, "color": "Orange", "vin": "dsad231ff"},
        {"brand": "Audi", "year": 2011, "color": "Black", "vin": "gwregre345"},
            ],
        }
    },
    template: `
<div class="p-grid">
    <p-card class="p-col-12">
        <template #title>
            Advanced Card <p-button label="Primary"  v-on:click="count++">You clicked me {{ count }} times.</p-button>
        </template>    
        <template #content>
test table            
<p-datatable :value="cars">
    <p-column field="vin" header="Vin"></p-column>
    <p-column field="year" header="Year"></p-column>
    <p-column field="brand" header="Brand"></p-column>
    <p-column field="color" header="Color"></p-column>
</p-datatable>
        </template>
    </p-card>
</div>        
`
}