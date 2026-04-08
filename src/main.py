from src.services.sistema import SistemaOcorrencias

sistema = SistemaOcorrencias()


def validar_id(entrada):
    try:
        occ_id = int(entrada)
        if occ_id <= 0:
            return None
        return occ_id
    except ValueError:
        return None


def formatar_ocorrencia(ocorrencia):
    return (
        f"ID: {ocorrencia.id}\n"
        f"Título: {ocorrencia.titulo}\n"
        f"Descrição: {ocorrencia.descricao}\n"
        f"Status: {ocorrencia.status}\n"
        f"Data de criação: {ocorrencia.data_criacao.strftime('%d/%m/%Y %H:%M:%S')}"
    )


def listar_ocorrencias_resumidas():
    ocorrencias = sistema.listar_ocorrencias()

    if not ocorrencias:
        print("Nenhuma ocorrência cadastrada.")
        return

    print("\n=== Ocorrências cadastradas ===")
    for ocorrencia in ocorrencias:
        print(f"id: {ocorrencia.id} - {ocorrencia.titulo} ({ocorrencia.status})")


def criar_ocorrencia():
    print("\n=== Criar Ocorrência ===")
    print("Digite 'v' a qualquer momento para voltar ao menu\n")

    titulo = input("Título: ").strip()
    if titulo.lower() == "v":
        return

    descricao = input("Descrição: ").strip()
    if descricao.lower() == "v":
        return

    sistema.criar_ocorrencia(titulo, descricao)
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
    if confirmacao != "s":
        print("Exclusão cancelada")
        return

    if sistema.remover_ocorrencia(occ_id):
        print("Ocorrência excluída e salva no JSON!")
    else:
        print("Não foi possível excluir a ocorrência")

while True:
    print("\n1 - Criar ocorrência")
    print("2 - Listar ocorrências")
    print("3 - Atualizar status")
    print("4 - Ver detalhes da ocorrência")
    print("5 - Excluir ocorrência")
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
    elif opcao == "0":
        break

    else:
        print("Opção inválida")