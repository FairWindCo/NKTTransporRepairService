const fwproducts = {
    data() {
        return {
            view_category: true,
            count: 0,
            products: [],
            current_product_category: null,
            total_product:0,
            category_loading: true,
            category_selected: null,
            category: null,
            product_filters_model: {
                'name':{value: null, matchMode: primevue.api.FilterMatchMode.STARTS_WITH},
                'brand': {
                    operator: primevue.api.FilterOperator.AND,
                    constraints: [{value: null, matchMode: primevue.api.FilterMatchMode.STARTS_WITH}],
                    value: null
                },
            },
        }
    },
    methods: {
        onNodeSelect: function (leaf) {
            console.log('LEAF', leaf)
            this.getProducts(leaf)
            console.log('LEAF', leaf)

        },
        getProducts: function (current_category = null) {
            const current_level = current_category ? current_category.key : null
            this.current_product_category = current_category
            get_data(this, '/ajax_category_product', {
                category_id: current_level
                //main: main
            }, data => {
                console.log(data.list);
                this.products = data.list;
                this.total_product = data.count;

            })
        },
        getProductsEx: function (current_category = null, event) {
            const current_level = current_category ? current_category.key : null
            this.current_product_category = current_category
            first = event.first?event.first:0;
            rows = event.rows?event.rows:10;
            params = {
                category_id: current_level,
                page:Math.round(first / rows)+1,
                per_page: rows,
                view_filter:{
                    page:Math.round(first / rows)+1,
                    per_page: rows,
                    filters: event.filters,
                    sortField: event.sortField,
                    sortOrder: event.sortOrder,
                    multiSortMeta: event.multiSortMeta
                }
            }

            if(event.filters){
                for(current_filter_filed in event.filters){
                    const filter_define = event.filters[current_filter_filed];
                    if(filter_define && filter_define.value) {
                        console.log(current_filter_filed, filter_define.value, filter_define.matchMode)
                        params[current_filter_filed] = {
                            'value': filter_define.value,
                            'action': filter_define.matchMode
                        }
                    }
                }
            }
            if(event.sortField){
                console.log(event.sortField)
            }
            console.log(params);
            get_data(this, '/ajax_category_product', params, data => {
                console.log(data);
                this.products = data.list;
                this.total_product = data.count;

            })
        },
        getCategory: function (current_category = null) {
            this.category_loading = true;
            const current_level = current_category ? current_category.key : ''
            if (current_category && current_category.leaf !== undefined && current_category.leaf) {
                return
            }
            const main = !current_category
            post_data(this, '/ajax_category', {
                level: current_level
                //main: main
            }, data => {
                console.log(data.list);
                this.category_loading = false;
                if (current_category) {
                    current_category.children = data.list
                } else {
                    this.category = data.list
                }
            })
        },
        onPage(event) {
            console.log(event);
            this.getProductsEx(this.current_product_category, event)
        },
        onSorting(event) {
            this.getProductsEx(this.current_product_category, event)
        },
        onFilter(event) {
            this.getProductsEx(this.current_product_category, event)
        }
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
                            <p-tree :value="category" :loading="category_loading" selection-mode="single"
                             :selection-keys="category_selected"
                            @node-expand="getCategory" @node-select="onNodeSelect">
                                    <template #default="slotProps">
                                            {{slotProps.node.data}} <b>{{slotProps.node.label}}</b>
                                    </template>              
                            </p-tree>
                        </div>
                        <div :class="{'col-9': view_category,
                 'col-12': !view_category}">
                            <p-datatable :value="products" :paginator="true" :rows="10"
                            :total-records="total_product"
                            sort-mode="multiple"  
                            :rows-per-page-options="[10,20,50]" responsive-layout="scroll"
                            filter-display="row" :lazy="true" ref="dt"
                            @page="onPage($event)" @sort="onSorting($event)" @filter="onFilter($event)"
                            v-model:filters="product_filters_model"
                            :global-filter-fields="['name']"
                            >
                <template #empty>
                    Продекты не найдены
                </template>
                <template #loading>
                    Loading data. Please wait.
                </template>                            
                                <p-column field="name" header="Name" ref="name" :sortable="true">
                    <template #filter="{filterModel,filterCallback}">
                        <p-inputtext type="text" v-model="filterModel.value"
                        class="p-column-filter" :placeholder="\`Search by name - \`"  
                       >
                        
                        </p-inputtext>                                                
                    </template>                             
</p-column>
                                <p-column field="code" header="1C Code" :sortable="true"></p-column>
                                <p-column field="vendor_code" header="Vendor Code"></p-column>
                                <p-column field="brand_id" header="Brand"></p-column>
                            </p-datatable>
                        </div>
                    </div>           
        </template>
    </p-card>
</div>        
`
}