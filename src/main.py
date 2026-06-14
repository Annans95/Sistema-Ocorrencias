from src.services.sistema import SistemaOcorrencias

sistema = SistemaOcorrencias()


def validar_id(entrada):
    # Centraliza a validação de ID para evitar repetição no menu.
    try:
        occ_id = int(entrada)
        if occ_id <= 0:
            return None
        return occ_id
    except ValueError:
        return None


def formatar_ocorrencia(ocorrencia):
    equipamento_texto = 'Nenhum equipamento vinculado'
    if ocorrencia.equipamentoId is not None:
        equipamento = sistema.buscar_equipamento_por_id(ocorrencia.equipamentoId)
        if equipamento:
            equipamento_texto = (
                f"{equipamento.nome} | Código: {equipamento.codigo} | "
                f"Localização: {equipamento.localizacao}"
            )
        else:
            equipamento_texto = f"ID {ocorrencia.equipamentoId} (não encontrado)"

    return (
        f"ID: {ocorrencia.id}\n"
        f"Título: {ocorrencia.titulo}\n"
        f"Descrição: {ocorrencia.descricao}\n"
        f"Equipamento: {equipamento_texto}\n"
        f"Status: {ocorrencia.status}\n"
        f"Data de criação: {ocorrencia.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}"
    )


def listar_ocorrencias_resumidas():
    ocorrencias = sistema.listar_ocorrencias()

    if not ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return

    # A lista aqui é curta de propósito: detalhes completos ficam na opção 4.
    print("\n=== Ocorrências cadastradas ===")
    for ocorrencia in ocorrencias:
        print(f"id: {ocorrencia.id} - {ocorrencia.titulo} ({ocorrencia.status})")


def listar_equipamentos_cli():
    equipamentos = sistema.listar_equipamentos()
    if not equipamentos:
        print("Nenhum equipamento cadastrado.")
        return

    print("\n=== Equipamentos cadastrados ===")
    for e in equipamentos:
        print(f"id: {e.id} - {e.nome} | {e.codigo} | {e.localizacao}")


def criar_equipamento_cli():
    print("\n=== Criar Equipamento ===")
    nome = input("Nome: ").strip()
    if nome.lower() == 'v':
        return
    codigo = input("Código: ").strip()
    if codigo.lower() == 'v':
        return
    localizacao = input("Localização: ").strip()
    if localizacao.lower() == 'v':
        return

    sistema.criar_equipamento(nome, codigo, localizacao)
    print("Equipamento criado e salvo no Banco!")


def editar_equipamento_cli():
    print("\n=== Editar Equipamento ===")

    # --- INÍCIO DA VALIDAÇÃO DO ID EM LOOP ---
    while True:
        entrada = input("ID do equipamento (ou 'v' para voltar): ").strip()

        if entrada.lower() == 'v':
            return  # Sai da função e volta para o menu

        if entrada == "":
            print("Erro: O ID do equipamento é obrigatório!")
            continue  # Força o loop a perguntar de novo

        try:
            eq_id = int(entrada)
            break  # ID é um número válido, sai do loop
        except ValueError:
            print("Erro: ID inválido! Digite um número inteiro.")
    # --- FIM DA VALIDAÇÃO DO ID ---

    # Busca o equipamento para ver se ele existe antes de continuar
    eq = sistema.buscar_equipamento_por_id(eq_id)
    if not eq:
        print("Equipamento não encontrado.")
        return

    # Coleta as novas informações mostrando o que já existe hoje
    nome = input(f"Nome [{eq.nome}](enter mantém): ").strip()
    codigo = input(f"Código [{eq.codigo}](enter mantém): ").strip()
    localizacao = input(f"Localização [{eq.localizacao}](enter mantém): ").strip()

    # Transforma strings vazias (apenas Enter) em None
    nome = nome if nome else None
    codigo = codigo if codigo else None
    localizacao = localizacao if localizacao else None

    # --- NOVA VALIDAÇÃO: SE TUDO FOR NONE, NADA MUDOU ---
    if nome is None and codigo is None and localizacao is None:
        print("\n Nenhuma alteração foi feita. O equipamento foi mantido igual.")
        return  # Encerra aqui sem precisar atualizar o banco

    # --- ENVIO PARA O BANCO (Só acontece se algo mudou) ---
    if sistema.atualizar_equipamento(eq_id, nome=nome, codigo=codigo, localizacao=localizacao):
        print("Equipamento atualizado e salvo no Banco!")
    else:
        print("Falha ao atualizar equipamento.")


def apagar_equipamento_cli():
    print("\n=== Apagar Equipamento ===")
    entrada = input("ID do equipamento: ").strip()
    if entrada.lower() == 'v':
        return
    try:
        eq_id = int(entrada)
    except ValueError:
        print("ID inválido")
        return

    eq = sistema.buscar_equipamento_por_id(eq_id)
    if not eq:
        print("Equipamento não encontrado")
        return

    confirmacao = input(f"Tem certeza que deseja apagar '{eq.nome}'? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada")
        return

    if sistema.remover_equipamento(eq_id):
        print("Equipamento apagado e salvo no Banco!")
    else:
        print("Falha ao apagar equipamento")


def criar_ocorrencia():
    print("\n=== Criar Ocorrência ===")
    print("Digite 'v' a qualquer momento para voltar ao menu\n")

    titulo = input("Título: ").strip()
    # "v" funciona como um atalho para voltar ao menu sem salvar nada.
    if titulo.lower() == "v":
        return

    descricao = input("Descrição: ").strip()
    if descricao.lower() == "v":
        return

    equipamento_id = None
    equipamentos = sistema.listar_equipamentos()
    if equipamentos:
        print("\nEquipamentos disponíveis:")
        for equipamento in equipamentos:
            print(f"{equipamento.id} - {equipamento.nome} | {equipamento.codigo}")

        entrada_equipamento = input("ID do equipamento (opcional): ").strip()
        if entrada_equipamento.lower() == "v":
            return
        if entrada_equipamento:
            try:
                equipamento_id = int(entrada_equipamento)
            except ValueError:
                print("ID de equipamento inválido, salvando sem vínculo.")
                equipamento_id = None

            if equipamento_id is not None and not sistema.buscar_equipamento_por_id(equipamento_id):
                print("Equipamento não encontrado, salvando sem vínculo.")
                equipamento_id = None

    sistema.criar_ocorrencia(titulo, descricao, equipamentoId=equipamento_id)
    print("Ocorrência criada e salva no Banco!")


def atualizar_status():
    print("\n=== Atualizar Status ===")
    print("Digite 'v' a qualquer momento para voltar ao menu\n")

    entrada = input("ID: ").strip()
    if entrada.lower() == "v":
        return

    occ_id = validar_id(entrada)
    if occ_id is None:
        print("ID inválido")
        return

    print("\n1 - aberta")
    print("2 - em andamento")
    print("3 - resolvida")

    opcao_status = input("Escolha o novo status: ").strip()
    if opcao_status.lower() == "v":
        return

    if opcao_status == "1":
        status = "aberta"
    elif opcao_status == "2":
        status = "em andamento"
    elif opcao_status == "3":
        status = "resolvida"
    else:
        print("Opção inválida")
        return

    if sistema.atualizar_status(occ_id, status):
        print("Atualizado e salvo no Banco!")
    else:
        print("Ocorrência não encontrada")


def ver_detalhes():
    print("\n=== Ver Detalhes ===")
    entrada = input("ID: ").strip()
    if entrada.lower() == "v":
        return

    occ_id = validar_id(entrada)
    if occ_id is None:
        print("ID inválido")
        return

    ocorrencia = sistema.buscar_ocorrencia_por_id(occ_id)

    if ocorrencia:
        print("\nDetalhes da ocorrência:")
        print(formatar_ocorrencia(ocorrencia))
    else:
        print("Ocorrência não encontrada")

def atualizar_ocorrencia_cli():
    print("\n=== Editar Ocorrência ===")

    while True:
        entrada_id = input("ID da ocorrência: ").strip()
        if entrada_id == "":
            print("Erro: O ID da ocorrência é obrigatório!")
            continue
        try:
            id = int(entrada_id)
            break
        except ValueError:
            print("Erro: O ID deve ser um número inteiro válido.")

    titulo = input("Novo título (enter mantém): ").strip()
    descricao = input("Nova descrição (enter mantém): ").strip()
    equipamentoId = input("Novo ID do equipamento (enter mantém, 'n' para remover vínculo): ").strip()

    # Tratamento das entradas vazias
    if titulo == "":
        titulo = None

    if descricao == "":
        descricao = None
    
    if equipamentoId == "":
        equipamento = None
    elif equipamentoId.lower() == "n":
        equipamento = "remover"
    else:
        try:
            equipamento = int(equipamentoId)
        except ValueError:
            print("Aviso: ID do equipamento inválido. Tratando como sem alterações.")
            equipamento = None

    # --- NOVA VALIDAÇÃO: NADA FOI ALTERADO? ---
    if titulo is None and descricao is None and equipamento is None:
        print("\nℹ Nenhuma alteração foi feita. A ocorrência foi mantida igual.")
        return # Encerra a função aqui mesmo, sem chamar o banco

    # --- ENVIO PARA O BANCO (Só acontece se algo mudou) ---
    sucesso = sistema.atualizar_ocorrencia(
        id,
        titulo=titulo,
        descricao=descricao,
        equipamentoId=equipamento
    )

    if sucesso:
        print("Ocorrência atualizada no banco com sucesso!")
    else:
        print("Erro: Ocorrência não encontrada com o ID informado.")


def excluir_ocorrencia():
    print("\n=== Excluir Ocorrência ===")
    print("Digite 'v' a qualquer momento para voltar ao menu\n")

    entrada = input("ID: ").strip()
    if entrada.lower() == "v":
        return

    occ_id = validar_id(entrada)
    if occ_id is None:
        print("ID inválido")
        return

    ocorrencia = sistema.buscar_ocorrencia_por_id(occ_id)
    if not ocorrencia:
        print("Ocorrência não encontrada")
        return

    confirmacao = input(f"Tem certeza que deseja excluir a ocorrência {occ_id}? (s/n): ").strip().lower()
    # Exigimos confirmação explícita para evitar exclusão acidental.
    if confirmacao != "s":
        print("Exclusão cancelada")
        return

    if sistema.remover_ocorrencia(occ_id):
        print("Ocorrência excluída e salva no Banco!")
    else:
        print("Não foi possível excluir a ocorrência")


def menu():
    while True:
        print("\n1 - Criar ocorrência")
        print("2 - Listar ocorrências")
        print("3 - Atualizar status")
        print("4 - Ver detalhes da ocorrência")
        print("5 - Editar ocorrencia")
        print("6 - Excluir ocorrência")
        print("7 - Listar equipamentos")
        print("8 - Criar equipamento")
        print("9 - Editar equipamento")
        print("10 - Apagar equipamento")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            criar_ocorrencia()
        elif opcao == "2":
            listar_ocorrencias_resumidas()
        elif opcao == "3":
            atualizar_status()
        elif opcao == "4":
            ver_detalhes()
        elif opcao == "5":
            atualizar_ocorrencia_cli()
        elif opcao == "6":
            excluir_ocorrencia()
        elif opcao == "7":
            listar_equipamentos_cli()
        elif opcao == "8":
            criar_equipamento_cli()
        elif opcao == "9":
            editar_equipamento_cli()
        elif opcao == "10":
            apagar_equipamento_cli()
        elif opcao == "0":
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu()