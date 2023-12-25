from pymilvus import (
    connections, utility, Collection,
    CollectionSchema, FieldSchema, DataType
)

from pipeline import *
import docx2txt

from config import *


def create_collection(collection_name):
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT, alias="default")

    has_collection = utility.has_collection(collection_name)

    if has_collection:
        collection = Collection(collection_name)
        if DROP_EXIST:
            collection.drop()
        else:
            return collection

    # Create collection
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIM),
        FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=1000)
    ]
    schema = CollectionSchema(
        fields=fields,
        description="demo",
        enable_dynamic_field=True
    )
    collection = Collection(name=collection_name, schema=schema)

    # Change index here if you want to accelerate search

    index_params = {
        'metric_type': 'IP',
        'index_type': 'IVF_FLAT',
        'params': {'nlist': 1024}
    }
    collection.create_index(
        field_name='embedding',
        index_params=index_params
    )
    # connections.disconnect("default")

    return collection


def convert_file(file, filename, filetype):
    with open(filename, "wb") as file1:
        file1.write(file)
    if filetype == '.docx':
        text = docx2txt.process(filename)
        with open(filename, "w") as file1:
            file1.write(text)
    # TODO: add more filetype
