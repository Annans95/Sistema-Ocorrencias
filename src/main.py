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
    print("Equipamento criado e salvo no JSON!")


def editar_equipamento_cli():
    print("\n=== Editar Equipamento ===")
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

    nome = input(f"Nome [{eq.nome}]: ").strip()
    codigo = input(f"Código [{eq.codigo}]: ").strip()
    localizacao = input(f"Localização [{eq.localizacao}]: ").strip()

    nome = nome if nome else None
    codigo = codigo if codigo else None
    localizacao = localizacao if localizacao else None

    if sistema.atualizar_equipamento(eq_id, nome=nome, codigo=codigo, localizacao=localizacao):
        print("Equipamento atualizado e salvo no JSON!")
    else:
        print("Falha ao atualizar equipamento")


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
        print("Equipamento apagado e salvo no JSON!")
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
    print("Ocorrência criada e salva no JSON!")


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
        print("Atualizado e salvo no JSON!")
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
        print("Ocorrência excluída e salva no JSON!")
    else:
        print("Não foi possível excluir a ocorrência")


def menu():
    while True:
        print("\n1 - Criar ocorrência")
        print("2 - Listar ocorrências")
        print("3 - Atualizar status")
        print("4 - Ver detalhes da ocorrência")
        print("5 - Excluir ocorrência")
        print("6 - Listar equipamentos")
        print("7 - Criar equipamento")
        print("8 - Editar equipamento")
        print("9 - Apagar equipamento")
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
            excluir_ocorrencia()
        elif opcao == "6":
            listar_equipamentos_cli()
        elif opcao == "7":
            criar_equipamento_cli()
        elif opcao == "8":
            editar_equipamento_cli()
        elif opcao == "9":
            apagar_equipamento_cli()
        elif opcao == "0":
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu()