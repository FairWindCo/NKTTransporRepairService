const fwproducts = {
    data() {
        return {
            view_category: true,
            count: 0,
            cars: [
                {"brand": "Volkswagen", "year": 2012, "color": "Orange", "vin": "dsad231ff"},
                {"brand": "Audi", "year": 2011, "color": "Black", "vin": "gwregre345"},
            ],
            category_loading: true,
            category: null,
        }
    },
    methods: {
        getCategory: function (current_category = null) {
            this.category_loading = true;
            const current_level = current_category ? current_category.id : null
            const main =  !current_category
            get_data(this, '/ajax_category', {level: current_level, main: main}, data => {
                console.log(data.data_list);
                this.category_loading = false;
                this.category = data.data_list
            })
        },
    },
    mounted() {
        this.getCategory();
    },
    template: `
<div class="p-grid">
    <p-card class="p-col-12">
        <template #title>
            <div class="p-grid">
                <div class="col-12">Справочник товаров и категорий</div>
                <div :class="{
                    'col-3':view_category,
                    'fw-layout':true
                    }">
                <span v-if="view_category">Категории</span>                
                <a class="fw-layout-menu-button p-shadow-6 p-ripple" @click="view_category=!view_category">
                    <i :class="{
                    pi:true,
                    'pi-chevron-left': view_category,
                    'pi-chevron-right': !view_category,
                    }"></i>
                    <span class="p-ink" style="height: 35px; width: 35px; top: -3px; left: -4px;"></span>
                 </a></div>
                <div :class="{
                 'col-9': view_category,
                 'col-11': !view_category,
                 'fw-layout-right':true
                }">Товары</div>
            </div>
        </template>    
        <template #content>
                    <div class="p-grid">
                        <div class="col-3" v-if="view_category">
                            <p-tree :value="category" @nodeExpand="getCategory" :loading="category_loading" label="name" key="id">
                                    <template #default="slotProps">
                                            <b>{{slotProps.node.label}}</b>
                                    </template>              
                            </p-tree>
                        </div>
                        <div :class="{'col-9': view_category,
                 'col-12': !view_category}">
                            <p-datatable :value="cars">
                                <p-column field="vin" header="Vin"></p-column>
                                <p-column field="year" header="Year"></p-column>
                                <p-column field="brand" header="Brand"></p-column>
                                <p-column field="color" header="Color"></p-column>
                            </p-datatable>
                        </div>
                    </div>           
        </template>
    </p-card>
</div>        
`
}