import customtkinter as ctk
from tkinter import messagebox

from src.services.sistema import SistemaOcorrencias
from src.models.ocorrencia import Ocorrencia


class OccurrenceSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("Sistema de Ocorrências")
        self.after(100, lambda: self.state('zoomed'))

        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Cores pastéis
        self.colors = {
            'bg_gradient': '#dbeafe',  # blue-100
            'white': '#ffffff',
            'blue_pastel': '#93c5fd',  # blue-300
            'blue_dark': '#1e3a8a',  # blue-900
            'green_pastel': '#86efac',  # green-300
            'green_dark': '#14532d',  # green-900
            'yellow_pastel': '#fcd34d',  # yellow-300
            'yellow_dark': '#7c2d12',  # yellow-900
            'gray_light': '#f3f4f6',  # gray-100
            'gray_text': '#6b7280',  # gray-500
            'blue_light': '#eff6ff',  # blue-50
            'green_light': '#f0fdf4',  # green-50
            'yellow_light': '#fef3c7',  # yellow-100
            'red_light': '#fee2e2',  # red-100
            'red_text': '#dc2626'  # red-600
        }

        # Lista de ocorrências
        self.sistema = SistemaOcorrencias()

        self.active_tab = 'aberta'  # 'aberta', 'em andamento' ou 'resolvida'
        self.equipamentos_window = None
        self.equipamentos_lista_frame = None
        self.equipamento_editando_id = None
        self.equipamento_combo = None
        self.equipamento_combo_map = {}

        self.configure(fg_color=self.colors['bg_gradient'])
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.create_header()

        # Stats
        self.create_stats()

        # Container principal
        main_container = ctk.CTkFrame(self, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=40, pady=20)

        # Grid layout
        main_container.grid_columnconfigure(0, weight=1, uniform='col')
        main_container.grid_columnconfigure(1, weight=2, uniform='col')
        main_container.grid_rowconfigure(0, weight=1)

        # Formulário (lado esquerdo)
        self.create_form(main_container)

        # Lista de ocorrências (lado direito)
        self.create_occurrence_list(main_container)

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=self.colors['white'],
                                    corner_radius=0, height=100)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)

        content = ctk.CTkFrame(header_frame, fg_color='transparent')
        content.pack(pady=20, padx=40)

        actions = ctk.CTkFrame(content, fg_color='transparent')
        actions.pack(side='right')

        reload_btn = ctk.CTkButton(actions,
                                   text='↻ Recarregar dados',
                                   height=36,
                                   corner_radius=10,
                                   fg_color=self.colors['gray_light'],
                                   text_color=self.colors['blue_dark'],
                                   hover_color='#e5e7eb',
                                   command=self.reload_data)
        reload_btn.pack(side='left', padx=(0, 10))

        equipamentos_btn = ctk.CTkButton(actions,
                                          text='Equipamentos',
                                          height=36,
                                          corner_radius=10,
                                          fg_color=self.colors['blue_pastel'],
                                          text_color=self.colors['blue_dark'],
                                          hover_color='#7dd3fc',
                                          command=self.open_equipamentos_window)
        equipamentos_btn.pack(side='left')

        # Título
        titulo = ctk.CTkLabel(content,
                              text="Sistema de Ocorrências",
                              font=ctk.CTkFont(size=34, weight='bold'),
                              text_color=self.colors['blue_dark'])
        titulo.pack(side='left', padx=10)

    def create_stats(self):
        stats_frame = ctk.CTkFrame(self, fg_color='transparent')
        stats_frame.pack(fill='x', padx=40, pady=20)
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)

        self.stats_frame = stats_frame

        aberta_count = self._count_by_status('aberta')
        andamento_count = self._count_by_status('em andamento')
        resolvida_count = self._count_by_status('resolvida')

        # Card Abertas
        aberta_card = ctk.CTkFrame(stats_frame, fg_color=self.colors['blue_pastel'],
                                   corner_radius=20, height=120)
        aberta_card.grid(row=0, column=0, padx=10, sticky='ew')
        aberta_card.pack_propagate(False)

        aberta_label = ctk.CTkLabel(aberta_card, text="Abertas",
                                    font=ctk.CTkFont(size=12),
                                    text_color=self.colors['blue_dark'])
        aberta_label.pack(anchor='w', padx=20, pady=(20, 5))

        aberta_number = ctk.CTkLabel(aberta_card, text=str(aberta_count),
                                     font=ctk.CTkFont(size=48, weight='bold'),
                                     text_color=self.colors['blue_dark'])
        aberta_number.pack(anchor='w', padx=20)
        self.aberta_number_label = aberta_number

        # Card Em Andamento
        andamento_card = ctk.CTkFrame(stats_frame, fg_color=self.colors['yellow_pastel'],
                                      corner_radius=20, height=120)
        andamento_card.grid(row=0, column=1, padx=10, sticky='ew')
        andamento_card.pack_propagate(False)

        andamento_label = ctk.CTkLabel(andamento_card, text="Em Andamento",
                                       font=ctk.CTkFont(size=12),
                                       text_color=self.colors['yellow_dark'])
        andamento_label.pack(anchor='w', padx=20, pady=(20, 5))

        andamento_number = ctk.CTkLabel(andamento_card, text=str(andamento_count),
                                        font=ctk.CTkFont(size=48, weight='bold'),
                                        text_color=self.colors['yellow_dark'])
        andamento_number.pack(anchor='w', padx=20)
        self.andamento_number_label = andamento_number

        # Card Resolvidas
        resolvida_card = ctk.CTkFrame(stats_frame, fg_color=self.colors['green_pastel'],
                                      corner_radius=20, height=120)
        resolvida_card.grid(row=0, column=2, padx=10, sticky='ew')
        resolvida_card.pack_propagate(False)

        resolvida_label = ctk.CTkLabel(resolvida_card, text="Resolvidas",
                                       font=ctk.CTkFont(size=12),
                                       text_color=self.colors['green_dark'])
        resolvida_label.pack(anchor='w', padx=20, pady=(20, 5))

        resolvida_number = ctk.CTkLabel(resolvida_card, text=str(resolvida_count),
                                        font=ctk.CTkFont(size=48, weight='bold'),
                                        text_color=self.colors['green_dark'])
        resolvida_number.pack(anchor='w', padx=20)
        self.resolvida_number_label = resolvida_number

    def create_form(self, parent):
        form_frame = ctk.CTkScrollableFrame(parent, fg_color=self.colors['white'],
                                  corner_radius=20)
        form_frame.grid(row=0, column=0, padx=10, sticky='nsew')

        # Título do formulário
        form_titulo = ctk.CTkLabel(form_frame, text="Nova Ocorrência",
                                   font=ctk.CTkFont(size=18, weight='bold'),
                                   text_color=self.colors['blue_dark'])
        form_titulo.pack(pady=(20, 10), padx=20, anchor='w')

        # Campo Título
        titulo_label = ctk.CTkLabel(form_frame, text="Título",
                                    font=ctk.CTkFont(size=12),
                                    text_color=self.colors['gray_text'])
        titulo_label.pack(pady=(10, 5), padx=20, anchor='w')

        self.titulo_entry = ctk.CTkEntry(form_frame,
                                         placeholder_text="Digite o título da ocorrência",
                                         height=40,
                                         corner_radius=10,
                                         border_color=self.colors['blue_pastel'])
        self.titulo_entry.pack(pady=(0, 15), padx=20, fill='x')

        # Campo Descrição
        desc_label = ctk.CTkLabel(form_frame, text="Descrição",
                                  font=ctk.CTkFont(size=12),
                                  text_color=self.colors['gray_text'])
        desc_label.pack(pady=(0, 5), padx=20, anchor='w')

        self.desc_text = ctk.CTkTextbox(form_frame, height=200,
                                        corner_radius=10,
                                        border_color=self.colors['blue_pastel'])
        self.desc_text.pack(pady=(0, 15), padx=20, fill='x')

        equipamento_label = ctk.CTkLabel(form_frame, text="Equipamento vinculado",
                         font=ctk.CTkFont(size=12),
                         text_color=self.colors['gray_text'])
        equipamento_label.pack(pady=(0, 5), padx=20, anchor='w')

        self.equipamento_combo = ctk.CTkComboBox(form_frame,
                             values=['Nenhum equipamento'],
                             height=40,
                             corner_radius=10,
                             button_color=self.colors['blue_pastel'],
                             button_hover_color='#7dd3fc')
        self.equipamento_combo.pack(pady=(0, 15), padx=20, fill='x')
        self.equipamento_combo.set('Nenhum equipamento')

        equipamento_btn = ctk.CTkButton(form_frame,
                        text="Gerenciar Equipamentos",
                        height=36,
                        corner_radius=10,
                        fg_color=self.colors['gray_light'],
                        text_color=self.colors['blue_dark'],
                        hover_color='#e5e7eb',
                        command=self.open_equipamentos_window)
        equipamento_btn.pack(pady=(0, 15), padx=20, fill='x')

        # Botão Registrar
        register_btn = ctk.CTkButton(form_frame,
                                     text="Registrar Ocorrência",
                                     height=40,
                                     corner_radius=10,
                                     fg_color=self.colors['blue_pastel'],
                                     text_color=self.colors['blue_dark'],
                                     hover_color='#7dd3fc',
                                     font=ctk.CTkFont(size=14, weight='bold'),
                                     command=self.add_occurrence)
        register_btn.pack(pady=(0, 20), padx=20, fill='x')

        self._refresh_equipamento_combo()

    def create_occurrence_list(self, parent):
        list_frame = ctk.CTkFrame(parent, fg_color=self.colors['white'],
                                  corner_radius=20)
        list_frame.grid(row=0, column=1, padx=10, sticky='nsew')

        # Tabs
        tabs_frame = ctk.CTkFrame(list_frame, fg_color='transparent')
        tabs_frame.pack(fill='x', padx=20, pady=20)

        tabs_frame.grid_columnconfigure(0, weight=1)
        tabs_frame.grid_columnconfigure(1, weight=1)
        tabs_frame.grid_columnconfigure(2, weight=1)

        self.aberta_tab_btn = ctk.CTkButton(tabs_frame,
                                            text="Abertas",
                                            height=40,
                                            corner_radius=10,
                                            fg_color=self.colors['blue_pastel'],
                                            text_color=self.colors['blue_dark'],
                                            hover_color='#7dd3fc',
                                            font=ctk.CTkFont(size=12, weight='bold'),
                                            command=lambda: self.switch_tab('aberta'))
        self.aberta_tab_btn.grid(row=0, column=0, padx=5, sticky='ew')

        self.andamento_tab_btn = ctk.CTkButton(tabs_frame,
                                               text="Em Andamento",
                                               height=40,
                                               corner_radius=10,
                                               fg_color=self.colors['yellow_light'],
                                               text_color=self.colors['gray_text'],
                                               hover_color='#fef3c7',
                                               font=ctk.CTkFont(size=12),
                                               command=lambda: self.switch_tab('em andamento'))
        self.andamento_tab_btn.grid(row=0, column=1, padx=5, sticky='ew')

        self.resolvida_tab_btn = ctk.CTkButton(tabs_frame,
                                               text="Resolvidas",
                                               height=40,
                                               corner_radius=10,
                                               fg_color=self.colors['green_light'],
                                               text_color=self.colors['gray_text'],
                                               hover_color='#dcfce7',
                                               font=ctk.CTkFont(size=12),
                                               command=lambda: self.switch_tab('resolvida'))
        self.resolvida_tab_btn.grid(row=0, column=2, padx=5, sticky='ew')

        # Scrollable frame para lista
        self.scrollable_frame = ctk.CTkScrollableFrame(list_frame,
                                                       fg_color='transparent')
        self.scrollable_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        self.update_list()

    def switch_tab(self, tab: str):
        self.active_tab = tab

        if tab == 'aberta':
            self.aberta_tab_btn.configure(fg_color=self.colors['blue_pastel'],
                                          text_color=self.colors['blue_dark'],
                                          font=ctk.CTkFont(size=12, weight='bold'))
            self.andamento_tab_btn.configure(fg_color=self.colors['yellow_light'],
                                             text_color=self.colors['gray_text'],
                                             font=ctk.CTkFont(size=12))
            self.resolvida_tab_btn.configure(fg_color=self.colors['green_light'],
                                             text_color=self.colors['gray_text'],
                                             font=ctk.CTkFont(size=12))
        elif tab == 'em andamento':
            self.aberta_tab_btn.configure(fg_color=self.colors['blue_light'],
                                          text_color=self.colors['gray_text'],
                                          font=ctk.CTkFont(size=12))
            self.andamento_tab_btn.configure(fg_color=self.colors['yellow_pastel'],
                                             text_color=self.colors['yellow_dark'],
                                             font=ctk.CTkFont(size=12, weight='bold'))
            self.resolvida_tab_btn.configure(fg_color=self.colors['green_light'],
                                             text_color=self.colors['gray_text'],
                                             font=ctk.CTkFont(size=12))
        else:
            self.aberta_tab_btn.configure(fg_color=self.colors['blue_light'],
                                          text_color=self.colors['gray_text'],
                                          font=ctk.CTkFont(size=12))
            self.andamento_tab_btn.configure(fg_color=self.colors['yellow_light'],
                                             text_color=self.colors['gray_text'],
                                             font=ctk.CTkFont(size=12))
            self.resolvida_tab_btn.configure(fg_color=self.colors['green_pastel'],
                                             text_color=self.colors['green_dark'],
                                             font=ctk.CTkFont(size=12, weight='bold'))

        self.update_list()

    def update_list(self):
        # Limpar lista atual
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Exibe só o status da aba ativa para manter a tela organizada.
        filtered = [
            o for o in self.sistema.ocorrencias
            if o.status == self.active_tab
        ]

        if not filtered:
            empty_label = ctk.CTkLabel(self.scrollable_frame,
                                       text="Nenhuma ocorrência neste status",
                                       font=ctk.CTkFont(size=14),
                                       text_color=self.colors['gray_text'])
            empty_label.pack(pady=50)
            return

        # Criar cards de ocorrências
        for occ in filtered:
            self.create_occurrence_card(occ)

        # Atualizar contadores nos tabs
        aberta_count = self._count_by_status('aberta')
        andamento_count = self._count_by_status('em andamento')
        resolvida_count = self._count_by_status('resolvida')

        self.aberta_tab_btn.configure(text=f"Abertas ({aberta_count})")
        self.andamento_tab_btn.configure(text=f"Em Andamento ({andamento_count})")
        self.resolvida_tab_btn.configure(text=f"Resolvidas ({resolvida_count})")

        # Atualizar stats
        self.refresh_stats()

    def create_occurrence_card(self, occ: Ocorrencia):
        card = ctk.CTkFrame(self.scrollable_frame,
                            fg_color=self.colors['white'],
                            corner_radius=15,
                            border_width=1,
                            border_color=self.colors['gray_light'])
        card.pack(fill='x', pady=10, padx=5)

        # Header do card
        header = ctk.CTkFrame(card, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(15, 5))

        # Título
        titulo = ctk.CTkLabel(header, text=occ.titulo,
                              font=ctk.CTkFont(size=16, weight='bold'),
                              text_color=self.colors['blue_dark'],
                              anchor='w')
        titulo.pack(side='left', fill='x', expand=True)

        # Botões
        buttons_frame = ctk.CTkFrame(header, fg_color='transparent')
        buttons_frame.pack(side='right')

        # Botão Info
        info_btn = ctk.CTkButton(buttons_frame,
                                 text='ℹ',
                                 width=40,
                                 height=40,
                                 corner_radius=10,
                                 fg_color=self.colors['blue_light'],
                                 text_color=self.colors['blue_dark'],
                                 hover_color='#bfdbfe',
                                 font=ctk.CTkFont(size=18, weight='bold'),
                                 command=lambda o=occ: self.show_details(o))
        info_btn.pack(side='left', padx=5)

        # Botão deletar
        delete_btn = ctk.CTkButton(buttons_frame,
                                   text='🗑',
                                   width=40,
                                   height=40,
                                   corner_radius=10,
                                   fg_color=self.colors['red_light'],
                                   text_color=self.colors['red_text'],
                                   hover_color='#fecaca',
                                   font=ctk.CTkFont(size=18),
                                   command=lambda o=occ: self.delete_occurrence(o.id))
        delete_btn.pack(side='left', padx=5)

        # Descrição
        desc = ctk.CTkLabel(card, text=occ.descricao,
                            font=ctk.CTkFont(size=12),
                            text_color=self.colors['gray_text'],
                            anchor='w',
                            justify='left',
                            wraplength=600)
        desc.pack(fill='x', padx=20, pady=5)

        equipamento = self.sistema.buscar_equipamento_por_id(occ.equipamentoId)

        if equipamento:
            equipamento_label = ctk.CTkLabel(
                card,
                text=f"🖥 Equipamento: {equipamento.nome}",
                font=ctk.CTkFont(size=11, weight='bold'),
                text_color=self.colors['blue_dark']
            )

            equipamento_label.pack(anchor='w', padx=20, pady=(0, 10))

        # Footer com data e status
        footer = ctk.CTkFrame(card, fg_color='transparent')
        footer.pack(fill='x', padx=20, pady=(5, 15))

        date_str = occ.data_criacao.strftime('%d de %b, %Y')
        date_label = ctk.CTkLabel(footer, text=f"📅 {date_str}",
                                  font=ctk.CTkFont(size=11),
                                  text_color=self.colors['gray_text'])
        date_label.pack(side='left')

        # Status com opções de mudança
        status_frame = ctk.CTkFrame(footer, fg_color='transparent')
        status_frame.pack(side='left', padx=10)

        status_map = {
            'aberta': (self.colors['blue_light'], '#1e40af', '○'),
            'em andamento': (self.colors['yellow_light'], self.colors['yellow_dark'], '◐'),
            'resolvida': (self.colors['green_light'], '#15803d', '●')
        }

        color, text_color, symbol = status_map.get(occ.status, status_map['aberta'])

        status_label = ctk.CTkLabel(status_frame,
                                    text=f"{symbol} {occ.status.capitalize()}",
                                    font=ctk.CTkFont(size=11, weight='bold'),
                                    text_color=text_color,
                                    fg_color=color,
                                    corner_radius=10,
                                    padx=10,
                                    pady=5)
        status_label.pack(side='left', padx=5)

        # Botões para mudar status
        status_buttons_frame = ctk.CTkFrame(status_frame, fg_color='transparent')
        status_buttons_frame.pack(side='left', padx=5)

        # Retroceder status
        back_status_btn = ctk.CTkButton(status_buttons_frame,
                                        text='⬇',
                                        width=30,
                                        height=30,
                                        corner_radius=8,
                                        fg_color='#fee2e2',
                                        text_color=self.colors['red_text'],
                                        hover_color='#fecaca',
                                        font=ctk.CTkFont(size=12, weight='bold'),
                                        command=lambda o=occ: self.revert_status(o.id))
        back_status_btn.pack(side='left', padx=2)

        # Avançar status
        change_status_btn = ctk.CTkButton(status_buttons_frame,
                                          text='⬆',
                                          width=30,
                                          height=30,
                                          corner_radius=8,
                                          fg_color=self.colors['blue_pastel'],
                                          text_color=self.colors['blue_dark'],
                                          hover_color='#7dd3fc',
                                          font=ctk.CTkFont(size=12, weight='bold'),
                                          command=lambda o=occ: self.advance_status(o.id))
        change_status_btn.pack(side='left', padx=2)

    def add_occurrence(self):
        titulo = self.titulo_entry.get().strip()
        descricao = self.desc_text.get('1.0', 'end-1c').strip()
        equipamento_id = self._obter_equipamento_selecionado()

        if not titulo or not descricao:
            return

        self.sistema.criar_ocorrencia(titulo, descricao, equipamentoId=equipamento_id)

        self.titulo_entry.delete(0, 'end')
        self.desc_text.delete('1.0', 'end')
        if self.equipamento_combo:
            self.equipamento_combo.set('Nenhum equipamento')

        self.update_list()
        self.reload_data()

    def _obter_equipamento_selecionado(self):
        if not self.equipamento_combo:
            return None

        selecionado = self.equipamento_combo.get().strip()
        if not selecionado or selecionado == 'Nenhum equipamento':
            return None

        return self.equipamento_combo_map.get(selecionado)

    def _refresh_equipamento_combo(self):
        if not self.equipamento_combo:
            return

        equipamentos = sorted(self.sistema.equipamentos, key=lambda eq: eq.nome.lower())
        opcoes = ['Nenhum equipamento']
        self.equipamento_combo_map = {}

        for equipamento in equipamentos:
            rotulo = f"{equipamento.nome} ({equipamento.codigo})"
            opcoes.append(rotulo)
            self.equipamento_combo_map[rotulo] = equipamento.id

        selecionado_atual = self.equipamento_combo.get().strip()
        self.equipamento_combo.configure(values=opcoes)
        if selecionado_atual in opcoes:
            self.equipamento_combo.set(selecionado_atual)
        else:
            self.equipamento_combo.set('Nenhum equipamento')

    def reload_data(self):
        self.sistema.carregar_dados()
        self.update_list()
        self._refresh_equipamento_combo()
        if self.equipamentos_window and self.equipamentos_window.winfo_exists():
            self.refresh_equipamentos_window()

    def open_equipamentos_window(self):
        if self.equipamentos_window and self.equipamentos_window.winfo_exists():
            self.equipamentos_window.lift()
            self.equipamentos_window.focus_force()
            return

        window = ctk.CTkToplevel(self)
        window.title('Equipamentos')
        window.state('zoomed')
        window.configure(fg_color=self.colors['bg_gradient'])
        window.transient(self)
        window.grab_set()
        self.equipamentos_window = window

        outer = ctk.CTkFrame(window, fg_color=self.colors['white'], corner_radius=20)
        outer.pack(fill='both', expand=True, padx=20, pady=20)

        header = ctk.CTkFrame(outer, fg_color='transparent')
        header.pack(fill='x', padx=20, pady=(20, 10))

        title = ctk.CTkLabel(header,
                             text='Equipamentos',
                             font=ctk.CTkFont(size=24, weight='bold'),
                             text_color=self.colors['blue_dark'])
        title.pack(side='left')

        reload_btn = ctk.CTkButton(header,
                                   text='↻ Recarregar',
                                   height=34,
                                   corner_radius=10,
                                   fg_color=self.colors['gray_light'],
                                   text_color=self.colors['blue_dark'],
                                   hover_color='#e5e7eb',
                                   command=self.reload_data)
        reload_btn.pack(side='right')

        body = ctk.CTkFrame(outer, fg_color='transparent')
        body.pack(fill='both', expand=True, padx=20, pady=10)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        form = ctk.CTkFrame(body, fg_color=self.colors['gray_light'], corner_radius=16)
        form.grid(row=0, column=0, padx=(0, 10), sticky='nsew')

        form_title = ctk.CTkLabel(form, text='Novo / Editar equipamento',
                                  font=ctk.CTkFont(size=16, weight='bold'),
                                  text_color=self.colors['blue_dark'])
        form_title.pack(anchor='w', padx=16, pady=(16, 10))

        self.eq_nome_entry = ctk.CTkEntry(form, placeholder_text='Nome do equipamento', height=40)
        self.eq_nome_entry.pack(fill='x', padx=16, pady=(0, 10))

        self.eq_codigo_entry = ctk.CTkEntry(form, placeholder_text='Código', height=40)
        self.eq_codigo_entry.pack(fill='x', padx=16, pady=(0, 10))

        self.eq_localizacao_entry = ctk.CTkEntry(form, placeholder_text='Localização', height=40)
        self.eq_localizacao_entry.pack(fill='x', padx=16, pady=(0, 10))

        buttons = ctk.CTkFrame(form, fg_color='transparent')
        buttons.pack(fill='x', padx=16, pady=(0, 16))

        self.eq_salvar_btn = ctk.CTkButton(buttons,
                                           text='Salvar equipamento',
                                           height=40,
                                           corner_radius=10,
                                           fg_color=self.colors['blue_pastel'],
                                           text_color=self.colors['blue_dark'],
                                           command=self.save_equipamento)
        self.eq_salvar_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))

        cancelar_btn = ctk.CTkButton(buttons,
                                     text='Limpar',
                                     height=40,
                                     corner_radius=10,
                                     fg_color=self.colors['gray_light'],
                                     text_color=self.colors['blue_dark'],
                                     hover_color='#e5e7eb',
                                     command=self.clear_equipamento_form)
        cancelar_btn.pack(side='left', fill='x', expand=True, padx=(8, 0))

        list_panel = ctk.CTkFrame(body, fg_color='transparent')
        list_panel.grid(row=0, column=1, padx=(10, 0), sticky='nsew')

        list_title = ctk.CTkLabel(list_panel,
                                 text='Equipamentos cadastrados',
                                 font=ctk.CTkFont(size=16, weight='bold'),
                                 text_color=self.colors['blue_dark'])
        list_title.pack(anchor='w', pady=(0, 10))

        self.equipamentos_lista_frame = ctk.CTkScrollableFrame(list_panel, fg_color='transparent')
        self.equipamentos_lista_frame.pack(fill='both', expand=True)
        self._refresh_equipamento_combo()
        self.refresh_equipamentos_window()

    def refresh_equipamentos_window(self):
        if not self.equipamentos_lista_frame:
            return

        for widget in self.equipamentos_lista_frame.winfo_children():
            widget.destroy()

        if not self.sistema.equipamentos:
            empty = ctk.CTkLabel(self.equipamentos_lista_frame,
                                 text='Nenhum equipamento cadastrado ainda.',
                                 text_color=self.colors['gray_text'])
            empty.pack(pady=40)
            return

        for equipamento in self.sistema.equipamentos:
            card = ctk.CTkFrame(self.equipamentos_lista_frame,
                                fg_color=self.colors['white'],
                                corner_radius=14,
                                border_width=1,
                                border_color=self.colors['gray_light'])
            card.pack(fill='x', pady=8, padx=4)

            info = ctk.CTkLabel(card,
                                text=f"{equipamento.nome}\nCódigo: {equipamento.codigo}\nLocalização: {equipamento.localização}",
                                justify='left',
                                anchor='w',
                                text_color=self.colors['gray_text'])
            info.pack(side='left', padx=16, pady=16, fill='x', expand=True)

            vinculos = [o for o in self.sistema.ocorrencias if o.equipamentoId == equipamento.id]
            vinculo_texto = 'Sem ocorrências vinculadas'
            if vinculos:
                titulos = ', '.join(o.titulo for o in vinculos[:2])
                if len(vinculos) > 2:
                    titulos += ', ...'
                vinculo_texto = f'Vinculado a {len(vinculos)} ocorrência(s): {titulos}'

            vinculo_label = ctk.CTkLabel(card,
                                         text=vinculo_texto,
                                         justify='left',
                                         anchor='w',
                                         text_color=self.colors['gray_text'],
                                         font=ctk.CTkFont(size=12))
            vinculo_label.pack(fill='x', padx=16, pady=(0, 12))

            buttons_frame = ctk.CTkFrame(card, fg_color='transparent')
            buttons_frame.pack(side='right', padx=16)

            details_btn = ctk.CTkButton(
                buttons_frame,
                text='ℹ',
                width=38,
                height=36,
                corner_radius=10,
                fg_color=self.colors['blue_light'],
                text_color=self.colors['blue_dark'],
                command=lambda eq=equipamento: self.show_equipamento_details(eq)
            )

            details_btn.pack(side='left', padx=5)

            edit_btn = ctk.CTkButton(buttons_frame,
                                    text='✏️',
                                    width=38,
                                    height=36,
                                    corner_radius=10,
                                    fg_color=self.colors['blue_pastel'],
                                    text_color=self.colors['blue_dark'],
                                    command=lambda eq=equipamento: self.load_equipamento_for_edit(eq))
            edit_btn.pack(side='left', padx=5)

            delete_btn = ctk.CTkButton(buttons_frame,
                                      text='🗑',
                                      width=38,
                                      height=36,
                                      corner_radius=10,
                                      fg_color=self.colors['red_light'],
                                      text_color=self.colors['red_text'],
                                      command=lambda eq=equipamento: self.delete_equipamento(eq.id))
            delete_btn.pack(side='left', padx=5)

            new_occ_btn = ctk.CTkButton(buttons_frame,
                                        text='➕',
                                        width=38,
                                        height=36,
                                        corner_radius=10,
                                        fg_color=self.colors['green_light'],
                                        text_color=self.colors['green_dark'],
                                        command=lambda eq=equipamento: self.abrir_formulario_ocorrencia_com_equipamento(eq))
            new_occ_btn.pack(side='left', padx=5)

    def load_equipamento_for_edit(self, equipamento):
        self.equipamento_editando_id = equipamento.id
        self.eq_nome_entry.delete(0, 'end')
        self.eq_nome_entry.insert(0, equipamento.nome)
        self.eq_codigo_entry.delete(0, 'end')
        self.eq_codigo_entry.insert(0, equipamento.codigo)
        self.eq_localizacao_entry.delete(0, 'end')
        self.eq_localizacao_entry.insert(0, equipamento.localizacao)
        self.eq_salvar_btn.configure(text='Atualizar equipamento')

    def delete_equipamento(self, eq_id: int):
        equipamento = self.sistema.buscar_equipamento_por_id(eq_id)
        if not equipamento:
            messagebox.showerror('Erro', 'Equipamento não encontrado.')
            return

        if messagebox.askyesno('Confirmar', f'Apagar o equipamento "{equipamento.nome}"? As ocorrências associadas não serão afetadas.'):
            if self.sistema.remover_equipamento(eq_id):
                self.refresh_equipamentos_window()
            else:
                messagebox.showerror('Erro', 'Não foi possível apagar o equipamento.')

    def clear_equipamento_form(self):
        self.equipamento_editando_id = None
        self.eq_nome_entry.delete(0, 'end')
        self.eq_codigo_entry.delete(0, 'end')
        self.eq_localizacao_entry.delete(0, 'end')
        self.eq_salvar_btn.configure(text='Salvar equipamento')

    def save_equipamento(self):
        nome = self.eq_nome_entry.get().strip()
        codigo = self.eq_codigo_entry.get().strip()
        localizacao = self.eq_localizacao_entry.get().strip()

        if not nome or not codigo or not localizacao:
            messagebox.showwarning('Validação', 'Preencha nome, código e localização.')
            return

        if self.equipamento_editando_id is None:
            self.sistema.criar_equipamento(nome, codigo, localizacao)
        else:
            if not self.sistema.atualizar_equipamento(self.equipamento_editando_id, nome=nome, codigo=codigo, localizacao=localizacao):
                messagebox.showerror('Erro', 'Equipamento não encontrado.')
                return

        self.clear_equipamento_form()
        self.reload_data()
        self.refresh_equipamentos_window()

    def abrir_formulario_ocorrencia_com_equipamento(self, equipamento):
        if self.equipamentos_window and self.equipamentos_window.winfo_exists():
            self.equipamentos_window.destroy()

        if self.equipamento_combo:
            rotulo = f"{equipamento.nome} ({equipamento.codigo})"
            if rotulo not in self.equipamento_combo_map:
                self._refresh_equipamento_combo()
            self.equipamento_combo.set(rotulo)

        self.title_entry_focus()

    def title_entry_focus(self):
        if hasattr(self, 'titulo_entry'):
            self.lift()
            self.focus_force()
            self.titulo_entry.focus_set()

    def advance_status(self, occ_id: int):
        """Avançar o status da ocorrência: aberta -> em andamento -> resolvida"""
        occ = self.sistema.buscar_ocorrencia_por_id(occ_id)
        if occ:
            # Fluxo linear de status para evitar combinações inválidas.
            status_order = ['aberta', 'em andamento', 'resolvida']
            current_index = status_order.index(occ.status) if occ.status in status_order else 0

            if current_index < len(status_order) - 1:
                new_status = status_order[current_index + 1]
                self.sistema.atualizar_status(occ_id, new_status)

        self.update_list()

    def show_details(self, occ: Ocorrencia):
        """Mostrar janela com detalhes da ocorrência"""
        # Criar janela top-level
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Detalhes - {occ.titulo}")
        details_window.geometry("700x650")
        details_window.resizable(False, False)

        # Fundo com gradiente sutil
        details_window.configure(fg_color=self.colors['bg_gradient'])
        # Esse bloco garante que a janela de detalhes abra na frente da principal.
        details_window.transient(self)
        details_window.lift()
        details_window.focus_force()
        details_window.grab_set()
        details_window.after(50, lambda: details_window.attributes('-topmost', True))
        details_window.after(150, lambda: details_window.attributes('-topmost', False))
        details_window.after(0, details_window.lift)

        # Container principal com fundo branco elegante
        main_frame = ctk.CTkFrame(details_window, fg_color=self.colors['white'],
                                  corner_radius=20)
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)

        # Header com fundo colorido baseado no status
        status_map = {
            'aberta': (self.colors['blue_light'], '#1e40af'),
            'em andamento': (self.colors['yellow_light'], self.colors['yellow_dark']),
            'resolvida': (self.colors['green_light'], '#15803d')
        }
        
        header_bg, header_text_color = status_map.get(occ.status, status_map['aberta'])
        
        header_frame = ctk.CTkFrame(main_frame, fg_color=header_bg, corner_radius=15)
        header_frame.pack(fill='x', pady=(0, 20), padx=5)

        # Título no header
        title_label = ctk.CTkLabel(header_frame, text=occ.titulo,
                                   font=ctk.CTkFont(size=24, weight='bold'),
                                   text_color=header_text_color)
        title_label.pack(pady=15, padx=15, anchor='w')

        # Info grid
        info_frame = ctk.CTkFrame(main_frame, fg_color=self.colors['gray_light'],
                                  corner_radius=15)
        info_frame.pack(fill='x', pady=(0, 20), padx=5)

        # ID
        id_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        id_frame.pack(fill='x', padx=15, pady=(10, 5))

        id_label = ctk.CTkLabel(id_frame, text="ID:",
                                font=ctk.CTkFont(size=13, weight='bold'),
                                text_color=self.colors['blue_dark'])
        id_label.pack(side='left', padx=(0, 15))

        id_value = ctk.CTkLabel(id_frame, text=str(occ.id),
                                font=ctk.CTkFont(size=13),
                                text_color=self.colors['gray_text'])
        id_value.pack(side='left')

        # Data de criação
        date_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        date_frame.pack(fill='x', padx=15, pady=5)

        date_label = ctk.CTkLabel(date_frame, text="Data de Criação:",
                                  font=ctk.CTkFont(size=13, weight='bold'),
                                  text_color=self.colors['blue_dark'])
        date_label.pack(side='left', padx=(0, 15))

        date_value = ctk.CTkLabel(date_frame, text=occ.data_criacao.strftime('%d de %b de %Y às %H:%M'),
                                  font=ctk.CTkFont(size=13),
                                  text_color=self.colors['gray_text'])
        date_value.pack(side='left')

        # Status
        status_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        status_frame.pack(fill='x', padx=15, pady=(5, 10))

        status_label = ctk.CTkLabel(status_frame, text="Status:",
                                    font=ctk.CTkFont(size=13, weight='bold'),
                                    text_color=self.colors['blue_dark'])
        status_label.pack(side='left', padx=(0, 15))

        color, text_color = status_map.get(occ.status, status_map['aberta'])

        status_value = ctk.CTkLabel(status_frame, text=occ.status.capitalize(),
                                    font=ctk.CTkFont(size=13, weight='bold'),
                                    text_color=text_color,
                                    fg_color=color,
                                    corner_radius=10,
                                    padx=12,
                                    pady=6)
        status_value.pack(side='left')

        equipamento = self.sistema.buscar_equipamento_por_id(occ.equipamentoId) if occ.equipamentoId else None
        equipamento_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        equipamento_frame.pack(fill='x', padx=15, pady=(5, 10))

        equipamento_label = ctk.CTkLabel(equipamento_frame, text="Equipamento:",
                                         font=ctk.CTkFont(size=13, weight='bold'),
                                         text_color=self.colors['blue_dark'])
        equipamento_label.pack(side='left', padx=(0, 15))

        if equipamento:
            equipamento_text = f"{equipamento.nome} | Código: {equipamento.codigo} | Local: {equipamento.localizacao}"
        elif occ.equipamentoId is not None:
            equipamento_text = f"ID {occ.equipamentoId} (não encontrado)"
        else:
            equipamento_text = 'Nenhum equipamento vinculado'

        equipamento_value = ctk.CTkLabel(equipamento_frame, text=equipamento_text,
                                         font=ctk.CTkFont(size=13),
                                         text_color=self.colors['gray_text'])
        equipamento_value.pack(side='left')

        # Separador
        separator = ctk.CTkFrame(main_frame, fg_color=self.colors['gray_light'], height=2)
        separator.pack(fill='x', pady=15, padx=5)

        # Descrição
        desc_label = ctk.CTkLabel(main_frame, text="Descrição:",
                                  font=ctk.CTkFont(size=14, weight='bold'),
                                  text_color=self.colors['blue_dark'])
        desc_label.pack(pady=(0, 12), anchor='w', padx=5)

        desc_text = ctk.CTkTextbox(main_frame, height=180,
                                   corner_radius=12,
                                   border_width=2,
                                   border_color=self.colors['blue_pastel'],
                                   text_color=self.colors['gray_text'])
        desc_text.pack(fill='both', expand=True, pady=(0, 20), padx=5)
        desc_text.insert('1.0', occ.descricao)
        desc_text.configure(state='disabled')

        # Botões de ação com melhor espaçamento
        buttons_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        buttons_frame.pack(fill='x', pady=(0, 0), padx=5)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        buttons_frame.grid_columnconfigure(3, weight=1)

        # Botão retroceder status
        back_status_btn = ctk.CTkButton(buttons_frame,
                                        text="⬇ Retroceder",
                                        height=45,
                                        corner_radius=12,
                                        fg_color='#fee2e2',
                                        text_color=self.colors['red_text'],
                                        hover_color='#fecaca',
                                        font=ctk.CTkFont(size=12, weight='bold'),
                                        command=lambda: self._close_and_revert(details_window, occ.id))
        back_status_btn.grid(row=0, column=0, padx=5, sticky='ew')

        # Botão avançar status
        advance_btn = ctk.CTkButton(buttons_frame,
                                    text="⬆ Avançar",
                                    height=45,
                                    corner_radius=12,
                                    fg_color=self.colors['blue_pastel'],
                                    text_color=self.colors['blue_dark'],
                                    hover_color='#7dd3fc',
                                    font=ctk.CTkFont(size=12, weight='bold'),
                                    command=lambda: self._close_and_advance(details_window, occ.id))
        advance_btn.grid(row=0, column=1, padx=5, sticky='ew')

        # Botão deletar
        delete_btn = ctk.CTkButton(buttons_frame,
                                   text="🗑 Deletar",
                                   height=45,
                                   corner_radius=12,
                                   fg_color=self.colors['red_light'],
                                   text_color=self.colors['red_text'],
                                   hover_color='#fecaca',
                                   font=ctk.CTkFont(size=12, weight='bold'),
                                   command=lambda: self._close_and_delete(details_window, occ.id))
        delete_btn.grid(row=0, column=2, padx=5, sticky='ew')

        # Botão fechar
        close_btn = ctk.CTkButton(buttons_frame,
                                  text="Fechar",
                                  height=45,
                                  corner_radius=12,
                                  fg_color=self.colors['gray_light'],
                                  text_color=self.colors['blue_dark'],
                                  hover_color='#e5e7eb',
                                  font=ctk.CTkFont(size=12, weight='bold'),
                                  command=details_window.destroy)
        close_btn.grid(row=0, column=3, padx=5, sticky='ew')

    def revert_status(self, occ_id: int):
        """Retroceder o status da ocorrência: resolvida -> em andamento -> aberta"""
        occ = self.sistema.buscar_ocorrencia_por_id(occ_id)
        if occ:
            # Usa a mesma ordem do avanço para manter consistência dos estados.
            status_order = ['aberta', 'em andamento', 'resolvida']
            current_index = status_order.index(occ.status) if occ.status in status_order else 0

            if current_index > 0:
                new_status = status_order[current_index - 1]
                self.sistema.atualizar_status(occ_id, new_status)

        self.update_list()

    def _close_and_advance(self, window, occ_id: int):
        """Fechar janela e avançar status"""
        self.advance_status(occ_id)
        window.destroy()

    def _close_and_revert(self, window, occ_id: int):
        """Fechar janela e retroceder status"""
        self.revert_status(occ_id)
        window.destroy()

    def _close_and_delete(self, window, occ_id: int):
        """Fechar janela e deletar ocorrência"""
        self.delete_occurrence(occ_id)
        window.destroy()

    def delete_occurrence(self, occ_id: int):
        """Deletar uma ocorrência"""
        self.sistema.remover_ocorrencia(occ_id)
        self.update_list()

    def _count_by_status(self, status: str) -> int:
        """Contar ocorrências por status."""
        return len([o for o in self.sistema.ocorrencias if o.status == status])

    def refresh_stats(self):
        """Atualizar estatísticas."""
        # Atualiza os números dos cards sem recriar os widgets do topo.
        if hasattr(self, 'aberta_number_label'):
            self.aberta_number_label.configure(text=str(self._count_by_status('aberta')))

        if hasattr(self, 'andamento_number_label'):
            self.andamento_number_label.configure(text=str(self._count_by_status('em andamento')))

        if hasattr(self, 'resolvida_number_label'):
            self.resolvida_number_label.configure(text=str(self._count_by_status('resolvida')))

    def _get_occurrence_status(self, occ_id: int) -> str:
        """Obter status da ocorrência por ID."""
        occ = self.sistema.buscar_ocorrencia_por_id(occ_id)
        return occ.status if occ else None

    def show_equipamento_details(self, equipamento):
        details = ctk.CTkToplevel(self)
        details.transient(self)
        details.lift()
        details.focus_force()
        details.grab_set()

        details.after(50, lambda: details.attributes('-topmost', True))
        details.after(150, lambda: details.attributes('-topmost', False))

        details.title(f"Equipamento - {equipamento.nome}")
        details.geometry("900x700")

        container = ctk.CTkFrame(details)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(
            container,
            text=equipamento.nome,
            font=ctk.CTkFont(size=26, weight='bold')
        )
        titulo.pack(anchor='w', pady=(0, 20))

        info = ctk.CTkLabel(
            container,
            text=(
                f"Código: {equipamento.codigo}\n"
                f"Localização: {equipamento.localizacao}"
            ),
            justify='left'
        )
        info.pack(anchor='w', pady=(0, 20))

        subtitulo = ctk.CTkLabel(
            container,
            text="Ocorrências relacionadas",
            font=ctk.CTkFont(size=18, weight='bold')
        )
        subtitulo.pack(anchor='w')

        scroll = ctk.CTkScrollableFrame(container)
        scroll.pack(fill='both', expand=True, pady=10)

        ocorrencias = [
            o for o in self.sistema.ocorrencias
            if o.equipamentoId == equipamento.id
        ]

        if not ocorrencias:
            vazio = ctk.CTkLabel(
                scroll,
                text="Nenhuma ocorrência vinculada."
            )
            vazio.pack(pady=20)

        for occ in ocorrencias:
            card = ctk.CTkFrame(scroll)
            card.pack(fill='x', pady=8)

            titulo_occ = ctk.CTkLabel(
                card,
                text=occ.titulo,
                font=ctk.CTkFont(size=15, weight='bold')
            )
            titulo_occ.pack(anchor='w', padx=15, pady=(10, 0))

            desc = ctk.CTkLabel(
                card,
                text=occ.descricao,
                wraplength=700,
                justify='left'
            )
            desc.pack(anchor='w', padx=15, pady=(5, 10))

            detalhes_btn = ctk.CTkButton(
                card,
                text="Abrir ocorrência",
                command=lambda o=occ: self.show_details(o)
            )
            detalhes_btn.pack(anchor='e', padx=15, pady=(0, 10))


if __name__ == "__main__":
    app = OccurrenceSystem()
    app.mainloop()