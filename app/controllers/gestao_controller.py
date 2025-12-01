from sqlalchemy.orm import Session
from app.models.aluno import Aluno, MeusPagamentos
from app.models.professor import Professor
from app.models.estudio import Estudio
from app.models.relacionamentos.agenda import Agenda
from app.models.enums import StatusPagamento      


class GestaoController:

    @staticmethod
    def obter_dados_dashboard(db: Session):
        total_alunos = db.query(Aluno).count()
        total_professores = db.query(Professor).count()
        total_estudios = db.query(Estudio).count()
        total_agendas = db.query(Agenda).count()


        # pagamentos atrasados = status_pagamento == pendente
        pagamentos_atrasados = db.query(Aluno).filter(
            Aluno.status_pagamento == StatusPagamento.pendente
        ).count()


        return {
            "total_alunos": total_alunos,
            "total_professores": total_professores,
            "total_estudios": total_estudios,
            "pagamentos_atrasados": pagamentos_atrasados,
            "total_agendas": total_agendas
        }
    

