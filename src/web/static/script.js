// ==========================================
// DADOS E ESTADO DA APLICAÇÃO
// ==========================================

let estado = {
    visualizacaoAtual: 'ocorrencias', // 'ocorrencias' ou 'equipamentos'
    abaAtiva: 'aberta', // 'aberta', 'em_andamento', 'resolvida'
    ocorrenciaSelecionada: null,
    equipamentoSelecionado: null,
    estaEditando: false,
    equipamentos: [],
    ocorrencias: []
};

// ==========================================
// CARREGAMENTO DE DADOS
// ==========================================

async function carregarOcorrencias() {

    try {

        const resposta =
            await fetch('/api/ocorrencias');

        if (!resposta.ok) {
            throw new Error(
                'Erro ao carregar ocorrências'
            );
        }

        const dados =
            await resposta.json();

        estado.ocorrencias = dados;

    } catch (erro) {

        console.error(erro);
        estado.ocorrencias = [];
    }
}

async function carregarEquipamentos() {

    try {

        const resposta =
            await fetch('/api/equipamentos');

        if (!resposta.ok) {
            throw new Error(
                'Erro ao carregar equipamentos'
            );
        }

        const dados =
            await resposta.json();

        estado.equipamentos = dados;

    } catch (erro) {

        console.error(erro);
        estado.equipamentos = [];
    }
}


// ==========================================
// FUNÇÕES AUXILIARES
// ==========================================

function obterRotuloStatus(status) {
    const rotulos = {
        'aberta': 'Aberta',
        'em_andamento': 'Em Andamento',
        'resolvida': 'Resolvida'
    };
    return rotulos[status] || status;
}

function obterIconeStatus(status) {
    const icones = {
        'aberta': '📋',
        'em_andamento': '⏳',
        'resolvida': '✅'
    };
    return icones[status] || '📋';
}

function formatarData(data) {
    return new Date(data).toLocaleDateString('pt-BR');
}

function obterOcorrenciasPorStatus(status) {
    return estado.ocorrencias.filter(ocorr => ocorr.status === status);
}

function obterOcorrenciasPorEquipamento(equipamentoId) {
    return estado.ocorrencias.filter(
        ocorr => String(ocorr.equipamentoId) === String(equipamentoId)
    );
}

function obterEquipamentoPorId(id) {
    return estado.equipamentos.find(
        eq => String(eq.id) === String(id)
    );
}

function obterEquipamentoPorCodigo(codigo) {
    // Busca equipamento pelo codigo, que e estavel para deep-links de QR code.
    return estado.equipamentos.find(
        eq => String(eq.codigo) === String(codigo)
    );
}

// ==========================================
// RENDERIZAÇÃO
// ==========================================

function renderizar() {
    renderizarCabecalho();
    renderizarEstatisticas();
    renderizarVisualizacoes();
    renderizarListaOcorrencias();
    atualizarSelectEquipamento();
}

function renderizarCabecalho() {
    const botaoVoltar = document.getElementById('botaoVoltar');
    const icone = document.getElementById('cabecalhoIconeContainer');
    const titulo = document.getElementById('cabecalhoTitulo');
    const subtitulo = document.getElementById('cabecalhoSubtitulo');
    const botaoEquipamentos = document.getElementById('botaoVerEquipamentos');

    if (estado.visualizacaoAtual === 'equipamentos') {
        botaoVoltar.style.display = 'flex';
        icone.textContent = '📦';
        titulo.textContent = 'Equipamentos';
        subtitulo.textContent = 'Gerencie equipamentos e patrimônios';
        botaoEquipamentos.style.display = 'none';
    } else {
        botaoVoltar.style.display = 'none';
        icone.textContent = '📋';
        titulo.textContent = 'Sistema de Ocorrências';
        subtitulo.textContent = 'Gerencie e acompanhe ocorrências internas';
        botaoEquipamentos.style.display = 'flex';
    }
}

function renderizarEstatisticas() {
    const container = document.getElementById('cardsEstatisticas');
    const contagemAbertas = obterOcorrenciasPorStatus('aberta').length;
    const contagemEmAndamento = obterOcorrenciasPorStatus('em_andamento').length;
    const contagemResolvidas = obterOcorrenciasPorStatus('resolvida').length;

    container.innerHTML = `
        <div class="card-estatistica azul">
            <div class="info-estatistica">
                <p>Ocorrências Abertas</p>
                <h3>${contagemAbertas}</h3>
            </div>
            <div class="icone-estatistica">📋</div>
        </div>
        <div class="card-estatistica amarelo">
            <div class="info-estatistica">
                <p>Em Andamento</p>
                <h3>${contagemEmAndamento}</h3>
            </div>
            <div class="icone-estatistica">⏳</div>
        </div>
        <div class="card-estatistica verde">
            <div class="info-estatistica">
                <p>Ocorrências Resolvidas</p>
                <h3>${contagemResolvidas}</h3>
            </div>
            <div class="icone-estatistica">✅</div>
        </div>
    `;
}

function renderizarVisualizacoes() {
    const visualizacaoOcorrencias = document.getElementById('visualizacaoOcorrencias');
    const visualizacaoEquipamentos = document.getElementById('visualizacaoEquipamentos');

    if (estado.visualizacaoAtual === 'ocorrencias') {
        visualizacaoOcorrencias.style.display = 'block';
        visualizacaoEquipamentos.style.display = 'none';
    } else {
        visualizacaoOcorrencias.style.display = 'none';
        visualizacaoEquipamentos.style.display = 'block';
        renderizarListaEquipamentos();
    }
}

function renderizarListaOcorrencias() {
    const containerLista = document.getElementById('listaOcorrencias');
    const ocorrencias = obterOcorrenciasPorStatus(estado.abaAtiva);

    // Atualizar contadores nas abas
    document.getElementById('contagemAbertas').textContent = obterOcorrenciasPorStatus('aberta').length;
    document.getElementById('contagemEmAndamento').textContent = obterOcorrenciasPorStatus('em_andamento').length;
    document.getElementById('contagemResolvidas').textContent = obterOcorrenciasPorStatus('resolvida').length;

    if (ocorrencias.length === 0) {
        containerLista.innerHTML = `
            <div class="estado-vazio">
                <div class="icone-vazio">${obterIconeStatus(estado.abaAtiva)}</div>
                <p><strong>${obterMensagemVazia()}</strong></p>
            </div>
        `;
        return;
    }

    containerLista.innerHTML = ocorrencias.map(ocorr => {
        const equipamento = ocorr.equipamentoId ? obterEquipamentoPorId(ocorr.equipamentoId) : null;
        const podeSubir = ocorr.status !== 'resolvida';
        const podeDescer = ocorr.status !== 'aberta';

        return `
            <div class="card-ocorrencia" data-id="${ocorr.id}">
                <div class="cabecalho-ocorrencia">
                    <h3 class="titulo-ocorrencia">${ocorr.titulo}</h3>
                    <div class="acoes-ocorrencia">
                        <button class="botao-acao botao-visualizar" onclick="visualizarDetalhesOcorrencia('${ocorr.id}')">👁</button>
                        ${podeSubir ? `<button class="botao-acao botao-cima" onclick="statusCima('${ocorr.id}')">⬆</button>` : ''}
                        ${podeDescer ? `<button class="botao-acao botao-baixo" onclick="statusBaixo('${ocorr.id}')">⬇</button>` : ''}
                        <button class="botao-acao botao-excluir" onclick="excluirOcorrencia('${ocorr.id}')">🗑</button>
                    </div>
                </div>
                <p class="descricao-ocorrencia">${ocorr.descricao}</p>
                ${equipamento ? `
                    <div class="emblema-equipamento">
                        📦 ${equipamento.nome} <span style="color: #9C27B0;">(${equipamento.codigo})</span>
                    </div>
                ` : ''}
                <div class="rodape-ocorrencia">
                    📅 ${formatarData(ocorr.data_criacao)}
                    <span>•</span>
                    <span class="emblema-status ${ocorr.status}">
                        ${obterIconeStatus(ocorr.status)} ${obterRotuloStatus(ocorr.status)}
                    </span>
                </div>
            </div>
        `;
    }).join('');
}

function obterMensagemVazia() {
    const mensagens = {
        'aberta': 'Nenhuma ocorrência aberta\nTodas as ocorrências foram resolvidas!',
        'em_andamento': 'Nenhuma ocorrência em andamento\nOcorrências em progresso aparecerão aqui',
        'resolvida': 'Nenhuma ocorrência resolvida\nAs ocorrências resolvidas aparecerão aqui'
    };
    return mensagens[estado.abaAtiva] || '';
}

function renderizarListaEquipamentos() {
    const containerLista = document.getElementById('listaEquipamentos');

    if (!containerLista) return;

    if (!estado.equipamentos || estado.equipamentos.length === 0) {
        containerLista.innerHTML = `
            <div class="estado-vazio">
                <div class="icone-vazio">📦</div>
                <p><strong>Nenhum equipamento cadastrado ainda</strong></p>
                <p style="font-size: 0.875rem; margin-top: 0.5rem;">Adicione equipamentos ao registrar ocorrências</p>
            </div>
        `;
        return;
    }

    containerLista.innerHTML = estado.equipamentos.map(equipamento => {
        const ocorrencias = obterOcorrenciasPorEquipamento(equipamento.id);
        const contagemAbertas = ocorrencias.filter(o => o.status === 'aberta').length;
        const contagemEmAndamento = ocorrencias.filter(o => o.status === 'em_andamento').length;
        const contagemResolvidas = ocorrencias.filter(o => o.status === 'resolvida').length;

        return `
            <div class="card-equipamento" onclick="visualizarHistoricoEquipamento('${equipamento.id}')">
                <div class="cabecalho-equipamento">
                    <div class="info-equipamento">
                        <h3>${equipamento.nome}</h3>
                        <p><strong>Código:</strong> ${equipamento.codigo}</p>
                        <p><strong>Local:</strong> ${equipamento.localizacao}</p>
                    </div>
                    <div class="contagem-equipamento">
                        <h3>${ocorrencias.length}</h3>
                        <p>ocorrências</p>
                    </div>
                </div>
                <div class="estatisticas-equipamento">
                    <div class="estatistica-equipamento aberta">
                        <h4>${contagemAbertas}</h4>
                        <p>Abertas</p>
                    </div>
                    <div class="estatistica-equipamento em_andamento">
                        <h4>${contagemEmAndamento}</h4>
                        <p>Em Andamento</p>
                    </div>
                    <div class="estatistica-equipamento resolvida">
                        <h4>${contagemResolvidas}</h4>
                        <p>Resolvidas</p>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function atualizarSelectEquipamento() {
    const select = document.getElementById('selectEquipamento');

    if (!select) return;

    const valorAtual = select.value;

    const equipamentos = estado.equipamentos || [];

    select.innerHTML = '<option value="">Nenhum equipamento</option>' +
        equipamentos.map(eq => `
            <option value="${eq.id}"> ${eq.nome} (${eq.codigo})</option>
        `).join('');

    const existe = equipamentos.some(
        eq => String(eq.id) === String(valorAtual)
    );

    select.value = existe ? valorAtual : '';
}

// ==========================================
// AÇÕES DE OCORRÊNCIAS
// ==========================================

async function adicionarOcorrencia(evento) {
    evento.preventDefault();

    const titulo = document.getElementById('inputTitulo').value.trim();
    const descricao = document.getElementById('inputDescricao').value.trim();
    const equipamentoId = document.getElementById('selectEquipamento').value;

    if (!titulo || !descricao) {
        alert('Por favor, preencha todos os campos obrigatórios!');
        return;
    }

    // Debug: verificar o que está sendo capturado
    console.log('adicionarOcorrencia - equipamentoId capturado:', equipamentoId, 'tipo:', typeof equipamentoId);

    const payload = {
        titulo,
        descricao,
        equipamentoId: equipamentoId ? parseInt(equipamentoId) : null
    };
    
    console.log('Payload enviado:', payload);

    const resposta = await fetch('/api/ocorrencias', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    if (!resposta.ok) {
        alert('Erro ao criar ocorrência');
        return;
    }

    // recarrega dados do backend
    await carregarOcorrencias();

    // limpa form
    document.getElementById('formularioOcorrencia').reset();
    document.getElementById('novoFormularioEquipamento').style.display = 'none';
}

async function atualizarStatus(id, novoStatus) {

    const resposta = await fetch(`/api/ocorrencias/${id}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: novoStatus })
    });

    if (!resposta.ok) {
        alert('Erro ao atualizar status');
        return;
    }

    await carregarOcorrencias();
}

function statusCima(id) {
    const ocorrencia = estado.ocorrencias.find(o => String(o.id) === String(id));
    if (!ocorrencia) return;
    const statusAtual = ocorrencia.status;

    if (statusAtual === 'aberta') {
        atualizarStatus(id, 'em_andamento');
    }
    else if (statusAtual === 'em_andamento') {
        atualizarStatus(id, 'resolvida');
    }
}

function statusBaixo(id) {
    const ocorrencia = estado.ocorrencias.find(o => String(o.id) === String(id));
    if (!ocorrencia) return;
    const statusAtual = ocorrencia.status;

    if (statusAtual === 'resolvida') {
        atualizarStatus(id, 'em_andamento');
    }
    else if (statusAtual === 'em_andamento') {
        atualizarStatus(id, 'aberta');
    }
}

async function excluirOcorrencia(id) {

    if (!confirm('Tem certeza que deseja excluir esta ocorrência?')) return;

    const resposta = await fetch(`/api/ocorrencias/${id}`, {
        method: 'DELETE'
    });

    if (!resposta.ok) {
        alert('Erro ao excluir ocorrência');
        return;
    }

    await carregarOcorrencias();
}

async function atualizarOcorrencia(id, titulo, descricao, equipamentoId) {

    const resposta = await fetch(`/api/ocorrencias/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            titulo,
            descricao,
            equipamentoId: equipamentoId || null
        })
    });

    if (!resposta.ok) {
        alert('Erro ao atualizar ocorrência');
        return;
    }

    fecharModalDetalhes();
    await carregarOcorrencias();
}

// ==========================================
// MODAIS
// ==========================================

function visualizarDetalhesOcorrencia(id) {
    const ocorrencia = estado.ocorrencias.find(o => o.id === Number(id));
    if (!ocorrencia) return;

    estado.ocorrenciaSelecionada = ocorrencia;
    estado.estaEditando = false;

    const modal = document.getElementById('modalDetalhes');
    const modalTitulo = document.getElementById('modalTitulo');
    const modalCorpo = document.getElementById('modalCorpo');
    const botaoEditar = document.getElementById('botaoEditar');

    modalTitulo.textContent = 'Detalhes da Ocorrência';
    botaoEditar.style.display = 'block';

    const equipamento = ocorrencia.equipamentoId ? obterEquipamentoPorId(ocorrencia.equipamentoId) : null;
    const podeSubir = ocorrencia.status !== 'resolvida';
    const podeDescer = ocorrencia.status !== 'aberta';

    modalCorpo.innerHTML = `
        <div class="grupo-detalhe">
            <div class="rotulo-detalhe">Título</div>
            <div class="valor-detalhe grande">${ocorrencia.titulo}</div>
        </div>
        <div class="grupo-detalhe">
            <div class="rotulo-detalhe">Descrição</div>
            <div class="valor-detalhe">${ocorrencia.descricao}</div>
        </div>
        ${equipamento ? `
            <div class="grupo-detalhe">
                <div class="rotulo-detalhe">Equipamento</div>
                <div class="detalhe-equipamento">
                    <p>${equipamento.nome}</p>
                    <small>Código: ${equipamento.codigo} | ${equipamento.localizacao}</small>
                    <br>
                    <button class="botao-link-roxo" onclick="visualizarEquipamentoDeDetalhes('${equipamento.id}')">
                        Ver histórico completo
                    </button>
                </div>
            </div>
        ` : ''}
        <div style="display: flex; gap: 1rem;">
            <div class="grupo-detalhe" style="flex: 1;">
                <div class="rotulo-detalhe">Data de Criação</div>
                <div class="valor-detalhe">${formatarData(ocorrencia.data_criacao)}</div>
            </div>
            <div class="grupo-detalhe" style="flex: 1;">
                <div class="rotulo-detalhe">Status</div>
                <div>
                    <span class="emblema-status ${ocorrencia.status}">
                        ${obterIconeStatus(ocorrencia.status)} ${obterRotuloStatus(ocorrencia.status)}
                    </span>
                </div>
            </div>
        </div>
        <div class="modal-rodape">
            ${podeSubir ? `<button class="botao-primario" onclick="statusCimaDoModal('${ocorrencia.id}')">⬆ Avançar Status</button>` : ''}
            ${podeDescer ? `<button class="botao-secundario" onclick="statusBaixoDoModal('${ocorrencia.id}')">⬇ Retroceder Status</button>` : ''}
            <button class="botao-perigo" onclick="excluirOcorrenciaDoModal('${ocorrencia.id}')">🗑 Excluir</button>
        </div>
    `;

    modal.style.display = 'flex';
}

function statusCimaDoModal(id) {
    statusCima(id);
    visualizarDetalhesOcorrencia(id);
}

function statusBaixoDoModal(id) {
    statusBaixo(id);
    visualizarDetalhesOcorrencia(id);
}

function excluirOcorrenciaDoModal(id) {
    excluirOcorrencia(id);
    fecharModalDetalhes();
}

function editarOcorrencia() {
    if (!estado.ocorrenciaSelecionada) return;

    estado.estaEditando = true;
    const ocorrencia = estado.ocorrenciaSelecionada;
    const modalTitulo = document.getElementById('modalTitulo');
    const modalCorpo = document.getElementById('modalCorpo');
    const botaoEditar = document.getElementById('botaoEditar');

    modalTitulo.textContent = 'Editar Ocorrência';
    botaoEditar.style.display = 'none';

    modalCorpo.innerHTML = `
        <form class="formulario-edicao" onsubmit="salvarEdicao(event)">
            <div class="grupo-formulario">
                <label for="editarTitulo">Título</label>
                <input type="text" id="editarTitulo" value="${ocorrencia.titulo}" required>
            </div>
            <div class="grupo-formulario">
                <label for="editarDescricao">Descrição</label>
                <textarea id="editarDescricao" rows="6" required>${ocorrencia.descricao}</textarea>
            </div>
            <div class="grupo-formulario">
                <label for="editarEquipamento">Equipamento</label>
                <select id="editarEquipamento">
                    <option value="">Nenhum equipamento</option>
                    ${estado.equipamentos.map(eq =>
                        `<option value="${eq.id}" ${eq.id === ocorrencia.equipamentoId ? 'selected' : ''}>
                            ${eq.nome} (${eq.codigo})
                        </option>`
                    ).join('')}
                </select>
            </div>
            <div class="modal-rodape">
                <button type="submit" class="botao-primario">💾 Salvar Alterações</button>
                <button type="button" class="botao-cancelar" onclick="cancelarEdicao()">✖️ Cancelar</button>
            </div>
        </form>
    `;
}

async function salvarEdicao(evento) {
    evento.preventDefault();

    const titulo = document.getElementById('editarTitulo').value.trim();
    const descricao = document.getElementById('editarDescricao').value.trim();
    const equipamentoId = document.getElementById('editarEquipamento').value;

    const id = estado.ocorrenciaSelecionada.id;

    const resposta = await fetch(`/api/ocorrencias/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            titulo,
            descricao,
            equipamentoId: equipamentoId || null
        })
    });

    if (!resposta.ok) {
        alert('Erro ao atualizar ocorrência');
        return;
    }

    fecharModalDetalhes();
    await carregarOcorrencias();
}

function cancelarEdicao() {
    visualizarDetalhesOcorrencia(estado.ocorrenciaSelecionada.id);
}

function fecharModalDetalhes() {
    const modal = document.getElementById('modalDetalhes');

    if (modal) {
        modal.style.display = 'none';
    }

    estado.ocorrenciaSelecionada = null;
    estado.estaEditando = false;
}

function visualizarEquipamentoDeDetalhes(equipamentoId) {
    fecharModalDetalhes();
    estado.visualizacaoAtual = 'equipamentos';

    renderizarVisualizacoes();

    visualizarHistoricoEquipamento(equipamentoId);
}

function visualizarHistoricoEquipamento(equipamentoId) {
    const equipamento = obterEquipamentoPorId(equipamentoId);
    if (!equipamento) return;

    estado.equipamentoSelecionado = equipamento;
    const ocorrencias = obterOcorrenciasPorEquipamento(equipamentoId)
        .sort((a, b) =>
            new Date(b.data_criacao || 0) - new Date(a.data_criacao || 0)
        );

    const modal = document.getElementById('modalHistoricoEquipamento');
    const cabecalho = document.getElementById('cabecalhoHistoricoEquipamento');
    const corpo = document.getElementById('corpoHistoricoEquipamento');

    // proteção contra elementos inexistentes
    if (!modal || !cabecalho || !corpo) return;

    // estatísticas
    const contagemAbertas =
        ocorrencias.filter(
            o => o.status === 'aberta'
        ).length;

    const contagemEmAndamento =
        ocorrencias.filter(
            o => o.status === 'em_andamento'
        ).length;

    const contagemResolvidas =
        ocorrencias.filter(
            o => o.status === 'resolvida'
        ).length;

    //cabeçalho do modal
    cabecalho.innerHTML = `
        <button class="botao-fechar-historico" onclick="fecharModalHistoricoEquipamento()">✖️</button>
        <h2>${equipamento.nome}</h2>
        <p><strong>Código:</strong> ${equipamento.codigo} | <strong>Local:</strong> ${equipamento.localizacao}</p>
        <div class="estatisticas-historico-equipamento">
            <div class="estatistica-historico">
                <h3>${ocorrencias.length}</h3>
                <p>Total de Ocorrências</p>
            </div>
            <div class="estatistica-historico">
                <h3>${contagemAbertas}</h3>
                <p>Abertas</p>
            </div>
            <div class="estatistica-historico">
                <h3>${contagemEmAndamento}</h3>
                <p>Em Andamento</p>
            </div>
            <div class="estatistica-historico">
                <h3>${contagemResolvidas}</h3>
                <p>Resolvidas</p>
            </div>
        </div>
    `;
    //corpo do modal
    corpo.innerHTML = `
        <div class="lista-historico">
            <h3>📋 Histórico de Ocorrências</h3>
            ${ocorrencias.length === 0 ? `
                <div class="estado-vazio">
                    <p>Nenhuma ocorrência registrada para este equipamento</p>
                </div>
            ` : ocorrencias.map(ocorr => `
                <div class="card-historico">
                    <div class="cabecalho-card-historico">
                        <h4>${ocorr.titulo}</h4>
                        <span class="emblema-status ${ocorr.status}">
                            ${obterIconeStatus(ocorr.status)} ${obterRotuloStatus(ocorr.status)}
                        </span>
                    </div>
                    <p>${ocorr.descricao}</p>
                    <div class="rodape-card-historico">
                        <span class="data-historico">📅 ${formatarData(ocorr.data_criacao)}</span>
                        <button class="botao-ver-detalhes" onclick="visualizarOcorrenciaDoHistorico('${ocorr.id}')">
                            Ver detalhes →
                        </button>
                    </div>
                </div>
            `).join('')}
        </div>
    `;

    modal.style.display = 'flex';
}

function visualizarOcorrenciaDoHistorico(id) {
    if (!id) return;

    fecharModalHistoricoEquipamento();
    visualizarDetalhesOcorrencia(id);
}

function fecharModalHistoricoEquipamento() {
    const modal =
        document.getElementById('modalHistoricoEquipamento');

    if (modal) {
        modal.style.display = 'none';
    }
    estado.equipamentoSelecionado = null;
}

// ==========================================
// AÇÕES DE EQUIPAMENTOS
// ==========================================

async function adicionarEquipamento() {

    const nome =
        document.getElementById('nomeEquipamento').value.trim();

    const codigo =
        document.getElementById('codigoEquipamento').value.trim();

    const localizacao =
        document.getElementById('localizacaoEquipamento').value.trim();

    if (!nome || !codigo || !localizacao) {

        alert(
            'Por favor, preencha todos os campos do equipamento!'
        );

        return;
    }

    const payload = {
        nome,
        codigo,
        localizacao
    };

    try {

        const resposta = await fetch(
            '/api/equipamentos',
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json'
                },

                body: JSON.stringify(payload)
            }
        );

        if (!resposta.ok) {

            alert('Erro ao criar equipamento');

            return;
        }

        // recarrega equipamentos do backend
        await carregarEquipamentos();

        // limpa formulário
        document.getElementById(
            'nomeEquipamento'
        ).value = '';

        document.getElementById(
            'codigoEquipamento'
        ).value = '';

        document.getElementById(
            'localizacaoEquipamento'
        ).value = '';

        // fecha formulário
        const formulario =
            document.getElementById(
                'novoFormularioEquipamento'
            );

        if (formulario) {
            formulario.style.display = 'none';
        }

        atualizarSelectEquipamento();

    } catch (erro) {

        console.error(erro);

        alert(
            'Erro ao conectar com o servidor'
        );
    }
}

// ==========================================
// OUVINTES DE EVENTOS
// ==========================================

document.addEventListener('DOMContentLoaded', async function() {

    // Formulário de ocorrência
    document.getElementById('formularioOcorrencia')
        .addEventListener('submit', adicionarOcorrencia);

    // Alternar formulário de equipamento
    document.getElementById(
        'botaoAlternarFormularioEquipamento'
    ).addEventListener('click', function() {

        const formulario =
            document.getElementById(
                'novoFormularioEquipamento'
            );

        formulario.style.display =
            formulario.style.display === 'none'
                ? 'block'
                : 'none';
    });

    // Adicionar equipamento
    document.getElementById(
        'botaoAdicionarEquipamento'
    ).addEventListener(
        'click',
        adicionarEquipamento
    );

    // Navegação
    document.getElementById(
        'botaoVerEquipamentos'
    ).addEventListener('click', function() {

        estado.visualizacaoAtual = 'equipamentos';

        renderizar();
    });

    document.getElementById(
        'botaoVoltar'
    ).addEventListener('click', function() {

        estado.visualizacaoAtual = 'ocorrencias';

        renderizar();
    });

    // Abas
    document.querySelectorAll('.botao-aba')
        .forEach(botao => {

            botao.addEventListener('click', function() {

                document.querySelectorAll('.botao-aba')
                    .forEach(b =>
                        b.classList.remove('ativo')
                    );

                this.classList.add('ativo');

                estado.abaAtiva =
                    this.getAttribute('data-status');

                renderizarListaOcorrencias();
            });
        });

    // Fechar modal
    document.getElementById(
        'botaoFecharModal'
    ).addEventListener(
        'click',
        fecharModalDetalhes
    );

    document.getElementById(
        'botaoEditar'
    ).addEventListener(
        'click',
        editarOcorrencia
    );

    // Fechar modal ao clicar fora
    document.getElementById(
        'modalDetalhes'
    ).addEventListener('click', function(e) {

        if (e.target === this) {
            fecharModalDetalhes();
        }
    });

    document.getElementById(
        'modalHistoricoEquipamento'
    ).addEventListener('click', function(e) {

        if (e.target === this) {
            fecharModalHistoricoEquipamento();
        }
    });

    // ==========================================
    // CARREGAMENTO INICIAL
    // ==========================================

    await carregarEquipamentos();

    await carregarOcorrencias();

    renderizar();

    // Suporte a deep-link: se a SPA for aberta em /equipamentos/code/<codigo> ou
    // /equipamentos/<id> abre automaticamente o histórico do equipamento.
    // Prioridade: codigo (estavel para QR codes) > id numerico (fallback)
    try {
        const partes = window.location.pathname.split('/').filter(Boolean);
        if (partes.length >= 2 && partes[0] === 'equipamentos') {
            if (partes[1] === 'code' && partes.length >= 3) {
                // Rota: /equipamentos/code/IMP-01
                const codigo = decodeURIComponent(partes[2]);
                const equipamento = obterEquipamentoPorCodigo(codigo);
                if (equipamento) {
                    estado.visualizacaoAtual = 'equipamentos';
                    renderizar();
                    visualizarHistoricoEquipamento(equipamento.id);
                }
            } else if (partes.length >= 2) {
                // Rota fallback: /equipamentos/<id>
                const possibilidadeId = partes[1];
                const idNumerico = Number(possibilidadeId);
                if (!Number.isNaN(idNumerico) && idNumerico > 0) {
                    const equipamento = obterEquipamentoPorId(idNumerico);
                    if (equipamento) {
                        estado.visualizacaoAtual = 'equipamentos';
                        renderizar();
                        visualizarHistoricoEquipamento(idNumerico);
                    }
                }
            }
        }
    } catch (erro) {
        console.error('Erro ao processar deep-link:', erro);
    }
});

console.log(
    '✅ Sistema de Ocorrências carregado com sucesso!'
);
