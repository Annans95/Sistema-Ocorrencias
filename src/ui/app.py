import customtkinter as ctk
from src.services.sistema import SistemaOcorrencias
from src.models.ocorrencia import Ocorrencia


class OccurrenceSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("Sistema de Ocorrências")
        self.geometry("1400x900")

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
        form_frame = ctk.CTkFrame(parent, fg_color=self.colors['white'],
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

        if not titulo or not descricao:
            return

        self.sistema.criar_ocorrencia(titulo, descricao)

        self.titulo_entry.delete(0, 'end')
        self.desc_text.delete('1.0', 'end')

        self.update_list()

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


if __name__ == "__main__":
    app = OccurrenceSystem()
    app.mainloop()