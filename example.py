from brasil import BrasilIO


api = BrasilIO()

# List all datasets, its tables and data URL for each one
for dataset in api.datasets():
    dataset_data = api.dataset(dataset['slug'])
    print(dataset['slug'])
    for table in dataset_data['tables']:
        print(f"  {table['name']}: {table['data_url']}")


# Filter and search into table data
results = api.dataset_table_data(
    'documentos-brasil', 'documents',  # dataset slug and table name
    document_type='CPF',  # filters, like in the Web interface (optional)
    search='jair bolsonaro',  # full-text search (optional)
)
for result in results:  # pagination is handled automatically
    print(result)  # each result is a dict
