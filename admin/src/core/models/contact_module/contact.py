from src.core.database import db
from datetime import datetime
import enum


class QueryState(enum.Enum):
    """Represent the state of a query. It can be: \n
        Creada --> The query has been created a sended \n
        Pendiente --> The query its being processed \n
        Atendida --> The query has been attended"""
    Creada = "Creada"
    Pendiente = "Pendiente"
    Atendida = "Atendida"


class PortalQuery(db.Model):
    """A portal query that has been created in the portal by a client"""
    __tablename__ = "Consulta"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    comentario = db.Column(db.String, nullable=True)
    estado = db.Column(db.Enum(QueryState), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    closed_at = db.Column(db.DateTime, nullable=False)
    borrado = db.Column(db.Boolean, nullable=True, default=False)

    @classmethod
    def create_query(cls, **kwargs):
        """
        Add a portal query by sending the parameters and types below:
            titulo: String 
            email: String
            descripcion: String
            estado: String
            created_at: String of a Date
            closed_at: String of a Date
        Finally, returns the portal query if the Dates are in a valid format, otherwhise, a
        dictionary with the errors.
        """
        errors = {}
        try:
            created_at = datetime.strptime(
                kwargs.get("created_at"), "%Y-%m-%d").date()
        except ValueError as e:
            errors.update(
                "La fecha de creación no se encuentra en un formato valido")

        try:
            closed_at = datetime.strptime(
                kwargs.get("closed_at"), "%Y-%m-%d").date()
        except ValueError as e:
            errors.update(
                "La fecha de terminación no se encuentra en un formato valido")

        if not errors:
            query = cls(**kwargs)
            db.session.add(query)
            db.session.commit()

            return {"portal_query": query, "info": errors}
        else:
            return {"portal_query": None, "info": errors}
        
    
    @classmethod
    def get_query(cls, id: int):
        """Gets a portal query by an id if exists"""
        return cls.query.filter_by(borrado=False).filter(cls.id == id).first()
    
    
    def update_query(self, state: str = None, comentary: str = None):
        """Updates a query with the state and comentary sended"""
        info = []
        
        if state and self.estado != state:
            self.estado = state
            self.closed_at = datetime.now()
            info.append(f'Se ha actualizado el estado de la consulta a {state}')
        
        if comentary and self.comentario != comentary:
            self.comentario = comentary
            info.append(f'Se ha actualizado el comentario de la consulta a "{comentary}"')
        
        if info == []:
            info.append("No se ha actualizado la consulta")
        else:
            db.session.commit()
            
        return info
            
    @classmethod
    def delete_query(cls, id: int):
        """Deletes the query logically"""
        query = cls.get_query(id)
        query.closed_at = datetime.now()
        query.borrado = True
        db.session.commit()
            
