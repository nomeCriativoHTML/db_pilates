from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from datetime import date, datetime
from app.models.relacionamentos.agenda import Agenda
from app.schema.agenda import AgendaCreate, AgendaUpdate
from app.models.estudio import Estudio
from app.models.professor import Professor
from app.models.enums import Presenca
from app.models.relacionamentos.agendamentos import Agendamento





class AgendaController:
    @staticmethod
    def listar_agendas(db: Session):
        return db.query(Agenda).order_by(Agenda.data, Agenda.hora).all()

    @staticmethod
    def obter_agenda(db: Session, agenda_id: int):
        agenda = db.query(Agenda).filter(Agenda.id == agenda_id).first()
        if not agenda:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agenda não encontrada.")
        return agenda

    @staticmethod
    def criar_agenda(db: Session, dados: AgendaCreate):
        # valida estúdio existe
        estudio = db.query(Estudio).filter(Estudio.id == dados.estudio_id).first()
        if not estudio:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estúdio inválido.")

        # valida professor existe e está ativo
        professor = db.query(Professor).filter(Professor.id == dados.professor_id).first()
        if not professor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Professor inválido.")

        # valida motivo se bloqueado
        if dados.bloqueado and (dados.motivo_bloqueio is None or dados.motivo_bloqueio.strip() == ""):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Motivo obrigatório ao bloquear a aula.")
        
        

        # evita duplicidade: mesma estúdio, mesma data e hora
        existe = db.query(Agenda).filter(
            Agenda.estudio_id == dados.estudio_id,
            Agenda.data == dados.data,
            Agenda.hora == dados.hora
        ).first()
        if existe:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já existe uma aula nesse estúdio com essa data e hora.")

  
        # Convertendo string "HH:MM" para time
        hora_obj = dados.hora
        if isinstance(dados.hora, str):
            hora_obj = datetime.strptime(dados.hora, "%H:%M").time()

        nova = Agenda(
            estudio_id=dados.estudio_id,
            professor_id=dados.professor_id,
            substituto_id=dados.substituto_id,
            data=dados.data,
            hora=hora_obj,  # aqui
            tipo_aula=dados.tipo_aula,
            max_alunos=dados.max_alunos if dados.max_alunos else 3,
            status=dados.status,
            bloqueado=dados.bloqueado,
            motivo_bloqueio=dados.motivo_bloqueio
)


        db.add(nova)
        db.commit()
        db.refresh(nova)
        return nova

    @staticmethod
    def atualizar_agenda(db: Session, agenda_id: int, dados: AgendaUpdate):
        agenda = AgendaController.obter_agenda(db, agenda_id)

        update_data = dados.model_dump(exclude_unset=True)

        # se tentou bloquear agora, exige motivo
        if "bloqueado" in update_data and update_data.get("bloqueado") is True:
            motivo = update_data.get("motivo_bloqueio") or agenda.motivo_bloqueio
            if motivo is None or str(motivo).strip() == "":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Motivo obrigatório ao bloquear a aula.")

        # se alterou estúdio/data/hora, garantir não conflitar com outra agenda
        novo_estudio = update_data.get("estudio_id", agenda.estudio_id)
        nova_data = update_data.get("data", agenda.data)
        nova_hora = update_data.get("hora", agenda.hora)

        conflito = db.query(Agenda).filter(
            Agenda.id != agenda.id,
            Agenda.estudio_id == novo_estudio,
            Agenda.data == nova_data,
            Agenda.hora == nova_hora
        ).first()
        if conflito:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conflito: já existe outra aula nesse estúdio nessa data/hora.")

        for key, value in update_data.items():
            setattr(agenda, key, value)

        db.commit()
        db.refresh(agenda)
        return agenda
    
    @staticmethod
    def excluir_agenda(db: Session, agenda_id: int):
        agenda = AgendaController.obter_agenda(db, agenda_id)
        db.delete(agenda)
        db.commit()
        return {"mensagem": "Agenda removida com sucesso."}

    @staticmethod
    def bloquear_agenda(db: Session, agenda_id: int, motivo: str):
        agenda = AgendaController.obter_agenda(db, agenda_id)
        if not motivo or motivo.strip() == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Motivo obrigatório ao bloquear.")
        agenda.bloqueado = True
        agenda.motivo_bloqueio = motivo
        db.commit()
        db.refresh(agenda)
        return agenda

    @staticmethod
    def desbloquear_agenda(db: Session, agenda_id: int):
        agenda = AgendaController.obter_agenda(db, agenda_id)
        agenda.bloqueado = False
        agenda.motivo_bloqueio = None
        db.commit()
        db.refresh(agenda)
        return agenda


    @staticmethod
    def listar_agenda_do_dia(db: Session, professor_id: int):
        hoje = date.today()

        return (
            db.query(Agenda)
            .filter(Agenda.professor_id == professor_id)
            .filter(Agenda.data == hoje)
            .order_by(Agenda.hora.asc())
            .all()
        )
    
    

    @staticmethod
    def listar_proximas_aulas(db: Session, professor_id: int):
        hoje = date.today()
        dias_semana = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        proximas_aulas = (
            db.query(Agenda)
            .options(joinedload(Agenda.estudio))
            .filter(Agenda.professor_id == professor_id)
            .filter(Agenda.data > hoje)
            .order_by(Agenda.data.asc(), Agenda.hora.asc())
            .all()
        )

        for aula in proximas_aulas:
            aula.dia_semana = dias_semana[aula.data.strftime("%A")]

        return proximas_aulas



    @staticmethod
    def listar_aulas_professor(professor, db: Session):
        return db.query(Agenda).filter(
            Agenda.professor_id == professor.id
        ).all()

    @staticmethod
    def carregar_presencas(aula_id: int, db: Session):
        aula = db.query(Agenda).get(aula_id)

        if not aula:
            raise HTTPException(status_code=404, detail="Aula não encontrada")

        return {
            "aula": aula,
            "alunos": aula.agendamentos
        }

    @staticmethod
    def salvar_presencas(aula_id: int, presentes_ids: list[str], db: Session):

        agendamentos = db.query(Agendamento).filter(
            Agendamento.aula_id == aula_id
        ).all()

        for ag in agendamentos:
            if str(ag.id) in presentes_ids:
                ag.presenca = Presenca.presente
            else:
                ag.presenca = Presenca.ausente

        db.commit()
