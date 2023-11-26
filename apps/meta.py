class BaseOrderingMetaclass(type):
    def __new__(cls, cls_name, bases, cls_dict):
        meta = cls_dict.get('Meta')
        if meta and hasattr(meta, 'fields'):
            return tuple(meta.fields)
        return super().__new__(cls, cls_name, bases, cls_dict)
    
