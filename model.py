from datetime import date


class Cliente:
    def __init__(self, nome, telefone, email, id_cliente):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id = id_cliente

    def __str__(self):
        return f"[{self.id}] {self.nome} - {self.telefone} - {self.email}"


class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero
        self.tipo = tipo
        self.preco_diaria = preco_diaria
        self.disponivel = True

    def verificar_disponibilidade(self):
        return self.disponivel

    def alterar_status(self):
        self.disponivel = not self.disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Ocupado"
        return f"Quarto {self.numero} ({self.tipo}) - R${self.preco_diaria}/dia - {status}"


class Reserva:
    def __init__(self, cliente, quarto, checkin: date, checkout: date):
        self.cliente = cliente
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.status = True  # Ativa
        dias = (checkout - checkin).days
        self.total = dias * quarto.preco_diaria if dias > 0 else quarto.preco_diaria

    def cancelar(self):
        self.status = False
        self.quarto.alterar_status()

    def __str__(self):
        return (
            f"Reserva de {self.cliente.nome} | Quarto {self.quarto.numero} "
            f"| {self.checkin} → {self.checkout} | Total: R${self.total} | "
            f"{'Ativa' if self.status else 'Cancelada'}"
        )


class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    # ---------- Clientes ----------
    def cadastrar_cliente(self, nome, telefone, email):
        id_cliente = len(self.clientes) + 1
        cliente = Cliente(nome, telefone, email, id_cliente)
        self.clientes.append(cliente)
        return cliente

    def listar_clientes(self):
        return self.clientes

    # ---------- Quartos ----------
    def adicionar_quarto(self, numero, tipo, preco_diaria):
        quarto = Quarto(numero, tipo, preco_diaria)
        self.quartos.append(quarto)
        return quarto

    def listar_quartos(self):
        return self.quartos

    def get_quarto(self, numero):
        for q in self.quartos:
            if q.numero == numero:
                return q
        return None

    # ---------- Reservas ----------
    def criar_reserva(self, id_cliente, numero_quarto, checkin: date, checkout: date):
        cliente = next((c for c in self.clientes if c.id == id_cliente), None)
        quarto = self.get_quarto(numero_quarto)
        if cliente and quarto and quarto.verificar_disponibilidade():
            reserva = Reserva(cliente, quarto, checkin, checkout)
            quarto.alterar_status()
            self.reservas.append(reserva)
            return reserva
        return None

    def cancelar_reserva(self, index):
        if 0 <= index < len(self.reservas):
            reserva = self.reservas[index]
            if reserva.status:
                reserva.cancelar()
                return True
        return False

    def listar_reservas(self):
        return self.reservas

 