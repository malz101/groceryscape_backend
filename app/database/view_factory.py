# The queries in this file are tailored to postgresql. If underlying
# database used needs to be changed, change the queries accordingly
# to match that databases syntax
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
from app.util.extensions import db

class CreateMaterializedView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


@compiler.compiles(CreateMaterializedView)
def compile(element, compiler, **kw):
    return f'Create MATERIALIZED VIEW {element.name} AS {compiler.sql_compiler.process(element.selectable, literal_binds=True)}'

def create_mat_view(name,selectable, metadata=db.metadata):
    temp_metadata = db.MetaData() #temp metadata just for initial Table object creation
    temp_table = db.Table(name, temp_metadata) #the actual mat view class is bound to db.metadata
    for c in selectable.c:
        temp_table.append_column(db.Column(c.name, c.type, primary_key=c.primary_key))
    
    #if no primary key is present, make all columns apart of the primary key
    if not (any([c.primary_key for c in selectable.c])):
        temp_table.append_constraint(PrimaryKeyConstraint(*[c.name for c in selectable.c]))
    
    db.event.listen(metadata, 'after_create', CreateMaterializedView(name, selectable))

    @db.event.listens_for(metadata, 'after_create')
    def create_indexes(target, connection, **kw):
        for idx in temp_table.indexes:
            idx.create(connection)
            
    db.event.listen(metadata, 'before_drop', db.DDL('DROP MATERIALIZED VIEW IF EXISTS ' + name))

    return temp_table


def refresh_mat_view(name, concurrently):
    # since session.execute() bypasses autoflush, must manually flush in order
    # to include newly-created/modified objects in the refresh
    db.session.flush()
    _con = 'CONCURRENTLY ' if concurrently else ''
    db.session.execute('REFRESH MATERIALIZED VIEW ' + _con + name)


def refresh_all_mat_views(concurrently=True):
    '''Refreshes all materialized views. Currently, views are refresh in
    non-deterministic order, so definitions can't depend on each other.'''
    mat_views = db.inspect(db.engine).get_view_names(include='materialized')
    for mat_view in mat_views:
        refresh_mat_view(mat_view, concurrently)


class MaterializedView(db.Model):
    __abstract__ = True

    @classmethod
    def refresh(cls, concurrently=True):
        '''Refreshes the current materialzed view'''
        refresh_mat_view(cls.__table__.fullname, concurrently)
    

