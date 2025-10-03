import flet as ft
from datetime import date
from model import GerenciadorDeReservas

gerenciador = GerenciadorDeReservas()

# ---------- CORES ----------
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#E8F5E9"
INPUT_BG = "#1E1E1E"
TEXT_COLOR = "#E8F5E9" 


def main(page: ft.Page):
    page.title = "Gerenciador de Reservas"
    page.window_width = 600
    page.window_height = 700
    page.bgcolor = SECONDARY_COLOR

    # ---------- TELAS ----------
    def tela_inicial():
        page.views.clear()
        lista_quartos = ft.Column(
            controls=[
                ft.Card(
                    content=ft.Container(
                        ft.Text(str(q), size=16, color=TEXT_COLOR),
                        padding=10,
                    ),
                    elevation=2,
                )
                for q in gerenciador.listar_quartos()
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        page.views.append(
            ft.View(
                "/",
                [
                    ft.Text("\U0001F3E8 Quartos", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    lista_quartos,
                    ft.Divider(),
                    ft.Row(
                        [
                            ft.ElevatedButton("Gerenciar Clientes", icon="people", bgcolor=PRIMARY_COLOR, color="white", expand=True, on_click=lambda e: tela_clientes()),
                            ft.ElevatedButton("Adicionar Quarto", icon="hotel", bgcolor=PRIMARY_COLOR, color="white", expand=True, on_click=lambda e: tela_quartos()),
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("Criar Reserva", icon="add_box", bgcolor=PRIMARY_COLOR, color="white", expand=True, on_click=lambda e: tela_reservas()),
                            ft.ElevatedButton("Ver Reservas", icon="list", bgcolor=PRIMARY_COLOR, color="white", expand=True, on_click=lambda e: tela_lista_reservas()),
                        ],
                        spacing=10,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                padding=20,
            )
        )
        page.update()

    def tela_clientes():
        page.views.clear()
        nome = ft.TextField(label="Nome", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        email = ft.TextField(label="Email", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        tel = ft.TextField(label="Telefone", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)

        lista_clientes = ft.Column(
            controls=[
                ft.Card(content=ft.Container(ft.Text(str(c), color=TEXT_COLOR), padding=10), elevation=1)
                for c in gerenciador.listar_clientes()
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        def adicionar_cliente(e):
            if nome.value and email.value and tel.value:
                gerenciador.cadastrar_cliente(nome.value, tel.value, email.value)
                lista_clientes.controls = [
                    ft.Card(content=ft.Container(ft.Text(str(c), color=TEXT_COLOR), padding=10), elevation=1)
                    for c in gerenciador.listar_clientes()
                ]
                nome.value, email.value, tel.value = "", "", ""
                page.update()

        page.views.append(
            ft.View(
                "/clientes",
                [
                    ft.Text("\U0001F465 Gerenciar Clientes", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    lista_clientes,
                    ft.Divider(),
                    nome, email, tel,
                    ft.ElevatedButton("Adicionar Cliente", icon="person_add", bgcolor=PRIMARY_COLOR, color="white", on_click=adicionar_cliente),
                    ft.TextButton("⬅ Voltar", on_click=lambda e: tela_inicial()),
                ],
                padding=20,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        page.update()

    def tela_quartos():
        page.views.clear()
        numero = ft.TextField(label="Número do quarto", keyboard_type=ft.KeyboardType.NUMBER, bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        tipo = ft.TextField(label="Tipo (single, double, suite)", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        preco = ft.TextField(label="Preço por diária", keyboard_type=ft.KeyboardType.NUMBER, bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        mensagem = ft.Text("", color=TEXT_COLOR)

        lista_quartos = ft.Column(
            controls=[
                ft.Card(content=ft.Container(ft.Text(str(q), color=TEXT_COLOR), padding=10), elevation=1)
                for q in gerenciador.listar_quartos()
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        def adicionar_quarto(e):
            tipos_validos = ["single", "double", "suite"]
            if numero.value and tipo.value and preco.value:
                if tipo.value.lower() not in tipos_validos:
                    mensagem.value = "\u274C Tipo de quarto inválido! Dígite: single, double ou suite."
                    mensagem.color = "red"
                    page.update()
                    return 
            
                gerenciador.adicionar_quarto(int(numero.value), tipo.value.lower(), float(preco.value))
                lista_quartos.controls = [
                    ft.Card(
                        content=ft.Container(ft.Text(str(q), color=TEXT_COLOR), padding=10),
                        elevation=1
                    )
                    for q in gerenciador.listar_quartos()
                ]
                numero.value, tipo.value, preco.value = "", "", ""
                mensagem.value = "\u2705 Quarto adicionado com sucesso!"
                mensagem.color = "green"
                page.update()

        page.views.append(
            ft.View(
                "/quartos",
                [
                    ft.Text("\U0001F6CF Adicionar Quartos", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    lista_quartos,
                    ft.Divider(),
                    numero, tipo, preco,
                    ft.ElevatedButton("Adicionar Quarto", icon="hotel", bgcolor=PRIMARY_COLOR, color="white", on_click=adicionar_quarto),
                    mensagem,
                    ft.TextButton("⬅ Voltar", on_click=lambda e: tela_inicial()),
                ],
                padding=20,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        page.update()

    def tela_reservas():
        page.views.clear()
        clientes_dropdown = ft.Dropdown(
            label="Selecione o Cliente",
            options=[ft.dropdown.Option(c.id, c.nome) for c in gerenciador.clientes],
            bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR,
        )
        quartos_dropdown = ft.Dropdown(
            label="Selecione o Quarto",
            options=[ft.dropdown.Option(q.numero, f"{q.numero} ({'Disponível' if q.disponivel else 'Ocupado'})") for q in gerenciador.quartos],
            bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR,
        )
        checkin = ft.TextField(label="Data Check-in (AAAA-MM-DD)", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        checkout = ft.TextField(label="Data Check-out (AAAA-MM-DD)", bgcolor=INPUT_BG, border_color=PRIMARY_COLOR, color=TEXT_COLOR)
        mensagem = ft.Text("", color=TEXT_COLOR)

        def confirmar_reserva(e):
            try:
                if clientes_dropdown.value and quartos_dropdown.value and checkin.value and checkout.value:
                    checkin_date = date.fromisoformat(checkin.value)
                    checkout_date = date.fromisoformat(checkout.value)
                    reserva = gerenciador.criar_reserva(int(clientes_dropdown.value), int(quartos_dropdown.value), checkin_date, checkout_date)
                    if reserva:
                        mensagem.value = "\u2705 Reserva criada com sucesso!"
                        mensagem.color = "green"
                    else:
                        mensagem.value = "\u274C Erro: quarto indisponível ou cliente inválido."
                        mensagem.color = "red"
            except Exception as err:
                mensagem.value = f"Erro: {err}"
                mensagem.color = "red"
            page.update()

        page.views.append(
            ft.View(
                "/reservas",
                [
                    ft.Text("\U0001F4DD Criar Reserva", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    clientes_dropdown,
                    quartos_dropdown,
                    checkin,
                    checkout,
                    ft.ElevatedButton("Confirmar Reserva", icon="check_circle", bgcolor=PRIMARY_COLOR, color="white", on_click=confirmar_reserva),
                    mensagem,
                    ft.TextButton("⬅ Voltar", on_click=lambda e: tela_inicial()),
                ],
                padding=20,
            )
        )
        page.update()

    def tela_lista_reservas():
        page.views.clear()
        if gerenciador.reservas:
            lista = ft.Column(
                controls=[
                    ft.Card(
                        content=ft.Row(
                            [
                                ft.Text(str(r), expand=True, color=TEXT_COLOR),
                                ft.IconButton(icon="delete", icon_color="red", on_click=lambda e, i=i: cancelar(i)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        elevation=2,
                    )
                    for i, r in enumerate(gerenciador.reservas)
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        else:
            lista = ft.Text("Nenhuma reserva encontrada.", size=16, italic=True, color=TEXT_COLOR)

        def cancelar(index):
            gerenciador.cancelar_reserva(index)
            tela_lista_reservas()

        page.views.append(
            ft.View(
                "/lista_reservas",
                [
                    ft.Text("\U0001F4CB Reservas", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    lista,
                    ft.TextButton("⬅ Voltar", on_click=lambda e: tela_inicial()),
                ],
                padding=20,
            )
        )
        page.update()

    
    tela_inicial()


if __name__ == "__main__":
    ft.app(target=main)


