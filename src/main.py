from src.services.sistema import SistemaOcorrencias

sistema = SistemaOcorrencias()

while True:
    print("\n1 - Criar ocorrência")
    print("2 - Listar ocorrências")
    print("3 - Atualizar status")
    print("4 - Ver detalhes da ocorrência")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        print("\n=== Criar Ocorrência ===")
        print("Digite 'v' a qualquer momento para voltar ao menu\n")

        titulo = input("Título: ")
        if titulo.lower() == "v":
            continue

        descricao = input("Descrição: ")
        if descricao.lower() == "v":
            continue

        sistema.criar_ocorrencia(titulo, descricao)
        print("Ocorrência criada!")

    elif opcao == "2":
        ocorrencias = sistema.listar_ocorrencias()
        if not ocorrencias:
            print("Nenhuma ocorrência cadastrada.")
        else:
            for o in ocorrencias:
                print(o)

    elif opcao == "3":
        print("\n=== Atualizar Status ===")
        print("Digite 'v' a qualquer momento para voltar ao menu\n")

        entrada = input("ID: ")
        if entrada.lower() == "v":
            continue

        if not entrada.isdigit():
            print("ID inválido")
            continue

        id = int(entrada)

        print("\n1 - aberta")
        print("2 - em andamento")
        print("3 - resolvida")

        opcao_status = input("Escolha o novo status: ")
        if opcao_status.lower() == "v":
            continue

        if opcao_status == "1":
            status = "aberta"
        elif opcao_status == "2":
            status = "em andamento"
        elif opcao_status == "3":
            status = "resolvida"
        else:
            print("Opção inválida")
            continue

        if sistema.atualizar_status(id, status):
            print("Atualizado!")
        else:
            print("Ocorrência não encontrada")

    elif opcao == "4":
        entrada = input("ID: ")
        if entrada.lower() == "v":
            continue

        if not entrada.isdigit():
            print("ID inválido")
            continue

        id = int(entrada)

        ocorrencia = sistema.buscar_ocorrencia_por_id(id)

        if ocorrencia:
            print("\nDetalhes da ocorrência:")
            print(f"ID: {ocorrencia.id}")
            print(f"Título: {ocorrencia.titulo}")
            print(f"Descrição: {ocorrencia.descricao}")
            print(f"Status: {ocorrencia.status}")
        else:
            print("Ocorrência não encontrada")

    elif opcao == "0":
        break

    else:
        print("Opção inválida")